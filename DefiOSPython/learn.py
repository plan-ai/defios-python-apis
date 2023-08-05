# right now, our application is limited enough that using the openai python
# lib makes sense, if we expand the functionality in the future which is included
# in current frameworks like Langchain, it might make sense to refactor this
import openai
import configparser
from authentication import validate_user
from flask import make_response, jsonify
import requests
import urllib.parse
from models import DailyFeatured
import re


def uri_encode(data):
    """
    URI encodes the given data.

    Args:
        data (str): The data to be URI encoded.

    Returns:
        str: URI encoded data.
    """
    return urllib.parse.quote(data)


config = configparser.ConfigParser()
config.read("config.ini")
openai.api_key = config["OPENAI"]["API_KEY"]
github_key = config["GITHUB"]["AUTH_TOKEN"]


# reads content from file
# to be used to read github docs for txt or MD file
def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


issue_search_api_docs = read_file("../API_DOCS/issue_search.txt")
if issue_search_api_docs is None:
    raise Exception("Please provide issue search documentation to get the API running")


def engineer_prompt(user_gh_name, user_experience, request, docs):
    prompt = """"{}
    Now, imagine a user {}. {}.
    
    He wants a roadmap of basic Github issues that he can solve to learn {}. 
    Can you please send him a list of 5 open github issues on recent repos so that he can solve to 
    gain some basic experience in it. Make sure the issues are beginner friendly. 
    Write a curl request to retrieve the issues.Assume that there may be no issues are labelled good first issues.
    Also write a curl to get most common repos in the space and push it to the issues api.
    Send the curl for issue api first before the repo api call
    """.format(
        docs, user_gh_name, user_experience, request
    )
    return prompt


# Function to parse curl command and extract URL, headers, etc.
def parse_curl_command(curl_command):
    url = re.findall(r'"(https?://.*?)"', curl_command)
    if len(url) != 0:
        return url[0]
    return None


# parses curl from response
def parse_curl(response):
    result = []
    curl_split = response.split("curl")[1:]
    for split_string in curl_split:
        parsed_result = parse_curl_command(
            split_string.strip().replace("<YOUR-TOKEN>", openai.api_key)
        )
        if parsed_result is not None:
            result.append(parsed_result)
    return result


def add_issue_filter(issue_url):
    return issue_url.split("q=")[0] + "q=is:issue+" + issue_url.split("q=")[1]


def parse_chatgpt_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # GPT-3.5 engine
            prompt=prompt,
            max_tokens=500,  # Maximum number of tokens in the generated response
            stop=None,  # Set custom stop sequences if needed
        )
        top_response = response.choices[0].text.strip()
        return parse_curl(top_response)
    except openai.OpenAIError:
        return None


def call_github_api(api_url, token):
    return requests.get(api_url, headers={"Authorization": f"Bearer {token}"}).json()


def change_repo_param(url, new_repo):
    """
    Changes the 'repo' parameter in the given URL to a new repository.

    Args:
        url (str): The URL to modify.
        new_repo (str): The new repository name to set for 'repo' parameter.

    Returns:
        str: The modified URL with the updated 'repo' parameter.
    """
    # Use regular expression to find and replace the 'repo' parameter with the new repository name
    pattern = r"q:repo=([\w\-]+\/[\w\-]+)"
    modified_url = re.sub(pattern, f"q:repo={new_repo}", url)

    return modified_url


def remove_duplicates(input_list):
    unique_list = []
    for item in input_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def learn_search(token, request):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        prompt = engineer_prompt(
            resp.user_gh_name,
            ""
            if resp.user_experiences == []
            else "He/she has contributed before in"
            + ", ".join(resp.user_experiences[:-1])
            + ", and "
            + resp.user_experiences[-1],
            request,
            issue_search_api_docs,
        )
        response = parse_chatgpt_response(prompt)
        if response is None:
            message = {"error": "OpenAICallFailed"}
            status_code = 400
        else:
            github_api_key = (
                github_key if resp.user_github_auth is None else resp.user_github_auth
            )
            try:
                [issue_api, repo_api] = response
                repos = call_github_api(repo_api, github_api_key)
            except:
                issue_api = response[0]
            common_repos = []
            issue_api = add_issue_filter(issue_api)
            try:
                if "total_count" in repos.keys() and repos["total_count"] != 0:
                    for repo in repos["items"]:
                        if len(common_repos) > 2:
                            break
                        if "full_name" in repo.keys():
                            common_repos.append(repo["full_name"])
                        else:
                            common_repos.append(
                                f"{repo['owner']['login']}/{repo['name']}"
                            )
            except:
                pass
            if len(issue_api.split("topic:")) > 1:
                issue_api = (
                    issue_api.split("topic:")[0]
                    + issue_api.split("topic:")[1].split("+", maxsplit=1)[1]
                )
            if common_repos != []:
                issues = call_github_api(
                    change_repo_param(issue_api, common_repos[0]), github_api_key
                )["items"][:5]
                second_issues = call_github_api(
                    change_repo_param(issue_api, common_repos[1]), github_api_key
                )["items"][:-5]
                issues.extend(second_issues)
                issues = remove_duplicates(issues)[:5]
            else:
                issues = issues = call_github_api(issue_api, github_api_key)["items"][
                    :5
                ]
            if issues == []:
                message = {"error": "Could not find any results"}
                status_code = 404
            else:
                message = {
                    "learn_search_user": resp.user_github,
                    "search_results": issues,
                }
                status_code = 200
                cached_learn_search = [issue["html_url"] for issue in issues]
                resp.update(
                    set__user_cached_learn_search=cached_learn_search,
                    set__user_cached_learn_query=request,
                )
    except Exception as err:
        message = {"error": "LearnSearchFailed", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)


def resume_last_roadmap(token):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        cached_roadmap = resp.user_cached_learn_search
        if len(cached_roadmap) == 0:
            message = {"error": "No Cached Roadmaps Found"}
            status_code = 404
        else:
            message = {
                "learn_search_user": resp.user_github,
                "learn_search_last_query": resp.user_cached_learn_query,
                "search_results": cached_roadmap,
            }
            status_code = 200
    except Exception as err:
        message = {"error": "ResumeRoadmapFailed", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)


def get_featured_repo(token):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        daily_featured = DailyFeatured.objects().first()
        if daily_featured is None:
            message = {"message": "No Daily Featured repo"}
            status_code = 404
        else:
            repo = daily_featured.featured_repo
            github_api_key = (
                github_key if resp.user_github_auth is None else resp.user_github_auth
            )
            response = call_github_api(
                f"https://api.github.com/repos/{repo}", github_api_key
            )
            message = {
                "featured_search_user": resp.user_github,
                "featured_repo": response,
            }
            status_code = 200
    except Exception as err:
        message = {"error": "FeaturedRepoSearchFailed", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)

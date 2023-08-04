# right now, our application is limited enough that using the openai python
# lib makes sense, if we expand the functionality in the future which is included
# in current frameworks like Langchain, it might make sense to refactor this
import openai
import configparser
from authentication import validate_user
from flask import make_response, jsonify

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
    Can you please send him a list of 5 open github issues on current Solana repos that he can solve to 
    gain some basic experience in it. Make sure the issues are beginner friendly. 
    Write a curl request to retrieve the issues.Assume that there may be no issues are labelled good first issues.
    Make sure the issue is not assigned to any other github user.Also write a curl to get most common repos in the 
    space and push it to the issues api.
    """.format(
        docs, user_gh_name, user_experience, request
    )
    return prompt


# Function to parse curl command and extract URL, headers, etc.
def parse_curl_command(curl_command):
    print(curl_command)
    parts = curl_command.split(" ")
    for i, part in enumerate(parts):
        if part.startswith('"https'):
            return part.strip('"').split('"')[0]
    return None


# parses curl from response
def parse_curl(response):
    curl_split = response.split("curl")[1:]
    return [
        parse_curl_command(split_string.strip().replace("<YOUR-TOKEN>", openai.api_key))
        for split_string in curl_split
    ]


def paerse_chatgpt_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # GPT-3.5 engine
            prompt=prompt,
            max_tokens=500,  # Maximum number of tokens in the generated response
            stop=None,  # Set custom stop sequences if needed
        )
        top_response = response.choices[0].text.strip()
        return parse_curl(top_response)
    except openai.OpenAIError as e:
        return None


def learn_search(token, request):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        prompt = engineer_prompt(
            resp.user_gh_name,
            ""
            if resp.user_experiences is None
            else ", ".join(resp.user_experiences[:-1])
            + ", and "
            + resp.user_experiences[-1],
            request,
            issue_search_api_docs,
        )
        response = paerse_chatgpt_response(prompt)
        if response is None:
            message = {"error": "OpenAICallFailed"}
            status_code = 400
        else:
            api_key = (
                github_key if resp.user_github_auth is None else resp.user_github_auth
            )
            message = {
                "learn_search_user": resp.user_github,
                "search_results": response,
            }
            status_code = 200
    except Exception as err:
        message = {"error": "LearnSearchFailed", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)

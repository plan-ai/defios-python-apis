import requests


def get_all_commits_for_user(id, username, access_token):
    endpoint = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    query = f"""
    query {{
      user(login: "{username}") {{
        repositories(first: 100) {{
          edges {{
            node {{
              name
              defaultBranchRef {{
                name
              }}
              ref(qualifiedName: "refs/heads/master") {{
                target {{
                  ... on Commit {{
                    history(first: 100, author: {{ id: "{id}" }}) {{
                      edges {{
                        node {{
                          oid
                          changedFilesIfAvailable
                          commitUrl
                          treeUrl
                        }}
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(endpoint, json={"query": query}, headers=headers)
    response_data = response.json()

    if "errors" in response_data:
        raise Exception(f"Error occurred: {response_data['errors'][0]['message']}")

    all_commits = []
    repositories = response_data["data"]["user"]["repositories"]["edges"]
    for repo in repositories:
        commits = repo["node"]["ref"]
        if commits is None:
            continue
        commits = commits["target"]["history"]["edges"]
        all_commits.extend(commits)

    return all_commits

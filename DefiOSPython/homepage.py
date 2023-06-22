from authentication import validate_user
from models import Roadmaps, Token, Issues, Projects
from flask import make_response, jsonify
from collections import defaultdict


def fetch_progress_json(progress_items):
    progress_json = defaultdict(list)
    for item in progress_items:
        progress_json[item.progress_type].append(
            [item.progress_text, item.progress_true]
        )
    return progress_json


def fetch_homepage(token):
    """
    Used to load data to be shown on homepage that opens to a user

    Parameters
    --------------------
    token:string
                  Unique jwt identifier of the user

    Returns
    --------------------
    issues -> List[Issues]:
            Return list of Issue model raw json of the issues with the highest stake amount
    tokens -> List[Token]:
                Return list of Token model raw json of 4 randomly sampled Token models without their mongoid
    roadmap -> Roadmap:
                Returns raw json of roadmap model with the highest number of active objectives
    projects -> List[Projects]:
                 Returns list of projects ordered by community_health in descending order and secondarily by num_open_issues in descending order
    paths -> List[List]
                key(progress_type:str):[
                    [
                        progress_text:str,
                        progress_true:bool
                    ]
                ]
             Returns an array or array that lists how far the use rhas advanced in each of the three respective walkthrough
    """
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        message = {}

        message["tokens"] = Token.objects(token_new=True).aggregate(
            [{"$sample": {"size": 4}}]
        )
        message["tokens"] = [i for i in message["tokens"]]
        for i in message["tokens"]:
            del i["_id"]

        message["issues"] = (
            Issues.objects(issue_state="open").order_by("-issue_stake_amount").limit(3)
        )
        message["issues"] = [i.parse_to_json() for i in message["issues"]]

        roadmap = Roadmaps.objects.order_by("-roadmap_active_objectives").first()
        message["roadmap"] = {} if roadmap is None else roadmap.to_roadmap_json()

        message["paths"] = fetch_progress_json(resp.user_progress)

        try:
            message["projects"] = (
                Projects.objects.order_by("-community_health", "-num_open_issues")
                .first()
                .parse_to_json(resp.user_github)
            )
        except:
            message["projects"] = {}

        status_code = 200
    except Exception as err:
        message = {"error": "HomepageFetchFailed", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)

from authentication import validate_user
from models import Roadmap, Token, Issues, Projects
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
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        message = {}

        message["tokens"] = Token.objects.aggregate(
            [{"$sample":{"size": 4}}]
        )
        message["tokens"] = [i for i in message["tokens"]]
        for i in message["tokens"]:
            del i["_id"]
        
        message["issues"] = Issues.objects(
            issue_state="open"
        ).order_by("-issue_stake_amount").limit(3)
        message["issues"] = [i.parse_to_json() for i in message["issues"]]

        message["roadmap"] = Roadmap.objects.order_by(
            "-roadmap_active_objectives"
        ).first().to_roadmap_json()
        
        message["paths"] = fetch_progress_json(resp.user_progress)
        
        message["projects"] = Projects.objects.order_by(
            "-community_health", "-num_open_issues"
        ).first().parse_to_json()
        
        status_code = 200
    except:
        message = {"error": "HomepageFetchFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)
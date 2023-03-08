from models import Issues
from authentication import validate_user
from flask import make_response, jsonify
from bson.objectid import ObjectId
import json
from utils import isfloat, remove_dups_by_id

def fetch_issues(token, request_params):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    
    try:
        start_id = request_params.get("first_id", None)    

        filter_params = {
            i.split(".")[1]: request_params[i]
            for i in request_params if "filter" in i and request_params[i] != ""
        }
        search_params = {
            i.split(".")[1]: request_params[i]
            for i in request_params if "search" in i and request_params[i] != ""
        }

        for i in search_params:
            if search_params[i] in ["false", "true"]:
                search_params[i] = {"$eq":json.loads(search_params[i])}
            elif i == "issue_creator_gh":
                search_params[i] = {"$eq": search_params[i]}
            elif search_params[i].isdigit() and i != "issue_creator_gh":
                search_params[i] = {"$gt": int(search_params[i])}
            elif isfloat(search_params[i]):
                search_params[i] = {"$gt": float(search_params[i])}
            elif "," in i:
                search_params[i] = {"$in": search_params[i].split(",")}
            else:
                search_params[i] = {"$regex": search_params[i]}

        for i in filter_params:
            if filter_params[i] in ["false", "true"]:
                filter_params[i] = json.loads(filter_params[i])
            elif filter_params[i].isdigit():
                filter_params[i] = int(filter_params[i])

        if filter_params.get("mine", False):
            search_params["issue_creator_gh"] = resp.user_github

        if not filter_params.get("order_by", False):
            filter_params["order_by"] = "-issue_stake_amount"


        issues = Issues.objects(
            __raw__=search_params
        ).order_by(
            filter_params["order_by"]
        ).skip(
            (filter_params["pageno"]-1)*filter_params["pagesize"]
        ).limit(filter_params["pagesize"]).all()

        cleaned_issues = [i.parse_to_json() for i in issues]

        message = {
            "issues": cleaned_issues
        }
        
        if start_id is not None:
            start_issue = Issues.objects(id=ObjectId(start_id)).first().parse_to_json()
            message["issues"].insert(0, start_issue)
            message = {
                "issues": remove_dups_by_id(message["issues"])
            }

        status_code = 200
    
    except Exception:
        message = {"error": "IssueFetchError"}
        status_code = 400
    
    return make_response(jsonify(message), status_code)

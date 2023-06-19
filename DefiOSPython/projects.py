from models import Projects, Token
from authentication import validate_user
from flask import make_response, jsonify
from bson.objectid import ObjectId
from utils import remove_dups_by_id
import json


def fetch_projects(token, request_params):
    """
    Used to push a firebase notif to the web frontend

    Parameters
    --------------------
    token:string
                  Unique jwt identifier of the user to authenticate notif request, all users are set to admin for this demonstration
    notif_json: json
                Json data regarding the notif, contains the following data:
                     user_github: Github uid of the user

    Returns
    --------------------
    message:
            Indicates whether the request was successful or not
    """
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        start_id = request_params.get("first_id", None)
        filter_params = {
            i.split(".")[1]: request_params[i]
            for i in request_params
            if "filter" in i and request_params[i] != ""
        }
        search_params = {
            i.split(".")[1]: request_params[i]
            for i in request_params
            if "search" in i and request_params[i] != ""
        }
        for i in search_params:
            if search_params[i] in ["false", "true"]:
                search_params[i] = {"$eq": json.loads(search_params[i])}
            elif "," in search_params[i]:
                search_params[i] = {"$in": search_params[i].split(",")}
            elif search_params[i].isdigit() and i != "project_owner_github":
                search_params[i] = {"$gt": int(search_params[i])}
            elif i == "project_owner_github":
                search_params[i] = {"$eq": search_params[i]}
            else:
                search_params[i] = {"$regex": search_params[i]}

        for i in filter_params:
            if filter_params[i] in ["false", "true"]:
                filter_params[i] = json.loads(filter_params[i])
            elif filter_params[i].isdigit():
                filter_params[i] = int(filter_params[i])

        if filter_params.get("mine", False):
            search_params["project_owner_github"] = resp.user_github

        if not filter_params.get("order_by", False):
            filter_params["order_by"] = "-num_open_issues"

        projects = (
            Projects.objects(__raw__=search_params)
            .order_by(filter_params["order_by"])
            .skip((filter_params.get("pageno", 1) - 1) * filter_params["pagesize"])
            .limit(filter_params["pagesize"])
            .all()
        )

        cleaned_projects = [i.parse_to_json(resp.user_github) for i in projects]

        message = {"projects": cleaned_projects}

        if start_id is not None:
            start_project = (
                Projects.objects(id=ObjectId(start_id))
                .first()
                .parse_to_json(resp.user_github)
            )
            message["projects"].insert(0, start_project)
            message["projects"] = remove_dups_by_id(message["projects"])

        status_code = 200
    except Exception as err:
        message = {"error": "ProjectsFetchFailed", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)


def mark_tokens_as_claimed(token, project_id):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp

    try:
        project = Projects.objects(id=ObjectId(project_id)).first()
        project.update(
            set__claimers_pending=[
                i for i in project.claimers_pending if i != resp.user_github
            ]
        )
        message = {"message": "ClaimMarkingSuccessful"}
        status_code = 200

    except:
        message = {"error": "ClaimMarkingFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)


def fetch_projects_minified(token):
    """
    Used to fetch projects in a minified fashion

    Parameters
    --------------------
    token:string
                  Unique jwt identifier of the user

    Returns
    --------------------
    message -> List[Json]:
            List[
                project_name: Name of Project,
                token_url: Url of image related to token of the project,
                id: Project mongoid,
                account:Name of project account,
                project_url: Github link of project
            ]
    """
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        projects = Projects.objects.only(
            "project_name", "project_token", "project_repo_link", "project_account"
        ).all()
        message = []
        for project in projects:
            message.append(
                {
                    "project_name": project.project_name,
                    "token_url": "https://ipfs.io/ipfs/QmZDH8LNFytG1YaMHcAaBEMFgAK56HCd2vbuTqwbvB1thN"
                    if project.project_token is None
                    else project.project_token.token_image_url,
                    "id": str(project.id),
                    "account": project.project_account,
                    "project_url": "https://github.com/defi-os/defios-alpha"
                    if project.project_repo_link == ""
                    else project.project_repo_link,
                }
            )
        status_code = 200
    except Exception:
        message = {"error": "Project Fetch Failed"}
        status_code = 400
    return make_response(jsonify(message), status_code)


def edit_token(auth: str, project_key: str, args: dict):
    isAuthorized, resp = validate_user(auth)
    if not isAuthorized:
        return resp
    try:
        project = (
            Projects.objects(project_key=project_key).only("roadmap_creator_gh").first()
        )
        if resp.user_github == project.roadmap_creator_gh:
            token = Token.objects(token_symbol=args["symbol"]).first()
            if token is None:
                token = Token(
                    token_name=args["name"],
                    token_symbol=args["symbol"],
                    token_image_url=args["image"],
                    token_new=False,
                )
                token.save()
            project.update(set__project_token=token)
            message = {"message": "Token added sucessfullt"}
            status_code = 200
        else:
            message = {"message": "Not authorized to perform this action"}
            status_code = 401
    except Exception:
        message = {"error": "Project Fetch Failed"}
        status_code = 400
    return make_response(jsonify(message), status_code)

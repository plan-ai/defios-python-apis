from models import Token
from authentication import validate_user
from flask import make_response, jsonify

def fetch_token_details(token, token_symbol):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        token = Token.objects(
            token_symbol=token_symbol
        ).first().to_mongo().to_dict()
        token["_id"] = str(token["_id"])
        message = {"details": token}
        status_code = 200
    except Exception:
        message = {"details": "TokenFetchFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)


def fetch_token_list(token):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        tokens = Token.objects.only("token_image_url", "token_symbol", "token_spl_addr").all()
        message = [i.to_mongo().to_dict() for i in tokens]
        for i in message:
            del i["_id"]
        status_code = 200
    except Exception:
        message = {"error": "TokenListFetchFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)
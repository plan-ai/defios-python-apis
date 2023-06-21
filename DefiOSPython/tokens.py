from models import Token
from authentication import validate_user
from flask import make_response,jsonify

def get_token(auth:str,token_addr:str):
    isAuthorized, resp = validate_user(auth)
    if not isAuthorized:
        return resp
    try:
        token = Token.objects(token_spl_addr=token_addr).first()
        message = token.to_mongo().to_dict()
        del message["_id"]
        status_code=200
    except Exception:
        message = {"error": "NotificationFetchFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)

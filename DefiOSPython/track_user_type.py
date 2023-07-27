from authentication import validate_user
from flask import jsonify, make_response


def track_user_type(token, user_type):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        resp.update(set__user_type=user_type)
        message = {
            "message": "AddUserDataSuceeded",
            "user": resp.user_github,
            "user_type": user_type,
        }
        status_code = 200
    except Exception as err:
        message = {"error": "AddUserDataFailed", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)

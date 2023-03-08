from authentication import validate_user
from models import ProgressItem
from flask import make_response, jsonify


def profile_contributions(token):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        message = resp.fetch_contributions()
        status_code = 200
    except Exception:
        message = {"error": "ProfileContributionFetchFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)


def update_user_progress(token, progress_type, progress_title):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        progress_master = resp.user_progress
        n = len(progress_master)
        for i in range(n):
            if progress_master[i].progress_type == progress_type and progress_master[i].progress_title == progress_title:
                progress_master[i] = ProgressItem(
                    progress_type=progress_type,
                    progress_master=progress_master,
                    progress_true=True
                )
        resp.update(set__user_progress=progress_master)
        message = {"message": "ProgressUpdateSuccessful"}
        status_code = 200
    except Exception:
        message = {"error": "ProgressUpdateFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)


def generate_portfolio_website(token, template_type):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        message = {"link": "https://portfolios.defi-os.com/never2average"}
        status_code = 200
    except:
        message = {"error": "ProfileURLCreationFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)
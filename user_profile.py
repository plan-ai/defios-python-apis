from authentication import validate_user
from models import ProgressItem
from flask import make_response, jsonify


def profile_contributions(token):
    """
    Used to fetch a users profile contributions
    
    Parameters
    --------------------
    token:string
                  Unique jwt identifier of the user to authenticate notif request, all users are set to admin for this demonstration
    Returns
    --------------------
    message -> List[Json]:
            List[
                contribution_amt: Amount given upon contribution by or to the user,
                contribution_link: Github pull request link of contribution,
                contribution_timestamp: Timestamp at which contribution occured,
                contribution_token_icon:Icon url of token in which contributor was paid by or to the user,
                contribution_token_symbol: Symbol of token in which contributor was paid by or to the user,
                contribution_type: Wether they staked the money on the issue or got money from contributing to it,
                contributor_github: Github UID of contributor,
                contributor_name: Name of contributor,
                contributor_profile_pic: Profile pic of contributor,
                contributor_project_id: mongodb id of project on which contributor contributed,
                contributor_project_name: Name of project in which contribution was made

            ]
    """
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
    """
    Used to update a users progress status
    
    Parameters
    --------------------
    token:string
                  Unique jwt identifier of the user to authenticate notif request, all users are set to admin for this demonstration
    progress_type: string
                      Type of progress in walkthrough(developer,enterprise,maintainer) 
    progress_title: string 
                      Title of progression step in walkthrough passed                

    Returns
    --------------------
    message:
            Indicates whether the request was successful or not
    """
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
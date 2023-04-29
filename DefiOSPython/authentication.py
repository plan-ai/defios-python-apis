import jwt
from models import Users, ProgressItem, Waitlist
from flask import make_response, jsonify

import requests


def verify_gh_access_token(github_uid, gh_access_token):
    """
    Used as an internal helper function to validate if the
    github_uid and gh_acess_token sent into the function
    are of convergent origin and return the name and
    avatar url(github profile pic) if true
    """
    url = "https://api.github.com/user"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {gh_access_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(url, headers=headers).json()
    if int(github_uid) != response["id"]:
        return False, None, None
    return True, response["name"], response["avatar_url"]


def set_progress_init(user):
    progress_chkpts = {
        "developer": [
            "Login with Github",
            "Connect your Phantom Wallet",
            "Look at existing open source projects",
            "Look for issues matching your skill sets",
            "Submit a Pull Request to close an open issue",
            "Stake project tokens on an open issue",
            "Vote for a Pull Request on an open issue",
            "Claim your token rewards for solving an issue",
            "Check out our jobs feature",
            "Signup for our jobs waitlist",
        ],
        "maintainer": [
            "Login with Github",
            "Connect your Phantom Wallet",
            "Convert your repositories into projects",
            "Check out your projects",
            "Check out open issues on your projects",
            "Stake project tokens to onboard contributors",
            "Advance your project's roadmap by incentivizing objectives",
        ],
        "enterprise": [
            "Login with Github",
            "Connect your Phantom Wallet",
            "Use tokens to prioritize your relevant issues",
        ],
    }
    progress = []
    for i in progress_chkpts:
        for idx, item in enumerate(progress_chkpts[i]):
            progress.append(
                ProgressItem(
                    progress_type=i, progress_text=item, progress_true=(idx == 1)
                )
            )
    user.update(set__user_progress=progress)


def generate_jwt(github_uid, firebase_uid, gh_access_token, pub_key):
    """
    Used to generate a unique jwt token for a user
    to authenticate requests to the server from the
    user

    Parameters
    --------------------
    github_uid:string
                  Unique github user id of the user's github account
    firebase_uid:string
                    Unique firebase uid of the user
    gh_access_token:string
                       Github access token of the user
    pub_key:string
               User's pubblic key on the solana blockchain



    Returns
    --------------------
    auth_creds:
               Unique JWT token of the user that can be used to authenticate the user
    firebase:
             Unique firebase uid of the user
    """
    try:
        is_gh_valid, user_gh_name, user_gh_profile_pic = verify_gh_access_token(
            github_uid, gh_access_token
        )
        if not is_gh_valid:
            raise Exception
        user = Users.objects(user_github=github_uid).first()
        if user is None:
            user = Users(
                user_github=github_uid,
                user_fb_uid=firebase_uid,
                user_gh_name=user_gh_name,
                user_profile_pic=user_gh_profile_pic,
                user_phantom_address=pub_key,
            )
            user.save()
            set_progress_init(user)
        else:
            user.update(set__user_fb_uid=firebase_uid)
        token = jwt.encode(
            {"github": github_uid, "firebase": firebase_uid},
            "SOME_JWT_SECRET",
            "HS256",
        )
        message = {"auth_creds": token, "firebase": firebase_uid}
        status_code = 200
    except Exception:
        message = {"error": "JWTFetchFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)


def validate_user(token):
    unauthorizedResponse = make_response(
        jsonify({"message": "Invalid or Expired User token"}), 401
    )
    try:
        github_uid = jwt.decode(token, "SOME_JWT_SECRET", ["HS256"])["github"]
        user = Users.objects(user_github=github_uid).first()
        if user is not None:
            return True, user
        return False, unauthorizedResponse
    except Exception:
        return False, unauthorizedResponse


def add_to_waitlist(email, wl_type="jobs"):
    """
    Used to add a user with given email to waitlist

    Parameters
    --------------------
    email:string
                  Email of user to be added to waitlist
    wl_type:string
                  Waitlist type to which user must be added, defaults to jobs

    Returns
    --------------------
    message:
            Indicates that the request was sucessful
    """
    wl = Waitlist(waitlist_email=email, waitlist_type=wl_type)
    wl.save()
    message = {"message": "signup_successful"}
    status_code = 200
    return make_response(jsonify(message), status_code)

from models import Token
from authentication import validate_user
from flask import make_response, jsonify

def fetch_token_details(token, token_symbol):
    """
    List details regarding a token 
    
    Parameters
    --------------------
    token:string
                  Unique jwt identifier of the user
    token_symbol:string
                  Symbol of token regarding which data is to be queried

    Returns
    --------------------
    message -> Token:
            Return token model raw json
    """
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
    """
    Used to fetch list of tokens
    
    Parameters
    --------------------
    token:string
                  Unique jwt identifier of the user

    Returns
    --------------------
    message -> List[Json]:
            List[
                token_image_url: Link of token icon,
                token_spl_addr: Public address where token smart contract is hosted,
                token_symbol: Symbol of token
            ]
    """
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
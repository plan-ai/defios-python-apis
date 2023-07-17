from flask import Response
import requests


def filter_headers(headers):
    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
        "access-control-allow-credentials",
        "access-control-allow-origin",
    ]
    return [
        (name, value)
        for (name, value) in headers
        if name.lower() not in excluded_headers
    ]


def api_request(path, request):
    """A catch-all route that proxies https://api.mixpanel.com

    This provides support for all of the Mixpanel Ingestion API endpoints in a single route.
    You could break this into multiple routes for /track, /engage, and /groups if you want
    more control over each request type.
    """

    # /decide is hosted on a different subdomain
    mixpanel_url = (
        "https://decide.mixpanel.com"
        if path == "decide"
        else "https://api.mixpanel.com"
    )

    # This relays the client's IP for geolocation lookup
    # The method via which you can retrieve the "real" client IP
    # is implementation specific so you may need to change this logic.
    if "HTTP_X_FORWARDED_FOR" in request.environ:
        ip = request.environ["HTTP_X_FORWARDED_FOR"]
    elif "HTTP_X_REAL_IP" in request.environ:
        ip = request.environ["HTTP_X_REAL_IP"]
    else:
        ip = request.remote_addr

    headers = {"X-REAL-IP": ip}

    # pass the request directly to Mixpanel
    resp = requests.request(
        method=request.method,
        url="%s/%s" % (mixpanel_url, path),
        headers=headers,
        params=request.args,
        data=request.form,
    )

    # filter out some irrelevant response headers
    headers = filter_headers(resp.raw.headers.items())

    # return the response from Mixpanel
    return Response(resp.content, resp.status_code, headers)

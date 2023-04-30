import json
from jinja2 import Template
from jinja2.utils import markupsafe
import boto3
import configparser
from authentication import validate_user
from flask import make_response, jsonify

config = configparser.ConfigParser()
config.read("config.ini")

bucketName = config["AWS"]["BUCKETNAME"]
cdn = config["AWS"]["CDN"]


def generate_website(requestData):
    # converts educational credentials sent into markup langauge for templating
    for i in requestData["education"]:
        i["summary"] = markupsafe.Markup(i["summary"])

    # opens jinja2 template with requested template_no
    template = open("../templates/template_{}.html".format(requestData["template_no"]))
    template = Template(template.read())

    # renders portfolio of user in requested template
    portfolio = template.render(data=requestData)

    # Pushed the portfolio to a s3 bucket
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(bucketName)
    key = (
        requestData["social"]["github_url"].replace("@", "-").replace(".", "-")
        + ".html"
    )
    bucket.put_object(
        Body=portfolio, Key=key, ACL="public-read", ContentType="text/html"
    )

    # sends in cloudfront link of generated portfolio
    web_page_url = "https://{}.s3.ap-south-1.amazonaws.com/{}".format(bucketName, key)

    return web_page_url


def generate_portfolio_website(token, template_type):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        requestData = {
            "profile_pic_url": resp.user_profile_pic,
            "profile_name": resp.user_gh_name,
            "social": {"github_url": resp.user_github},
            "template_no": template_type,
        }
        message = {"link": generate_website(requestData)}
        status_code = 200
    except:
        message = {"error": "ProfileURLCreationFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)

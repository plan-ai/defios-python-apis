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


def lambda_handler(event):
    # request data sent by users
    requestData = event["body"]["data"]

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
    key = requestData["social"]["email"].replace("@", "-").replace(".", "-") + ".html"
    bucket.put_object(
        Body=portfolio, Key=key, ACL="public-read", ContentType="text/html"
    )

    # sends in cloudfront link of generated portfolio
    web_page_url = "https://{}.s3.ap-south-1.amazonaws.com/{}".format(bucketName, key)

    # api response
    response = {
        "statusCode": 200,
        "body": json.dumps(
            {"message": "Successfully Generated CV!", "url": web_page_url}
        ),
    }

    return response


def generate_portfolio_website(token, template_type):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        message = {"link": "https://userportfolios.s3.ap-south-1.amazonaws.com/tanmaymunjal64-gmail-com.html"}
        status_code = 200
    except:
        message = {"error": "ProfileURLCreationFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)


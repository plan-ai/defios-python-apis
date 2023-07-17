from flask import Flask, make_response, jsonify
from flask_restful import Api, Resource, request
import mongoengine
from flask_cors import CORS
from authentication import generate_jwt, add_to_waitlist
from notifications import fetch_notifications, post_notifications, mark_notifs_as_read
from projects import fetch_projects, fetch_projects_minified, edit_token
from issues import fetch_issues
from user_profile import profile_contributions, update_user_progress
from roadmaps import get_roadmaps, get_roadmap_objectives, get_roadmap_projects
from homepage import fetch_homepage
from swap import fetch_token_details, fetch_token_list
from portfolio_generator import generate_portfolio_website
from tokens import get_token
from mixpanel_proxy import api_request
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
try:
    mongoengine.connect(config["MONGODB"]["HOST"])
except:
    mongoengine.connect("DefiOS")


class Tokens(Resource):
    def get(self):
        return get_token(
            request.headers.get("Authorization"), request.args.get("token_addr")
        )


class Notifications(Resource):
    def get(self):
        return fetch_notifications(request.headers.get("Authorization"))

    def post(self):
        return post_notifications(
            request.headers.get("Authorization"), request.get_json()
        )


class Projects(Resource):
    def get(self):
        return fetch_projects(request.headers.get("Authorization"), request.args)

    def post(self):
        return edit_token(
            request.headers.get("Authorization"),
            request.args.get("project_key"),
            request.get_json(),
        )


class Issues(Resource):
    def get(self):
        return fetch_issues(request.headers.get("Authorization"), request.args)


class Roadmaps(Resource):
    def get(self):
        return get_roadmaps(request.headers.get("Authorization"), request.args)


class RoadmapObjectives(Resource):
    def get(self):
        return get_roadmap_objectives(
            request.headers.get("Authorization"), request.args.get("roadmap_key")
        )


class NotificationsRead(Resource):
    def post(self):
        return mark_notifs_as_read(
            request.headers.get("Authorization"), request.args.get("reset")
        )


class TokenDetails(Resource):
    def get(self):
        return fetch_token_details(
            request.headers.get("Authorization"), request.args.get("token_symbol")
        )


class ListTokens(Resource):
    def get(self):
        return fetch_token_list(request.headers.get("Authorization"))


class FetchJWT(Resource):
    def post(self):
        body = request.get_json()
        return generate_jwt(
            body.get("github_id"),
            body.get("firebase_uid"),
            body.get("user_gh_access_token"),
            body.get("pub_key"),
        )


class SanityCheck(Resource):
    def get(self):
        return make_response(jsonify({"Status": "API is reachable"}), 200)


class ProfileContributions(Resource):
    def get(self):
        return profile_contributions(request.headers.get("Authorization"))


class PortfolioGenerator(Resource):
    def post(self):
        return generate_portfolio_website(
            request.headers.get("Authorization"), request.args.get("website_type")
        )


class HomepageAPI(Resource):
    def get(self):
        return fetch_homepage(request.headers.get("Authorization"))


class UpdateProgress(Resource):
    def post(self):
        return update_user_progress(
            request.headers.get("Authorization"),
            request.args.get("progress_type"),
            request.args.get("progress_title"),
        )


class ProjectsMinified(Resource):
    def get(self):
        return fetch_projects_minified(request.headers.get("Authorization"))


class JobsPreSignups(Resource):
    def post(self):
        return add_to_waitlist(request.args.get("email"), request.args.get("wl_type"))


class RoadmapProjects(Resource):
    def get(self):
        return get_roadmap_projects(
            request.headers.get("Authorization"), request.args.get("project_id")
        )


class Mixpanel(Resource):
    def get(self, path):
        return api_request(path, request)

    def post(self, path):
        return api_request(path, request)


api.add_resource(Notifications, "/notifications")
api.add_resource(NotificationsRead, "/notifications/read")
api.add_resource(Projects, "/projects")
api.add_resource(ProjectsMinified, "/projects/minified")
api.add_resource(Issues, "/issues")
api.add_resource(Roadmaps, "/roadmaps")
api.add_resource(RoadmapObjectives, "/roadmaps/objectives")
api.add_resource(ProfileContributions, "/profile/contributions")
api.add_resource(PortfolioGenerator, "/profile/portfolio")
api.add_resource(TokenDetails, "/swap/profile")
api.add_resource(ListTokens, "/swap/list")
api.add_resource(FetchJWT, "/user/setup")
api.add_resource(SanityCheck, "/")
api.add_resource(HomepageAPI, "/home")
api.add_resource(UpdateProgress, "/progress/new")
api.add_resource(JobsPreSignups, "/waitlist/jobs")
api.add_resource(Tokens, "/tokens")
api.add_resource(RoadmapProjects, "/roadmaps/project")
api.add_resource(Mixpanel, "/mixpanel/proxy/<path>")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)

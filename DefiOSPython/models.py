from mongoengine import Document, IntField, StringField, URLField, DictField
from mongoengine import EmbeddedDocument, DateTimeField, ReferenceField, DynamicField
from mongoengine import BooleanField, FloatField, ListField, EmbeddedDocumentListField
from mongoengine import EmailField
from bson import ObjectId
from datetime import datetime

default_token_dict = {
    "token_spl_addr": "E1r1HeJdpNuAfKDyBXoLG3i79cTretrCHoXWhhSKGUPt",
    "token_symbol": "ITD",
    "token_name": "ItadakimasuDollar",
    "token_image_url": "https://ipfs.io/ipfs/QmZDH8LNFytG1YaMHcAaBEMFgAK56HCd2vbuTqwbvB1thN",
}


class Token(Document):
    token_name = StringField()
    token_spl_addr = StringField()
    token_symbol = StringField()
    token_image_url = URLField()
    token_price_feed = URLField()
    token_ltp = FloatField()
    token_ltp_24h_change = FloatField()
    token_total_supply = IntField()
    token_circulating_supply = IntField()
    token_creator_name = StringField()
    token_creation_date = DateTimeField()
    token_repository_link = URLField()
    meta = {"collection": "tokens"}


class RoadmapObjective(EmbeddedDocument):
    objective_title = StringField(required=True)
    objective_creation_date = DateTimeField()
    objective_creator_gh_name = StringField()
    objective_creator_gh_profile_pic = URLField()
    objective_deliverable = StringField(
        choices=["Infrastructure", "Tooling", "Publication", "Product", "Other"]
    )
    objective_state = StringField(
        choices=["Locked", "InProgress", "Closed", "Deprecated"]
    )
    objective_start_date = DateTimeField()
    objective_end_date = DateTimeField()


class Roadmap(Document):
    roadmap_creator_gh = StringField()
    roadmap_creator_gh_profile_url = URLField()
    roadmap_creator_gh_name = StringField(required=True, default="")
    roadmap_cover_img_url = URLField()
    roadmap_total_stake = FloatField()
    roadmap_active_objectives = IntField()
    roadmap_outcome_types = ListField(
        StringField(
            choices=["Infrastructure", "Tooling", "Publication", "Product", "Other"]
        )
    )
    roadmap_objectives_list = EmbeddedDocumentListField(RoadmapObjective)
    roadmap_objectives_graph = DictField()
    roadmap_creation_date = DateTimeField()
    roadmap_title = StringField()
    roadmap_outlook = StringField(
        required=True,
        default="Next 2 Yrs",
        choices=[
            "Next 2 Yrs",
            "Long-Term Public Good",
            "Next 5 Yrs",
            "More than 5 Yrs",
        ],
    )

    def to_roadmap_json(self):
        return {
            "title": self.roadmap_title,
            "creation_date": datetime.strftime(
                self.roadmap_creation_date, "%Y-%m-%dT%H:%M:%s"
            ),
            "creator": self.roadmap_creator_gh,
            "creator_profile_pic": self.roadmap_creator_gh_profile_url,
            "creator_name": self.roadmap_creator_gh_name,
            "total_stake": self.roadmap_total_stake,
            "cover_image": self.roadmap_cover_img_url,
            "active_objectives": self.roadmap_active_objectives,
            "outcomes": list(set(self.roadmap_outcome_types)),
        }


class Contributions(EmbeddedDocument):
    contribution_type = StringField(required=True, choices=["inbound", "outbound"])
    contributor_github = StringField(required=True)
    contribution_link = URLField(required=True)
    contribution_timestamp = DateTimeField(required=True)
    contributor_project_id = StringField(required=True)
    contributor_project_name = StringField(required=True)
    contribution_amt = FloatField()
    contribution_token_symbol = StringField()
    contribution_token_icon = URLField()


class ProgressItem(EmbeddedDocument):
    progress_type = StringField(
        required=True, choices=["developer", "maintainer", "enterprise"]
    )
    progress_text = StringField(required=True)
    progress_true = BooleanField(required=True, default=False)


class Users(Document):
    user_github = StringField(required=True)
    user_phantom_address = StringField()
    user_fb_uid = StringField(required=True)
    user_gh_name = StringField()
    user_profile_pic = URLField()
    user_contributions = EmbeddedDocumentListField(Contributions)
    user_progress = EmbeddedDocumentListField(ProgressItem)

    def fetch_contributions(self):
        contributions = self.to_mongo().to_dict()["user_contributions"]
        contributors = [i["contributor_github"] for i in contributions]
        contributors_data = Users.objects(user_github__in=contributors).only(
            "user_github", "user_gh_name", "user_profile_pic"
        )
        contributors_data = {i.user_github: i for i in contributors_data}

        for contribution in contributions:
            token = Token.objects(
                token_symbol=contribution["contribution_token_symbol"]
            ).first()
            contribution["token_spl_addr"] = token.token_spl_addr
            contribution["token_image_url"] = token.token_image_url
            contribution["contributor_name"] = contributors_data[
                contribution["contributor_github"]
            ].user_gh_name
            contribution["contributor_profile_pic"] = contributors_data[
                contribution["contributor_github"]
            ].user_profile_pic

        return contributions


class IssuePRs(EmbeddedDocument):
    issue_pr_account = StringField()
    issue_pr_author = StringField()
    issue_pr_link = URLField()
    issue_originality_score = IntField()
    issue_author_github = StringField()
    issue_title = StringField()
    issue_vote_amount = IntField()
    issue_pr_github = StringField()


class Issues(Document):
    issue_account = StringField()
    issue_creator_gh = StringField()
    issue_project_id = StringField()
    issue_project_name = StringField()
    issue_title = StringField()
    issue_state = StringField(choices=["open", "voting", "winner_declared", "closed"])
    issue_summary = StringField()
    issue_gh_url = URLField()
    issue_stake_amount = FloatField()
    issue_stake_token_symbol = StringField()
    issue_stake_token_url = URLField()
    issue_prs = EmbeddedDocumentListField(IssuePRs)
    issue_tags = ListField(StringField())
    rewardee = StringField()

    def parse_to_json(self):
        issue_json = self.to_mongo().to_dict()
        issue_json["_id"] = str(issue_json["_id"])
        return issue_json


class Projects(Document):
    project_account = StringField()
    project_owner_github = StringField()
    project_token = ReferenceField(Token)
    project_status = StringField(choices=["Secure", "Vulnerable", "Broken"])
    project_name = StringField()
    project_repo_link = URLField()
    top_supporter_name = StringField()
    top_supporter_address = StringField()
    top_builder_name = StringField()
    top_builder_address = StringField()
    num_open_issues = IntField()
    community_health = IntField()
    community_health_graph = URLField()
    num_contributions = IntField()
    num_contributions_chg_perc = FloatField()
    num_contributions_graph = URLField()
    is_token_native = BooleanField()
    internal_tags = DynamicField()
    coins_staked = FloatField(default=0)
    coins_rewarded = FloatField(default=0)
    claimers_pending = ListField(StringField())

    def parse_to_json(self, github_id=""):
        project_json = self.to_mongo().to_dict()
        project_json["_id"] = str(project_json["_id"])
        project_json["project_token"] = (
            default_token_dict
            if self.project_token is None
            else self.project_token.to_mongo().to_dict()
        )
        if github_id in project_json["claimers_pending"]:
            project_json["claimable"] = True
        else:
            project_json["claimable"] = False
        project_json["coins_staked"] = self.coins_staked
        project_json["coins_rewarded"] = self.coins_rewarded
        if "_id" in project_json["project_token"]:
            del project_json["project_token"]["_id"]
        return project_json


class Notifications(Document):
    reciever = StringField()
    sender_id = StringField(required=True)
    sender_name = StringField(required=True)
    sender_profile_pic = StringField()
    notif_post_time = DateTimeField()
    notif_type = StringField()
    notif_content = StringField()
    notif_action_path = StringField(required=True, default="/")
    notif_action_state_params = DictField()
    notif_action_api_params = DictField()
    notif_read_status = BooleanField(required=True, default=False)


class Waitlist(Document):
    waitlist_email = EmailField()
    waitlist_type = StringField(choices=["jobs", "enterprise"])

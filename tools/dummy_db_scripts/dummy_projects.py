import mongoengine
from DefiOSPython.models import Token, Projects
import random

mongoengine.connect("DefiOS")

token = Token.objects(token_ltp__exists=True).all()

project_statuses = ["Secure", "Vulnerable", "Broken"]
project_name = ["DefiOS Legacy Frontend", "MusicProX", "FitBro"]
project_repo_link = [
    "https://github.com/AbhisekBasu1/DefiOS",
    "https://github.com/Rohitkk432/Music-Pro-X",
    "https://github.com/Rohitkk432/FitBro",
]
top_supporters = [
    {"name": "Rohitkk432", "address": "81sWMLg1EgYps3nMwyeSW1JfjKgFqkGYPP85vTnkFzRn"},
    {
        "name": "prasannkumar1263",
        "address": "EyarH752DNqzXBLGXJV8ciJQzo8xdZAnFeJFjksWTcaq",
    },
    {"name": "AbhisekBasu1", "address": "81sWMLg1EgYps3nMwyeSW1JfjKgFqkGYPP85vTnkFzRn"},
]

top_builders = [
    {
        "name": "MayankMittal1",
        "address": "81sWMLg1EgYps3nMwyeSW1JfjKgFqkGYPP85vTnkFzRn",
    },
    {
        "name": "never2average",
        "address": "FV9vFVVv2fTskCd4XhnGDMjdNLvkhxyvD5fwmtsAciEh",
    },
    {"name": "TanmayMunjal", "address": "Fam7Kkoq2jUZFuwxeZuJuNbW3cnSnc4kjW1Xrp3fGCtz"},
]

for i in range(3):
    projects = Projects(
        project_owner_github="74586376",
        project_token=token[random.randint(0, len(token) - 1)],
        project_status=project_statuses[random.randint(0, 2)],
        project_name=project_name[i],
        project_repo_link=project_repo_link[i],
        top_supporter_name=top_supporters[i]["name"],
        top_supporter_address=top_supporters[i]["address"],
        top_builder_name=top_builders[i]["name"],
        top_builder_address=top_builders[i]["address"],
        num_open_issues=random.randint(10, 50),
        community_health=random.randint(10, 50),
        community_health_graph="https://community-health-graph-23.s3.ap-south-1.amazonaws.com/fitbro_community_health_02032023.json",
        num_contributions=random.randint(10, 50),
        num_contributions_chg_perc=float(random.uniform(1.5, 10.5)),
        num_contributions_graph="https://community-health-graph-23.s3.ap-south-1.amazonaws.com/fitbro_community_health_02032023.json",
        is_token_native=random.choice([True, False]),
        internal_tags={},
    )
    projects.save()

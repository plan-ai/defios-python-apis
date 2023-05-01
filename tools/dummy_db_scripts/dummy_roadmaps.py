import mongoengine
from DefiOSPython.models import Roadmap, Users
import random
from datetime import datetime, timedelta

mongoengine.connect("DefiOS")
users = Users.objects.all()

roadmap_creator_gh_list = [
    random.choice([user.user_github for user in users]) for i in range(5)
]

roadmap_creator_gh_profile_url_list = [
    [j for j in users if j.user_github == i][0].user_profile_pic
    for i in roadmap_creator_gh_list
]

roadmap_cover_img_url_list = [
    "https://foresight.org/wp-content/uploads/2022/10/Nanotechb.jpg",
    "https://foresight.org/wp-content/uploads/2022/10/biotech-2022-horizontal.jpg",
    "https://foresight.org/wp-content/uploads/2022/10/computerb.jpg",
    "https://foresight.org/wp-content/uploads/2022/10/neurob.jpg",
    "https://foresight.org/wp-content/uploads/2022/10/spaceb.jpg",
]

roadmap_title_list = [
    "Molecular Machines Group",
    "Biotech & Health Extension",
    "Computation: Intelligent Cooperation",
    "Neurotech: Improving Cognition",
    "Space: Expanding Outward",
]


for i in range(5):
    roadmap = Roadmap(
        roadmap_creator_gh=roadmap_creator_gh_list[i],
        roadmap_creator_gh_profile_url=roadmap_creator_gh_profile_url_list[i],
        roadmap_cover_img_url=roadmap_cover_img_url_list[i],
        roadmap_total_stake=random.uniform(400, 800),
        roadmap_active_objectives=random.randint(20, 30),
        roadmap_outcome_types=[
            random.choice(
                ["Infrastructure", "Tooling", "Publication", "Product", "Other"]
            )
            for i in range(random.randint(2, 7))
        ],
        roadmap_creation_date=datetime.now() - timedelta(hours=random.randint(20, 50)),
        roadmap_title=roadmap_title_list[i],
    )
    roadmap.save()

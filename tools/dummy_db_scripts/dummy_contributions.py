from DefiOSPython.models import Contributions, Users, Projects, Token
import random
from datetime import datetime, timedelta
import mongoengine

mongoengine.connect("DefiOS")

users = Users.objects.all()
projects = Projects.objects.only("project_name").all()
project_ids = [str(i.id) for i in projects]
project_names = [i.project_name for i in projects]
token = Token.objects.only("token_symbol", "token_image_url").all()
token_symbols = [i.token_symbol for i in token]
token_image_url = [i.token_image_url for i in token]
token_data = []
for i in range(10):
    k = random.randint(0, len(token_symbols) - 1)
    token_data.append([token_symbols[k], token_image_url[k]])


contributions = [
    Contributions(
        contribution_type=random.choice(["inbound", "outbound"]),
        contributor_github=random.choice([i.user_github for i in users]),
        contribution_link="https://github.com/OnFinance/onfinance_db_model_master/pull/{}".format(
            1, 23
        ),
        contribution_timestamp=datetime.now() - timedelta(days=random.randint(4, 10)),
        contributor_project_id=random.choice(project_ids),
        contributor_project_name=random.choice(project_names),
        contribution_amt=random.uniform(100, 500),
        contribution_token_symbol=token_data[i][0],
        contribution_token_icon=token_data[i][1],
    )
    for i in range(10)
]

for user in users:
    user.update(set__user_contributions=contributions)

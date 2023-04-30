from models import ProgressItem, Users
import mongoengine

mongoengine.connect("DefiOS")


users = Users.objects.all()


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


for user in users:
    set_progress_init(user)

import mongoengine
from DefiOSPython.models import Token, Issues, IssuePRs
import random

mongoengine.connect("DefiOS")

issues_titles_list = [
    "Add documentation to DefiOS API",
    "Implement 'Create Roadmap' button functionality",
    "Allow users to unstake tokens from roadmap objectives",
    "Integrate GitLab logins",
    "Allow users to Import new Initial Fair Distribution algorithms",
]

issue_creator_gh = "74586376"

issue_project_name_list = [
    random.choice(["FitBro", "MusicProX", "'DefiOS Legacy Frontend'"]) for i in range(5)
]

issue_state_list = ["open", "voting", "winner_declared", "closed", "open"]

issue_project_id_list = [
    random.choice(
        [
            "64042d3ab0f1a2216e23e5e1",
            "64042d3bb0f1a2216e23e5e2",
            "64042d3bb0f1a2216e23e5e3",
        ]
    )
    for i in range(5)
]

issue_summary_list = [
    "The login button is unresponsive when attempting to log in from their mobile devices. This issue seems to be specific to devices with smaller screens, as the button works fine on larger screens. We need to investigate and fix this issue as soon as possible to ensure that all users can log in from their mobile devices.",
    "Some of the images on the homepage are not loading properly. This issue seems to be intermittent and affects users across different browsers and devices. We need to identify the root cause of the issue and implement a fix to ensure that all images are loaded properly on the homepage.",
    "One of the links in the footer menu is broken and leads to a 404 error page. The link in question is important and needs to be fixed as soon as possible. We need to identify the correct URL for the link and update it in the footer menu.",
    "Product pages are taking a long time to load, especially when they contain a large number of images or videos. This issue seems to be affecting users across different browsers and devices. We need to optimize the product pages to improve loading times and provide a better user experience.",
    "The pricing information displayed on the checkout page is incorrect, and they are being charged a higher amount than they expected. We need to investigate the issue and identify the root cause of the problem. Once we have identified the issue, we need to update the pricing information on the checkout page to ensure that users are not overcharged.",
]

issue_prs_list = [
    [
        IssuePRs(
            issue_pr_author=random.choice(
                [
                    "Rohitkk432",
                    "MayankMittal1",
                    "never2average",
                    "AbhisekBasu1",
                    "sameshl",
                ]
            ),
            issue_pr_link="https://github.com/OnFinance/onfinance_db_model_master/pull/22",
            issue_originality_score=random.randint(50, 100),
            issue_author_github="https://github.com/never2average",
            issue_title=i,
            issue_vote_amount=random.randint(100, 1000),
        )
        for i in [
            "Fix mobile login button click event on smaller screens",
            "Update CSS styles for mobile login button to ensure responsiveness",
            "Add additional event listeners for mobile login button to improve user experience",
        ]
    ],
    [
        IssuePRs(
            issue_pr_author=random.choice(
                [
                    "Rohitkk432",
                    "MayankMittal1",
                    "never2average",
                    "AbhisekBasu1",
                    "sameshl",
                ]
            ),
            issue_pr_link="https://github.com/OnFinance/onfinance_db_model_master/pull/22",
            issue_originality_score=random.randint(50, 100),
            issue_author_github="https://github.com/never2average",
            issue_title=i,
            issue_vote_amount=random.randint(100, 1000),
        )
        for i in [
            "Optimize image file sizes to improve page load times",
            "Use lazy loading technique to improve loading times for images below the fold",
            "Implement fallback image sources to ensure all images load successfully",
        ]
    ],
    [
        IssuePRs(
            issue_pr_author=random.choice(
                [
                    "Rohitkk432",
                    "MayankMittal1",
                    "never2average",
                    "AbhisekBasu1",
                    "sameshl",
                ]
            ),
            issue_pr_link="https://github.com/OnFinance/onfinance_db_model_master/pull/22",
            issue_originality_score=random.randint(50, 100),
            issue_author_github="https://github.com/never2average",
            issue_title=i,
            issue_vote_amount=random.randint(100, 1000),
        )
        for i in [
            "Update footer link URL to correct destination",
            "Test and verify footer link works on all browsers and devices",
            "Implement a link monitoring tool to detect and fix broken links in the future",
        ]
    ],
    [
        IssuePRs(
            issue_pr_author=random.choice(
                [
                    "Rohitkk432",
                    "MayankMittal1",
                    "never2average",
                    "AbhisekBasu1",
                    "sameshl",
                ]
            ),
            issue_pr_link="https://github.com/OnFinance/onfinance_db_model_master/pull/22",
            issue_originality_score=random.randint(50, 100),
            issue_author_github="https://github.com/never2average",
            issue_title=i,
            issue_vote_amount=random.randint(100, 1000),
        )
        for i in [
            "Implement lazy loading for images and videos on product pages",
            "Optimize image file sizes and compress videos to improve loading times",
            "Utilize a content delivery network (CDN) to improve page load times for users in different geographic locationse",
        ]
    ],
    [
        IssuePRs(
            issue_pr_author=random.choice(
                [
                    "Rohitkk432",
                    "MayankMittal1",
                    "never2average",
                    "AbhisekBasu1",
                    "sameshl",
                ]
            ),
            issue_pr_link="https://github.com/OnFinance/onfinance_db_model_master/pull/22",
            issue_originality_score=random.randint(50, 100),
            issue_author_github="https://github.com/never2average",
            issue_title=i,
            issue_vote_amount=random.randint(100, 1000),
        )
        for i in [
            "Update pricing calculations on checkout page to ensure accuracy",
            "Implement a validation step to confirm correct pricing before charging users",
            "Add unit tests to validate correct pricing calculations for different scenarios",
        ]
    ],
]

issue_tags_list = [
    [
        random.choice(
            [
                "bug",
                "documentation",
                "urgent",
                "feature request",
                "update needed",
                "good first issue",
            ]
        )
        for j in range(random.randint(2, 5))
    ]
    for i in range(5)
]

issue_gh_url = "https://github.com/never2average/Git2DAO/issues/1"
issue_stake_amount_list = [random.uniform(5400, 8000) for i in range(5)]

tokens = Token.objects.only("token_symbol", "token_image_url").all()
token_symbols = [i.token_symbol for i in tokens]
token_urls = [i.token_image_url for i in tokens]

issue_stake_token_symbol_list = [random.choice(token_symbols) for i in range(5)]
issue_stake_token_url_list = [random.choice(token_urls) for i in range(5)]


for idx in range(5):
    issue = Issues(
        issue_creator_gh=issue_creator_gh,
        issue_project_id=issue_project_id_list[idx],
        issue_project_name=issue_project_name_list[idx],
        issue_title=issues_titles_list[idx],
        issue_state=issue_state_list[idx],
        issue_summary=issue_summary_list[idx],
        issue_gh_url=issue_gh_url,
        issue_stake_amount=issue_stake_amount_list[idx],
        issue_stake_token_symbol=issue_stake_token_symbol_list[idx],
        issue_stake_token_url=issue_stake_token_url_list[idx],
        issue_prs=issue_prs_list[idx],
        issue_tags=issue_tags_list[idx],
    )
    issue.save()

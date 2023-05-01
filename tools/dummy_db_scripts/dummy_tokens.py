from DefiOSPython.models import Tokens
from datetime import datetime, timedelta
import random
import mongoengine

mongoengine.connect("DefiOS")


token_names = ["USDT", "Wrapped SOL", "Wrapped Bitcoin (Sollet)"]
token_spl_addresses = [
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    "So11111111111111111111111111111111111111112",
    "9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E",
]
token_symbols = ["USDT", "SOL", "BTC"]
token_image_urls = [
    "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB/logo.svg",
    "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png",
    "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E/logo.png",
]
token_ltps = [random.uniform(4, 100) for i in range(3)]
token_ltp_24h_change = [random.random() for i in range(3)]
token_total_supply = [random.randint(100000, 1000000) for i in range(3)]
token_circulating_supply = [
    random.randint(int(0.5 * token_total_supply[i]), int(0.9 * token_total_supply[i]))
    for i in range(3)
]
token_creator_name = [
    "Q6XprfkF8RQQKoQVG33xT88H7wi8Uk1B1CC7YAs69Gi",
    "AqH29mZfQFgRpfwaPoTMWSKJ5kqauoc1FwVBRksZyQr",
    "6krMGWgeqD4CySfMr94WcfcVbf2TrMzfshAk5DcZ7mbu",
]
token_creation_date = [
    datetime.now() - timedelta(days=random.randint(3, 10)) for i in range(3)
]

for i in range(3):
    token = Tokens(
        token_name=token_names[i],
        token_spl_addr=token_spl_addresses[i],
        token_symbol=token_symbols[i],
        token_price_feed="https://token-price-charts.s3.ap-south-1.amazonaws.com/USDC_price.json",
        token_image_url=token_image_urls[i],
        token_ltp=token_ltps[i],
        token_ltp_24h_change=token_ltp_24h_change[i],
        token_total_supply=token_total_supply[i],
        token_circulating_supply=token_circulating_supply[i],
        token_creator_name=token_creator_name[i],
        token_creation_date=token_creation_date[i],
        token_repository_link="https://github.com/never2average/",
    )
    token.save()

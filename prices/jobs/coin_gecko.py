# prices/tasks.py
from datetime import datetime
import requests
from celery import shared_task

from prices.models import DataSources
from prices.models import PriceRecords


@shared_task
def fetch_coin_gecko_data():
    source = DataSources.objects.get(key='CoinGecko')
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

    try:
        if not source:
            raise Exception('Data source not found')
        response = requests.get(url)
        response.raise_for_status()  # will raise an exception for HTTP error codes
        data = response.json()

        # Extract price for Ethereum in USD
        eth_price = data.get('ethereum', {}).get('usd')
        if eth_price:
            PriceRecords.objects.create(
                symbol='ETH',
                price_decimal=eth_price,
                price_raw=str(eth_price),
                timestamp=datetime.now(),
                source=source,
            )
    except requests.RequestException as e:
        # Log an error message or send an alert
        print(e)

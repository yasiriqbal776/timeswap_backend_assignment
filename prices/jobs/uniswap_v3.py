# prices/tasks.py
import os
from datetime import datetime
import requests
from celery import shared_task
from web3 import Web3

from assignment import settings
from prices.models import DataSources
from prices.models import PriceRecords
from decimal import Decimal, getcontext


@shared_task
def fetch_data(source_id):

    try:
        source = DataSources.objects.get(id=2)

        if not source:
            raise Exception('Data source not found')
        web3 = Web3(Web3.HTTPProvider(settings.ETH_MAINNET_RPC))

        # :TODO - Load contract address dynamically using either source or new table.
        usdc_weth_pool_v3 = '0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640'

        #: TODO - Place ABI in separate file instead of hard coded
        pool_abi = [{"inputs": [], "name": "slot0",
                    "outputs": [{"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
                                {"internalType": "int24", "name": "tick", "type": "int24"},
                                {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
                                {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
                                {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
                                {"internalType": "uint8", "name": "feeProtocol", "type": "uint8"},
                                {"internalType": "bool", "name": "unlocked", "type": "bool"}],
                    "stateMutability": "view", "type": "function"}]

        pool_contract = web3.eth.contract(address=usdc_weth_pool_v3, abi=pool_abi)

        slot0 = pool_contract.functions.slot0().call()

        sqrt_price_x96 = slot0[0]

        factor_token_0 = Decimal(10) ** 6
        factor_token_1 = Decimal(10) ** 18

        price_squared = sqrt_price_x96 ** 2

        price_adjusted = price_squared * factor_token_0 / factor_token_1
        final_price_usdc_per_eth = price_adjusted / (Decimal(2) ** Decimal(192))

        final_price_eth_to_usdc = Decimal(1) / final_price_usdc_per_eth

        latest_block = web3.eth.get_block('latest')
        PriceRecords.objects.create(
            symbol='ETH',
            price_decimal=final_price_eth_to_usdc,
            price_raw=str(slot0[0]),
            block_no=latest_block.number,
            timestamp=datetime.now(),
            source=source,
        )
    except requests.RequestException as e:
        # Log an error message or send an alert
        print(e)

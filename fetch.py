#!/usr/bin/env python

import requests
from datetime import datetime
from requests.exceptions import HTTPError
from lxml import html


SLACK_TOKEN = 'changeme'
SLACK_CHANNEL = 'changeme'


def send_to_slack(message):
    print("Found CPU: ", message)
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': SLACK_TOKEN,
        'channel': SLACK_CHANNEL,
        'text': message,
    }).json()


def canada_computers():
    try:
        url = "https://www.canadacomputers.com/product_info.php?ajaxstock=true&itemid=183430"

        payload = {}
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.canadacomputers.com/product_info.php?cPath=4_64&item_id=183430',
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()

        if "NO AVAILABLE" not in jsonResponse.values():
            send_to_slack('Canada computers: https://www.canadacomputers.com/product_info.php?cPath=4_64&item_id=183430')

        if 0 not in jsonResponse.values():
            send_to_slack('Canada computers: https://www.canadacomputers.com/product_info.php?cPath=4_64&item_id=183430')

    except HTTPError as http_err:
        print(http_err)
    except Exception as err:
        print(err)


def memory_express():
    try:
        url = "https://www.memoryexpress.com/Products/MX00114451"

        response = requests.get(url)
        tree = html.fromstring(response.content)

        stock_for_stores = tree.xpath('//span[@class="c-capr-inventory-store__availability InventoryState_InStock"]/text()')

        if len(stock_for_stores) > 0:
            send_to_slack('memory express: https://www.memoryexpress.com/Products/MX00114451')

    except HTTPError as http_err:
        print(http_err)
    except Exception as err:
        print(err)


def newegg():
    try:
        url = "https://www.newegg.ca/amd-ryzen-9-5900x/p/N82E16819113664?Description=5900x&cm_re=5900x-_-19-113-664-_-Product"

        response = requests.get(url)
        tree = html.fromstring(response.content)

        stock_for_stores = tree.xpath('//button[@title="Add AMD Ryzen 9 5900X 12-Core 3.7 GHz Socket AM4 105W 100-100000061WOF Desktop Processor to cart"]/text()')
        # access JSOn content
        if len(stock_for_stores):
            send_to_slack('newegg: https://www.newegg.ca/amd-ryzen-9-5900x/p/N82E16819113664?Description=5900x&cm_re=5900x-_-19-113-664-_-Product')

    except HTTPError as http_err:
        print(http_err)
    except Exception as err:
        print(err)


canada_computers()
memory_express()
newegg()
print("script ran at: ", datetime.now())

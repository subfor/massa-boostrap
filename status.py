"""
This script must be run on your Node
    Example run script every 5 minutes:
    Install to cron to run every 5(o) min (on Ubuntu example):
    srcipt dir: /root/scripts
    cd /root/scripts
    chmod +x status.py
    crontab -e
    select nano (easiest way) if asked
    add this line
    */5 * * * * /usr/bin/python3 /root/scripts/status.py > /dev/null 2>&1
    press ctrl+X and safe changes

"""

from os import system
from time import sleep

import requests

IP = "127.0.0.1"
"""
IP = ip address your node or any other public node.
If script run on node -  IP = "127.0.0.1" 
"""

WALLET_ADDRESS = ""
MASSA_PASSWD = ""
"""Massa wallet address and password"""

API_TOKEN = ""
CHAT_ID = ""
"""
API_TOKEN you can get with @BotFather when creating bot
CHAT_ID you can get it this way:
1) Go to bot and send /start
2) Send anything to bot
3) In browser go https://api.telegram.org/bot_API_TOKEN_/getUpdates
example "https://api.telegram.org/bot534238456:AAHbl_s-sr3FR6TxWGLeuxN5EfGQefwegasfgg/getUpdates"
"""
API_URL = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'


def send_to_telegram(message):
    try:
        response = requests.post(API_URL, json={'chat_id': CHAT_ID, 'text': message})
    except Exception as e:
        return e


def get_response(json_data: dict):
    try:
        response = requests.post(f"http://{IP}:33035", json=json_data)
    except requests.ConnectionError:
        return None
    return response


def get_wallet_info():
    json_data = {"id": "1", "jsonrpc": "2.0", "method": "get_addresses",
                 "params": [[f"{WALLET_ADDRESS}"]]}

    response = get_response(json_data=json_data)

    if response:
        final_rolls = response.json().get('result')[0].get('final_roll_count')
        candidate_rolls = response.json().get('result')[0].get('candidate_roll_count')
        active_rolls = response.json().get('result')[0].get('cycle_infos')[-1].get('active_rolls')
        balance = float(response.json().get('result')[0].get('final_balance'))

        return active_rolls, final_rolls, candidate_rolls, balance


if __name__ == '__main__':

    active_rolls, _, candidate_rolls, balance = get_wallet_info()

    if active_rolls == 0 and candidate_rolls == 0:
        send_to_telegram(f"Alert !!! Active Rolls: {active_rolls}")
        if balance < 100:
            send_to_telegram(f"Not enough balance {balance} , can't buy roll")
        else:
            system(
                f"cd /root/massa/massa-client && ./massa-client -p {MASSA_PASSWD} buy_rolls {WALLET_ADDRESS} 1 0 >> /root/status.log")

            sleep(30)

            active_rolls, final_rolls, candidate_rolls, _ = get_wallet_info()
            send_to_telegram(f"Roll purchased successfully! \n Active Rolls: {active_rolls}\n Rolls: {final_rolls}\n "
                             f"Candidate Rolls: {candidate_rolls}")

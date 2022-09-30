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

import requests
import json

IP = "127.0.0.1"
"""
IP = ip address your node or any other public node.
If script run on node -  IP = "127.0.0.1" 
"""

address = "A127LPgaKbBVHov5Zs8Qu1TiYYAndC2qpJf15x2zD57q4ekYom4D"
"""Massa wallet address"""

apiToken = '5341188078:AAHbl_s-sr3FR6TxWGLeuxN5EfGQKXpZjOc'
chatID = '232571704'
"""
apiToken you can get with @BotFather when creating bot
chatID you can get this way:
1) Go to bot and send /start
2) Send anything to bot
3) In browser go https://api.telegram.org/bot_API_TOKEN_/getUpdates
example "https://api.telegram.org/bot534238456:AAHbl_s-sr3FR6TxWGLeuxN5EfGQefwegasfgg/getUpdates"
"""
apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'


def send_to_telegram(message):
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
    except Exception as e:
        return e


def get_response(json_data: dict):
    try:
        response = requests.post(f"http://{IP}:33035", json=json_data)
    except requests.ConnectionError:
        return None
    return response


if __name__ == '__main__':

    json_data = {"id": "1", "jsonrpc": "2.0", "method": "get_addresses",
                 "params": [["A127LPgaKbBVHov5Zs8Qu1TiYYAndC2qpJf15x2zD57q4ekYom4D"]]}

    resp = get_response(json_data=json_data)
    rolls = resp.json().get('result')[0].get('final_roll_count')
    candidate_rolls = resp.json().get('result')[0].get('candidate_roll_count')
    active_rolls = resp.json().get('result')[0].get('cycle_infos')[-1].get('active_rolls')
    balance = float(resp.json().get('result')[0].get('final_sequential_balance'))

    # print(resp.json())
    print(json.dumps(resp.json(), indent=4))
    print(f"Rolls: {rolls} {type(rolls)}")
    print(f"Candidate Rolls: {candidate_rolls} {type(candidate_rolls)}")
    print(f"Active Rolls: {active_rolls} {type(active_rolls)}")
    print(f"Balance: {balance} {type(balance)}")
    data = (f"Rolls: {rolls} Balance: {balance}")

    print("=================================")

    if active_rolls == 1 and candidate_rolls == 2:
        send_to_telegram(f"Alert !!! Active Rolls: {active_rolls}")
        if balance < 100:
            send_to_telegram(f"Not enough balance {balance} , can't buy roll")
        else:
            system(
                f"cd /root/massa/massa-client && ./massa-client -p Qwqd32dasxq23rd buy_rolls {address} 1 0 >> /root/status.log")
            send_to_telegram(f"Roll purchased successfully! \n Active Rolls: {active_rolls}\n Rolls: {rolls}\n "
                             f"Candidate Rolls: {candidate_rolls}")

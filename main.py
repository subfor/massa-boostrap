from os import path

import requests
import pingparsing
import click

IP = "127.0.0.1"
"""
IP = ip address of your node or any other public node.
If script run on node -  IP = "127.0.0.1" 
"""


def get_response():
    try:
        response = requests.post(f"http://{IP}:33035", json={"jsonrpc": "2.0", "method": "get_status", "id": "1"})
    except requests.ConnectionError:
        return None
    return response


def check_ping(ip: str):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = ip
    transmitter.count = 5
    result = transmitter.ping()
    avg_ping = ping_parser.parse(result).as_dict().get('rtt_avg')
    return avg_ping


def main():
    print(f"Fetching list of nodes from {IP}")
    response = get_response()
    if response:
        nodes = response.json().get('result').get('connected_nodes')

        with click.progressbar(nodes.values(), label='Checking latency ') as bar:
            for value in bar:
                avg_speed = check_ping(value[0])
                value.append(avg_speed)

        cleaned_nodes = {k: v for k, v in nodes.items() if v[-1]}
        sorted_nodes = dict(sorted(cleaned_nodes.items(), key=lambda item: item[1][-1]))
        list_nodes = [[k, v[0]] for k, v in sorted_nodes.items()]

        with open(path.join('bootstrap_list.txt'), "w") as txt_file:
            txt_file.write(f"bootstrap_list = [\n")
            for node in list_nodes:
                txt_file.write(f'  ["{node[1]}:31245", "{node[0]}"],\n')
            txt_file.write("]")
        print("Done!")
    else:
        print("Can't connect")


if __name__ == '__main__':
    main()

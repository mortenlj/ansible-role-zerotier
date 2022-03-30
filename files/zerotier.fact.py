#!/usr/bin/env python3

import dataclasses
import json
import subprocess
import sys


@dataclasses.dataclass
class Network:
    status: str
    device: str


def get_node_id():
    cmd = ["zerotier-cli", "-j", "info"]
    data = call_zerotier(cmd)
    return data["address"]


def call_zerotier(cmd):
    try:
        result = subprocess.run(cmd, encoding="utf-8", check=True, capture_output=True)
        data = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to execute zerotier-cli. Are you sure you are running this as root? The error was: %s", e.output)
        sys.exit(1)
    return data


def generate_networks():
    cmd = ["zerotier-cli", "-j", "listnetworks"]
    for network in call_zerotier(cmd):
        yield network['id'], Network(network['status'], network['portDeviceName'])


def main():
    result = {
        "node_id": get_node_id(),
        "networks": {network_id: dataclasses.asdict(n) for (network_id, n) in generate_networks()}
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    main()

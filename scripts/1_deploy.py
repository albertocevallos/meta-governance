from brownie import (
    convert,
    accounts,
    network,
    interface,
    MetaGovernance
)
import os
import sys
import signal
from datetime import datetime
from rich.console import Console
console = Console()


def main():
    # setup
    dev = connect_account()

    owner = dev
    token = '0xD533a949740bb3306d119CC777fa900bA034cd52' # eg. CRV
    name = 'Meta Governance CRV' # Meta Governance + {YOUR_TOKEN}
    symbol = 'metaCRV' # eg. for CRV ecosystem
    tokens = ['0xD533a949740bb3306d119CC777fa900bA034cd52', '0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2'] # eg. CRV, veCRV
    multiples = [1e18, 4e18] # 1 vote == 1e18
    isLp = [False, False]

    args = (owner, token, name, symbol, tokens, multiples, isLp)

    # deploy
    governance = deploy_governance(dev, args)

    # wireup


def deploy_governance(dev, args):
    (owner, token, name, symbol, tokens, multiples, isLp) = args
    governance_instance = MetaGovernance.deploy(owner, token, name, symbol, tokens, multiples, isLp, {'from': dev})
    console.print('[blue]Meta Governance contract was deployed at: [/blue]', governance_instance.address)
    return governance_instance

def connect_account():
    console.print(f"\nnetwork: {network.show_active()}")
    accts = accounts.load()
    console.print("\n[green]Accounts:[/green]")
    for acct in accts:
        console.print(f"\t{acct}")
    name = input("\nEnter account name: ").strip()
    owner = accounts.load(name)
    return (name, owner)
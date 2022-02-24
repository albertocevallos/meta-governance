from brownie import (
    convert,
    accounts,
    network,
    interface,
    MetaGovernance,
)
import os
import sys
import signal
from datetime import datetime
import click
from rich.console import Console
console = Console()


def main():
    # setup
    # dev = connect_account()
    dev = '0x1A7Acc011811eEa942730757141Dc1E693E491b8'

    owner = dev
    token = '0xD533a949740bb3306d119CC777fa900bA034cd52' # eg. CRV
    name = 'Meta Governance CRV' # Meta Governance + {YOUR_TOKEN}
    symbol = 'metaCRV' # eg. for CRV ecosystem
    tokens = ['0xD533a949740bb3306d119CC777fa900bA034cd52', '0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2'] # eg. CRV, veCRV
    multiples = [1, 1] # 1 vote == 1e18
    isLp = [False, False]

    args = (owner, token, name, symbol, tokens, multiples, isLp)

    # deploy
    governance = deploy_governance(dev, args)

    # test
    user = '0xE5350E927B904FdB4d2AF55C566E269BB3df1941'
    meta = governance.balanceOf(user)
    console.print('[red] Balance of user via contract is: [/red]', meta)

    sum = 0

    tx = interface.ERC20(tokens[0]).balanceOf(user)
    sum += tx
    console.print('[red] Balance of user crv is: [/red]', tx)

    tx = interface.ERC20(tokens[1]).balanceOf(user)
    sum += tx
    console.print('[red] Balance of user vecrv is: [/red]', tx)

    console.print('[red] Balance of sum: [/red]', sum)

    assert sum == meta

    



def deploy_governance(dev, args):
    (owner, token, name, symbol, tokens, multiples, isLp) = args
    governance_instance = MetaGovernance.deploy(owner, token, name, symbol, tokens, multiples, isLp, {'from': dev})
    console.print('[blue]Meta Governance contract was deployed at: [/blue]', governance_instance.address)
    return governance_instance

def connect_account():
    click.echo(f"You are using the '{network.show_active()}' network")
    dev = accounts.load(click.prompt("Account", type=click.Choice(accounts.load())))
    click.echo(f"You are using: 'dev' [{dev.address}]")
    return dev
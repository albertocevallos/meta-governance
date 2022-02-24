import pytest
import brownie
from dotenv import load_dotenv
from enum import Enum
from rich.console import Console

# load environment variables defined in .env
load_dotenv()

console = Console()

@pytest.fixture(scope="module", autouse=True)
def dev():
    return brownie.accounts.at('0x1A7Acc011811eEa942730757141Dc1E693E491b8', force=True)

@pytest.fixture(scope="module", autouse=True)
def owner():
    return brownie.accounts.at('0x0000000000000000000000000000000000000000', force=True)

@pytest.fixture(scope="module", autouse=True)
def valid_user():
    return brownie.accounts.at('0xE5350E927B904FdB4d2AF55C566E269BB3df1941', force=True)

@pytest.fixture(scope="module", autouse=True)
def invalid_user():
    return brownie.accounts[0]


@pytest.fixture(scope="module", autouse=True)
def system(dev, owner, invalid_user):
    # setup
    token = '0xD533a949740bb3306d119CC777fa900bA034cd52' # eg. CRV
    name = 'Meta Governance CRV' # Meta Governance + {YOUR_TOKEN}
    symbol = 'metaCRV' # eg. for CRV ecosystem
    tokens = ['0xD533a949740bb3306d119CC777fa900bA034cd52', '0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2'] # eg. CRV, veCRV
    multiples = [1, 1] # 1 vote == 1e18
    isLp = [False, False]

    args = (owner, token, name, symbol, tokens, multiples, isLp)

    # deploy
    governance = deploy_governance(dev, args)

    # wireup
    wireup = wireup_governance(dev, owner, governance)

def deploy_governance(dev, args):
    (owner, token, name, symbol, tokens, multiples, isLp) = args
    governance_instance = brownie.MetaGovernance.deploy(dev, token, name, symbol, tokens, multiples, isLp, {'from': dev})
    console.print('[blue]Meta Governance contract was deployed at: [/blue]', governance_instance.address)
    return governance_instance

def wireup_governance(dev, owner, governance):
    tx = governance.changeOwner(owner, {'from': dev})
    console.print('System ownership handed over to owener')

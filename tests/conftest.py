import pytest
import boa


@pytest.fixture(scope="module")
def accounts():
    accounts = []
    for _ in range(10):
        addr = boa.env.generate_address()
        boa.env.set_balance(addr, 1 * 10**18)
        accounts.append(addr)
    return accounts


@pytest.fixture(scope="module")
def deployer():
    addr = boa.env.generate_address()
    boa.env.set_balance(addr, 1 * 10**18)
    return addr


@pytest.fixture(scope="module")
def name():
    return "Test Token"


@pytest.fixture(scope="module")
def symbol():
    return "TEST"


@pytest.fixture(scope="module")
def initial_supply():
    return 10_000 * 10**18


@pytest.fixture(scope="module")
def erc20(deployer, name, symbol, initial_supply):
    with boa.env.prank(deployer):
        return boa.load("contracts/ERC20.vy", name, symbol, initial_supply)

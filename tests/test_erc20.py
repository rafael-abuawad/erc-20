import boa


def test_token_name(erc20, name):
    assert erc20.name() == name


def test_token_symbol(erc20, symbol):
    assert erc20.symbol() == symbol


def test_token_decimals(erc20):
    assert erc20.decimals() == 18


def test_token_intial_supply_is_total_supply(erc20, initial_supply):
    assert erc20.totalSupply() == initial_supply


def test_token_deployer_is_minter(erc20, deployer):
    assert erc20.is_minter(deployer)


def test_token_mint(erc20, accounts, deployer, initial_supply):
    total_minted = 0
    for acc in accounts:
        assert erc20.balanceOf(acc) == 0
        mint_amount = 20 * 10**18
        with boa.env.prank(deployer):
            erc20.mint(acc, mint_amount)
        assert erc20.balanceOf(acc) == mint_amount
        total_minted += mint_amount
    expected_total_supply = total_minted + initial_supply
    assert erc20.totalSupply() == expected_total_supply


def test_token_transfer(erc20, deployer, accounts):
    for acc in accounts:
        assert erc20.balanceOf(acc) == 0
        transfer_amount = 20
        initial_deployer_balance = erc20.balanceOf(deployer)
        with boa.env.prank(deployer):
            erc20.transfer(acc, transfer_amount)
        assert erc20.balanceOf(deployer) == initial_deployer_balance - transfer_amount
        assert erc20.balanceOf(acc) == transfer_amount


def test_token_transfer_from(erc20, deployer, accounts):
    user = accounts[0]
    assert erc20.balanceOf(user) == 0

    transfer_amount = 20
    with boa.env.prank(deployer):
        erc20.approve(user, transfer_amount)

    with boa.env.prank(user):
        erc20.transferFrom(deployer, user, transfer_amount)

    assert erc20.balanceOf(user) == transfer_amount

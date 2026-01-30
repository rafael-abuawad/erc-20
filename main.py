import boa


def main():
    name = ""
    symbol = ""
    initial_supply = 0
    contract = boa.load("contracts/ERC20.vy", name, symbol, initial_supply)
    contract.deploy()


if __name__ == "__main__":
    main()

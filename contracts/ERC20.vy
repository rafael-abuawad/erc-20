# pragma version ==0.4.3

name: public(immutable(String[10]))
symbol: public(immutable(String[5]))
decimals: public(constant(uint8)) = 18
totalSupply: public(uint256)
balanceOf: public(HashMap[address, uint256])
allowance: public(HashMap[address, HashMap[address, uint256]])
is_minter: public(HashMap[address, bool])


event Transfer:
    _from: indexed(address)
    _to: indexed(address)
    _value: uint256


event Approve:
    _owner: indexed(address)
    _spender: indexed(address)
    _value: uint256


@deploy
def __init__(_name: String[10], _symbol: String[5], _intial_supply: uint256):
    name = _name
    symbol = _symbol
    self._mint(msg.sender, _intial_supply)
    self.is_minter[msg.sender] = True


@external
def transfer(_to: address, _value: uint256) -> bool:
    assert self.balanceOf[msg.sender] >= _value, "erc20: insufficient balance"
    self.balanceOf[msg.sender] -= _value
    self.balanceOf[_to] += _value
    log Transfer(_from=msg.sender, _to=_to, _value=_value)
    return True


@external
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    assert self.allowance[_from][_to] >= _value, "erc20: insufficient allowance"
    assert self.balanceOf[_from] >= _value, "erc20: insufficient balance"
    self.allowance[_from][_to] -= _value
    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value
    log Transfer(_from=_from, _to=_to, _value=_value)
    return True


@external
def approve(_spender: address, _value: uint256) -> bool:
    self.allowance[msg.sender][_spender] = _value
    log Approve(_owner=msg.sender, _spender=_spender, _value=_value)
    return True


@external
def burn(_value: uint256):
    assert self.balanceOf[msg.sender] >= _value, "erc20: insufficient balance"
    self.balanceOf[msg.sender] -= _value
    self.totalSupply -= _value
    log Transfer(_from=msg.sender, _to=empty(address), _value=_value)


@external
def mint(_to: address, _value: uint256):
    assert self.is_minter[msg.sender], "erc20_mint: caller is not minter"
    self._mint(_to, _value)


@internal
def _mint(_to: address, _value: uint256):
    self.balanceOf[_to] += _value
    self.totalSupply += _value
    log Transfer(_from=empty(address), _to=_to, _value=_value)

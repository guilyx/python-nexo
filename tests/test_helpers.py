import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from nexo.helpers import check_pair_validity

def test_pair_validity_no_slash():
    pair = "BTCUSD"
    assert(check_pair_validity(pair) == False)

def test_pair_validity_valid():
    pair = "BTC/USD"
    assert(check_pair_validity(pair) == True)

def test_pair_validity_too_short():
    pair = "NORMAL/O"
    assert(check_pair_validity(pair) == False)

def test_pair_validity_too_short_but_different():
    pair = "O/NORMAL"
    assert(check_pair_validity(pair) == False)

def test_pair_validity_too_long():
    pair = "MORETHANSIXCHARS/NORMAL"
    assert(check_pair_validity(pair) == False)

def test_pair_validity_too_long_but_different():
    pair = "NORMAL/MORETHANSIXCHARS"
    assert(check_pair_validity(pair) == False)

def test_pair_validity_lower_case():
    pair = "usdc/btc"
    assert(check_pair_validity(pair) == False)

def test_pair_validity_lower_upper_case_mix():
    pair = "usdc/BAHIO"
    assert(check_pair_validity(pair) == False)

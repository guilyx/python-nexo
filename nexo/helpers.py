import re
# temp: use regex!
def check_pair_validity(pair: str)-> bool:
    assets = pair.split("/")

    if len(assets) != 2:
        return False

    print(assets)
    
    for asset in assets:
        print(asset)
        if not re.match(r"[A-Z]{2,6}", asset) or len(asset) > 6:
            return False

    return True
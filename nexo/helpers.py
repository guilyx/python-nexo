import re
from typing import Dict
import json

def check_pair_validity(pair: str)-> bool:
    assets = pair.split("/")

    if len(assets) != 2:
        return False
    
    for asset in assets:
        if not re.match(r"[A-Z]{2,6}", asset) or len(asset) > 6:
            return False

    return True

def compact_json_dict(data: Dict):
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
import sys
import requests
import traceback
import logging
from .config import API_ROOT
import pandas as pd

logger = logging.getLogger(__name__)
    
def get_data_for_score() -> pd.DataFrame:
    try:
        r = requests.get(f'{API_ROOT}/miners/score_data')
        return pd.DataFrame(r.json())
    except:
        traceback.print_exc(1, file=sys.stdout)
        return None
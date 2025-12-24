import bittensor as bt
import math
import pandas as pd
from dinobets import api

def compute_miner_scores(n: int = 256) -> pd.Series:
    """
    Fully vectorized per-miner score computation.
    Returns a pandas Series indexed by uid.
    """
    df = api.get_data_for_score()
    df['score'] = (df['max_profit'] * df['pool_amount']) ** 0.5 / df['house_edge']
    + math.log(df['cnt_user']) + (1 + df['growth_users']) * df['wager'] / df['days']

    scores = pd.Series(0, index=range(n), dtype=float)
    scores[df['uid']] = df['score'].values
    return scores
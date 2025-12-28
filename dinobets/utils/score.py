import bittensor as bt
import pandas as pd
from dinobets import api
import numpy as np

def compute_miner_scores(n: int = 256) -> pd.Series:
    """
    Fully vectorized per-miner score computation.
    Returns a pandas Series indexed by uid.
    """
    df = api.get_data_for_score()
    df['score'] = (df['max_profit'] * df['pool_amount']) ** 0.5 / df['house_edge']
    +  np.log1p(df['cnt_user']) * df['wager'] / df['days']

    scores = pd.Series(0, index=range(n), dtype=float)
    scores[df['uid']] = df['score'].values
    return scores
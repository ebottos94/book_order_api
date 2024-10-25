import pandas as pd
from typing import List

"""
Get Df from raw data and add 'value' column
"""


def get_df(data: List[dict]):
    df = pd.DataFrame(data)
    df["value"] = df.px * df.qty
    return df


"""
Calculate stats for Bids and Asks single book
"""


def get_symbol_stats(data: List[dict]):
    df = get_df(data)
    mean_value = df["value"].mean()
    df = df.sort_values(by="value", ascending=False)
    max_value = df.iloc[0].to_dict()
    min_value = df.iloc[-1].to_dict()
    tot_qty = df["qty"].sum()
    tot_price = df["px"].sum()
    return {
        "average_value": mean_value,
        "greater_value": max_value,
        "lesser_value": min_value,
        "total_qty": tot_qty,
        "total_px": tot_price,
    }


"""
Calculate general stats for all books
"""


def get_global_stats(data: List[dict]):
    df = get_df(data)
    return {"count": df.shape[0], "qty": df["qty"].sum(), "value": df["value"].sum()}

import logging

import pandas as pd


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if DataFrame is not empty
    if df.empty:
        logging.info("No songs downloaded. Finishing execution")
        return False

    # Primary key check
    if not pd.Series(df["played_at"]).is_unique:
        raise Exception("Primary key check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")

    return True

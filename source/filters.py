# filters.py

import pandas as pd

def filter_forbidden_terms(items_df, forbidden_terms):
    """ Filter out items containing forbidden terms in the title """
    mask = ~items_df['Title'].str.lower().str.contains(r'\b(?:' + '|'.join(forbidden_terms) + r')\b')
    filtered_df = items_df[mask]
    return filtered_df

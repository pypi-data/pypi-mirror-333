"""
Absfuyu: Data Analysis [W.I.P]
------------------------------
Extension for ``pd.DataFrame``
(deprecated)

Version: 5.1.0
Date updated: 10/03/2025 (dd/mm/yyyy)
"""

# Library
# ---------------------------------------------------------------------------
from absfuyu.extra.da.dadf import DADF  # noqa
from absfuyu.extra.da.df_func import (  # noqa
    compare_2_list,
    equalize_df,
    rename_with_dict,
)

# Class - DA
# TODO: split column df[['A','B']]=df['AB'].str.split(' ',n=1,expand=True) | drop dups | Combine: row with data, row NaN

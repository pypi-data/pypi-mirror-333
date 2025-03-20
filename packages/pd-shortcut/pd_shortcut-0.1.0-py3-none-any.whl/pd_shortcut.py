#!/usr/bin/env python

"""
Shortcuts for working with pandas DataFrames.
"""

__version__ = "0.1.0"

import pandas as pd


def load(p, **kwargs):
    s = str(p)
    if s.endswith('.csv') or s.endswith('.csv.gz'):
        return pd.read_csv(p, **kwargs)
    elif s.endswith('.tsv') or s.endswith('.tsv.gz'):
        sep = kwargs.pop('sep', '\t')
        return pd.read_csv(p, sep=sep, **kwargs)
    elif s.endswith('.parquet'):
        return pd.read_parquet(p, **kwargs)
    elif s.endswith('.smi') or s.endswith('.smi.gz'):
        sep, header = kwargs.pop('sep', '\t'), kwargs.pop('header', None)
        return pd.read_csv(p, sep=sep, header=header, **kwargs)
    else:
        raise ValueError(f'No known extension was found from "{p}" to determine how to read the data')


def save(df, p, **kwargs):
    s = str(p)
    if s.endswith('.csv') or s.endswith('.csv.gz'):
        df.to_csv(p, **kwargs)
    elif s.endswith('.tsv') or s.endswith('.tsv.gz'):
        sep = kwargs.pop('sep', '\t')
        return df.to_csv(p, sep=sep, **kwargs)
    elif s.endswith('.parquet'):
        return df.to_parquet(p, **kwargs)
    elif s.endswith('.smi') or s.endswith('.smi.gz'):
        sep, header = kwargs.pop('sep', '\t'), kwargs.pop('header', None)
        return df.to_csv(p, sep=sep, header=header, **kwargs)
    else:
        raise ValueError(f'No known extension was found from "{p}" to determine how to save the data')


pd.read = load
pd.save = save

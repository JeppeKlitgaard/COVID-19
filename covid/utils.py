import wbdata
import numpy as np
import pandas as pd


def rchop(s, sub):
    return s[:-len(sub)] if s.endswith(sub) else s


def lchop(s, sub):
    return s[len(sub):] if s.startswith(sub) else s


def print_wb_sources():
    wbdata.get_source()


def print_wb_indicators(source):
    wbdata.get_indicator(source=source)


def get_x_day(df, label, n):
    """
    Get the day of the nth `label` in country according to ts_df.

    label can be 'deaths', 'cases', 'recoveries'.
    """
    # 'deaths > 10'
    query_string = f'{label} > {n}'
    try:
        return df.query(query_string).iloc[0]['day']
    except IndexError:
        return np.NaN


def drop_y(df, suffix='_y', inplace=True):
    """
    Drops duplicate y-column.
    See: https://stackoverflow.com/questions/19125091/pandas-merge-how-to-avoid-duplicating-columns

    Use with suffixes=('', '_y')
    """
    to_drop = [x for x in df if x.endswith(suffix)]
    if inplace:
        return df.drop(to_drop, axis=1, inplace=True)
    else:
        return df.drop(to_drop, axis=1)


def get_latest_valid(df, groupby_index='country'):
    list_of_indexes = df.groupby(groupby_index).apply(pd.Series.first_valid_index).to_list()
    mi = pd.MultiIndex.from_tuples(list_of_indexes)
    return df.reindex(mi)

import wbdata
import numpy as np


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

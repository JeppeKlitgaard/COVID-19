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

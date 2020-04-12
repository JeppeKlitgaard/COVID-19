import wbdata
import numpy as np
import pandas as pd
import pycountry
import pycountry_convert


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


def country_to_continent(country, verbose=False):
    if verbose:
        print(f'Processing country: {country}')
    try:
        country_obj = pycountry.countries.search_fuzzy(country)[0]
    except (LookupError, AttributeError) as e:
        print(f'Failed to process {country} due to error: {e}')
        return 'Unknown'
    
    try:
        continent_code = pycountry_convert.country_alpha2_to_continent_code(country_obj.alpha_2)
    except KeyError as e:
        print(f'Failed to process {country} due to error: {e}')
        return 'Unknown'
    
    continent = pycountry_convert.convert_continent_code_to_continent_name(continent_code)
    
    return continent

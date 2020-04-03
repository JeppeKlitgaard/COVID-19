import wbdata

def print_wb_sources():
    wbdata.get_source()


def print_wb_indicators(source):
    wbdata.get_indicator(source=source)


def find_date_of_nth_label(ts_df, country, n, label):
    """
    Get the date of the nth `label` in country according to ts_df.

    label can be 'deaths', 'cases', 'recoveries'.
    """
    try:
        return ts_df.loc[country][ts_df.loc[country][label] > n].head(1).index.values[0]
    except IndexError:
        return None

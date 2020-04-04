import wbdata
import pandas as pd
import numpy as np
from .constants import DATA_URLS, JHU_RENAMED_COLUMNS, JHU_DATE_FILTER

def grab_wbdata(indicators, countries='all', convert_date=False):
    """Grab indicator data via wbdata."""
    df = wbdata.get_dataframe(indicators, country=countries, convert_date=convert_date)
    
    return df

def grab_JHU():
    """Grab COVID-19 data from John Hopkin's data set."""
    LABELS = ('cases', 'deaths', 'recoveries')
    MERGE_ON_COLUMNS = ('country', 'province_state', 'lat', 'long', 'date')

    dfs = {}
    for label in LABELS:
        # Get data
        df = pd.read_csv(DATA_URLS['global'][label])
        df.rename(columns=JHU_RENAMED_COLUMNS['time_series'], inplace=True)

        # Melt df into proper format
        date_cols = df.filter(regex=JHU_DATE_FILTER).columns.array
        df = pd.melt(df, id_vars=['province_state', 'country', 'lat', 'long'],
            value_vars=date_cols, var_name='date', value_name=label)
        dfs[label] = df
    
    # Merge into one dataframe
    df_jhu = pd.merge(dfs[LABELS[0]], dfs[LABELS[1]], on=MERGE_ON_COLUMNS)
    df_jhu = pd.merge(df_jhu, dfs[LABELS[2]], on=MERGE_ON_COLUMNS)

    # Convert date into datetime type
    df_jhu.date = pd.to_datetime(df_jhu.date, format='%m/%d/%y')  # Weird American format
    df_jhu['day'] = (df_jhu.date - pd.to_datetime(df_jhu.date.iloc[0])).astype('timedelta64[D]')

    # Fill in NaN province_state with country index
    df_jhu['province_state'] = df_jhu.province_state.fillna(df_jhu.country)

    pivot_temp = df_jhu.pivot_table(index=['country', 'date'], columns='province_state', margins=True, margins_name='total', values=['cases', 'deaths', 'recoveries'], aggfunc=np.sum).stack()
    df_jhu = pd.merge(df_jhu, pivot_temp, on=['country', 'date', 'deaths', 'cases', 'recoveries', 'province_state'], how='right')
    df_jhu.set_index(['country', 'date'], inplace=True)
    df_jhu.sort_index(inplace=True)
    df_jhu.ffill(inplace=True)

    # Clean up after pivot
    df_jhu.reset_index(inplace=True)
    df_jhu.drop(df_jhu[df_jhu['country'] == 'total'].index, inplace=True)

    df_jhu.set_index(['country', 'date'], inplace=True)
    df_jhu.sort_index(inplace=True)

    return df_jhu


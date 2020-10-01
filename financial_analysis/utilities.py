import os, sys, inspect

import pandas as pd
import matplotlib as plt
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

working_dir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(working_dir)
sys.path.insert(0, parent_dir)


# GET DATA ============================================================
def get_historical_data(
        csv_path: str,
        ) -> pd.core.frame.DataFrame:

    df = pd.read_csv(csv_path, usecols=['Date', 'Price'])
    df.columns = ['date', 'price']
    df['date'] = pd.to_datetime(df['date'])
    try:
        df['price'] = df['price'].str.replace(',', '')
    except AttributeError:
        pass
    df['price'] = pd.to_numeric(df['price'])

    return df


# PLOT DATA ===========================================================
def plot_historical_data(
        data_dfs: list
        ):
    fig, ax = plt.subplots(figsize=[12, 8])

    for df in data_dfs:
        ax.plot(
            df['date'],
            df['price'],
            )

    plt.xlabel('Date')
    plt.ylabel('Share Price')
    plt.show()
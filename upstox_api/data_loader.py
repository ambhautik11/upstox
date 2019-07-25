from past.builtins import raw_input

from upstox_api.api import *
from datetime import *
from pprint import pprint
import numpy as np
import talib
import matplotlib.pyplot as plt
import pandas as pd

import os, sys
from tempfile import gettempdir

u = Upstox('SJLkbkvO203qdlfEJsj2y1Smb3q9rNvZ3qicd8wL','97568a26efc5a8b410ddc9c5df3017e9d034781e')

# securities = [ 'M&M', 'MARUTI',
#               'ASHOKLEY']

securities = ['TATAMOTORS','TECHM','LUPIN','SBIN','TATASTEEL','SAIL','VEDL','CANBK','DRREDDY','M&M','MARUTI','ASHOKLEY']




def start():
    global u
    print("Sdf");
    # u = Upstox(upstox.api_key, upstox.access_token);
    u.get_master_contract("NSE_EQ");

    ### Uncomment  to read 6 months data between curr_data - end_date

    curr_date = datetime.strptime('01/04/2019', '%d/%m/%Y').date()
    end_date = datetime.strptime('01/07/2019', '%d/%m/%Y').date()

    print("Loading Data...")

    for stock in securities:
        print("Loading for :" , stock)
        #data_6months_5minutes = load_data(curr_date, end_date, OHLCInterval.Minute_5, stock)
        data_6months_Day = load_data(curr_date, end_date, OHLCInterval.Day_1, stock )

        atr = ATR(data_6months_Day, stock);


    '''df_6months_DAY = pd.read_csv('./6months_Data_Day/TATAMOTORS_data_6months.csv');

    atr = df_6months_DAY['atr'];

    plt.plot(atr,color='r');
    plt.plot([(float(data.get('close')) - 1300) for data in data_6months_Day],color='b')
    plt.show();'''

    # run_back_testing("TATAMOTORS")


# /home/bhautik/ghost/upstox-python
def ATR(data_Day, stock, timeperiod=21):
    filename = './6months_Data_Day/' + stock + '_data_6months.csv'
    df = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False);

    high = np.array([float(data.get('high')) for data in data_Day]);
    df['high'] = high.tolist();
    low = np.array([float(data.get('low')) for data in data_Day]);
    df['low'] = low.tolist();
    close = np.array([float(data.get('close')) for data in data_Day]);
    df['close'] = close.tolist();
    atr = talib.ATR(high, low, close, timeperiod);
    df['atr'] = atr;

    date = np.array(
        [datetime.fromtimestamp(int(data.get('timestamp')) / 1000).strftime('%d/%m/%Y') for data in data_Day])
    df['date'] = date
    df.to_csv(filename, sep=',');

    return atr


def load_data(curr_date, end_date, interval, stock):
    global u

    data_6months = []
    while (curr_date <= end_date):
        data_Day = u.get_ohlc(u.get_instrument_by_symbol('NSE_EQ', stock), interval,
                              curr_date,
                              curr_date + timedelta(days=6))
        curr_date = curr_date + timedelta(days=7)

        # pprint(data_Day);
        data_6months += data_Day

    return data_6months

start();

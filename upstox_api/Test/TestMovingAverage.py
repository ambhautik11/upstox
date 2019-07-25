from past.builtins import raw_input

from upstox_api.api import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

u = None

def load_data(curr_date, end_date, interval, stock):

    global u
    u.get_master_contract("NSE_EQ");
    df = pd.DataFrame(columns=['date', 'close', 'rolling_avg'])

    data_6months = []
    dates = []

    while (curr_date <= end_date):
        print('Date : ', curr_date)
        data_Day = u.get_ohlc(u.get_instrument_by_symbol('NSE_EQ', stock), interval,
                              curr_date,
                              curr_date + timedelta(days=6))
        curr_date = curr_date + timedelta(days=7)

        # pprint(data_Day);
        for data in data_Day:
            today = datetime.fromtimestamp(int(data.get('timestamp')) / 1000).strftime('%d/%m/%Y')
            dates.append(today)
        data_6months += data_Day

    ax = plt.gca()
    df['date'] = dates
    df['close'] = [float(data.get('close')) for data in data_6months];

    df['rolling_avg'] = df['close'].rolling(window=21).mean()
    df.plot(kind='line', x='date', y='rolling_avg', color='blue', ax=ax)
    df.plot(kind='line', x='date', y='close', color='red', ax=ax)

    plt.show()
    print("Done")
    print(df)
    return data_6months



def main():
    print("Inside Main...")
    stored_api_key = 'SJLkbkvO203qdlfEJsj2y1Smb3q9rNvZ3qicd8wL'  # read_key_from_settings('api_key')
    stored_access_token = '7b222d7bbf5f5452f544a131d98bf8b0cacebf41' #read_key_from_settings('access_token')
    global u
    u = Upstox(stored_api_key, stored_access_token)

    curr_date = datetime.strptime('01/04/2019', '%d/%m/%Y').date()
    end_date = datetime.strptime('01/07/2019', '%d/%m/%Y').date()

    data_6months_Day = load_data(curr_date, end_date, OHLCInterval.Day_1, "TATAMOTORS")


if __name__ == "__main__":
    print("Main Running...")
    main()
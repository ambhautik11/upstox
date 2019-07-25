from past.builtins import raw_input

from upstox_api.api import *
from datetime import *
from pprint import pprint
import numpy as np
import talib
import math
import pandas as pd
import holidays
import time
from tempfile import gettempdir

u = None
entryList = []
exitList = []
plList = []
typeList = []
dateList = []

securities = ['TATAMOTORS','TECHM','LUPIN','SBIN','TATASTEEL','SAIL','VEDL','CANBK','DRREDDY','M&M','MARUTI','ASHOKLEY']
df = pd.DataFrame(columns=['date' ,'entry', 'exit', 'type', 'P/L']);


def start(upstox):
    global u
    global df
    global entryList
    global exitList
    global plList
    global typeList
    global dateList

    print("Sdf");
    u = Upstox (upstox.api_key, upstox.access_token);
    u.get_master_contract("NSE_EQ");

    '''
    ### Uncomment  to read 6 months data between curr_data - end_date
    
    curr_date = datetime.strptime('01/01/2019', '%d/%m/%Y').date()
    end_date = datetime.strptime('01/07/2019', '%d/%m/%Y').date()

    print("Loading Data...")

    for stock in securities:
        print("Loading for :" , stock)
        #data_6months_5minutes = load_data(curr_date, end_date, OHLCInterval.Minute_5, stock)
        data_6months_Day = load_data(curr_date, end_date, OHLCInterval.Day_1, stock )

        atr = ATR(data_6months_Day, stock);
    '''

    '''df_6months_DAY = pd.read_csv('./6months_Data_Day/TATAMOTORS_data_6months.csv');

    atr = df_6months_DAY['atr'];

    plt.plot(atr,color='r');
    plt.plot([(float(data.get('close')) - 1300) for data in data_6months_Day],color='b')
    plt.show();'''

    for stock in securities:

        print('-------------------------------------')
        print('-------------------------------------')
        print('              '+ stock + '               ')
        print('-------------------------------------')
        print('-------------------------------------')

        dfRead = pd.read_csv('./6months_Data_Day/' + stock + '_data_6months.csv')

        dateRange = dfRead['date']

        # curr_date = datetime.strptime('01/06/2019', '%d/%m/%Y').date()
        # end_date = datetime.strptime('01/07/2019', '%d/%m/%Y').date()
        #while(curr_date<=end_date):

        i = 0;
        for curr_date in dateRange:
            if i == 0:
                i += 1
                continue;
            current_date = datetime.strptime(curr_date, '%d/%m/%Y').date()
            run_back_testing(stock,current_date);
            #curr_date = nextBusinessDay(curr_date);


        global entryList
        global exitList
        global plList
        global typeList
        global dateList

        df['date'] = dateList
        df['entry'] = entryList
        df['exit'] = exitList
        df['type'] = typeList
        df['P/L'] = plList

        print('-------------------------------------')
        print('-------------------------------------')
        print('              Finished               ')
        print('-------------------------------------')
        print('-------------------------------------')
        #print(df)
        df.to_csv('./Stock_PL/' + stock + '_PL.csv', sep=',')

        entryList.clear()
        exitList.clear()
        plList.clear()
        typeList.clear()
        dateList.clear()


#/home/bhautik/ghost/upstox-python
def ATR(data_Day, stock, timeperiod=21):
    filename = './6months_Data_Day/' + stock + '_data_6months.csv'
    df = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False);

    high = np.array([float(data.get('high'))for data in data_Day]);
    df['high'] = high.tolist();
    low = np.array([float(data.get('low')) for data in data_Day]);
    df['low'] = low.tolist();
    close = np.array([float(data.get('close')) for data in data_Day]);
    df['close'] = close.tolist();
    atr = talib.ATR(high, low, close, timeperiod);
    df['atr'] = atr;

    date = np.array([datetime.fromtimestamp(int(data.get('timestamp'))/1000).strftime('%d/%m/%Y') for data in data_Day])
    df['date'] = date
    df.to_csv(filename, sep=',');

    return atr

def load_data(curr_date, end_date, interval, stock):
    global u

    #
    # data_6months = []
    # while(curr_date <= end_date):
    return u.get_ohlc(u.get_instrument_by_symbol('NSE_EQ', stock), interval,
               curr_date,
               end_date)
        # curr_date = curr_date + timedelta(days=6)
        #pprint(type(data_Day));
        # data_6months += data_Day

    # return data_6months


def run_back_testing(stock,date):

    global u
    global df
    global entryList
    global exitList
    global plList
    global typeList
    global dateList

    entry = -1
    exit = -1
    type = ''
    stop_loss = -1
    pl = 0

    high_45minute = -1
    low_45minute = -1

    today = date # datetime.today();

    yesterday = previousBusinessDay(today);

    data_today_5minutes = load_data(today, today + timedelta(days=1),
                                      OHLCInterval.Minute_5,
                                          stock)

    if len(data_today_5minutes) == 0 :
        return;
    data_yesterday_Day = load_data(yesterday, today,
                                    OHLCInterval.Day_1,
                                    stock)

    high_yesterday = float(data_yesterday_Day[0].get('high'));
    low_yesterday = float(data_yesterday_Day[0].get('low'));
    close_yesterday = float(data_yesterday_Day[0].get('close'));


    #print(len(data_yesterday_Day))

    for i in range(9):
        data = data_today_5minutes[i];
        #print(data.get('high') , ' | ', data.get('low') , ' | ', data.get('close') , ' | ', datetime.fromtimestamp(int(data.get('timestamp'))/1000));
        local_high = float(data.get('high'))
        local_low = float(data.get('low'))

        if high_45minute == -1:
            high_45minute = local_high
        else :
            high_45minute = max(high_45minute, local_high)

        if low_45minute == -1:
            low_45minute = local_low
        else :
            low_45minute = max(low_45minute, local_low)

    print('Low : ' , low_45minute , ' High :' , high_45minute , ' | Date :', today)


    if high_45minute > high_yesterday and high_45minute > close_yesterday :
        gain_45minute = high_45minute - close_yesterday;
        if gain_45minute > close_yesterday*0.02 :
            print("Enter the long trade");

            entry = float(data_today_5minutes[9].get('open'))
            type = 'long'
            stop_loss = (1 - 0.0075) * entry
            exit = float(day_simulation(data_today_5minutes, entry, type, stop_loss,stock))
            pl = (exit - entry) * 100 / entry

    else:
        if low_45minute < low_yesterday :
            print("Enter the short trade")
            entry = float(data_today_5minutes[9].get('open'))
            type = 'short'
            stop_loss = 1.0075 * entry
            exit = float(day_simulation(data_today_5minutes, entry, type, stop_loss,stock))
            pl = (entry - exit) * 100 / entry

    entryList.append(entry)
    exitList.append(exit)
    typeList.append(type)
    plList.append(pl)
    dateList.append(date.strftime('%d/%m/%Y'))
    #pprint(data_6months_1minutes)


def day_simulation(data_today_5minutes, entry, type, stop_loss,security):

    for i in range(9,len(data_today_5minutes)):
        data = data_today_5minutes[i];
        data_previous = data_today_5minutes[i-1];
        date = (datetime.fromtimestamp(int(data.get('timestamp')) / 1000))
        date = previousBusinessDay(date)

        date = date.strftime('%d/%m/%Y')
        df = pd.read_csv('./6months_Data_Day/' + security + '_data_6months.csv', index_col='date')
        data_previous_day = df.loc[date]


        high = float(data.get('high'));
        low = float(data.get('low'));
        close = float(data_today_5minutes[i-1].get('close'))

        temp1 = abs(high - low)
        temp2 = abs(high - close)
        temp3 = abs(low - close)
        tr = max(temp1 , temp2 , temp3)
        atr = float(data_previous_day['atr'])*20
        if math.isnan(atr):
            atr = tr
        else :
            atr = atr + tr;
            atr = atr / 21

        new_sl = float(data.get('close'))

        if i == len(data_today_5minutes) - 1:
            print(security, "  ", entry, "  ", data.get('close'), "  ", type, "  ", "SO HIT")
            return float(data.get('close'))

        if (type == 'long') :
            new_sl -= 4*atr;
            if(stop_loss < new_sl):
                stop_loss = new_sl

            if float(data.get('low'))<=stop_loss :
                print(security , "  ", entry , "  ",stop_loss , "  " , type , "  ","SL HIT")
                #time.sleep(5)
                return stop_loss;
        else:
            new_sl += 4*atr
            #print("Stock Values With Time :" , int(5*i) , " | Values : ", high, " : " , low, " : ", float(data_today_5minutes[i].get('close')))
            #print("Stop Losses : ", stop_loss, " : ", new_sl, " : ", atr, " | " , tr)
            #time.sleep(5)

            if(stop_loss > new_sl):
                stop_loss = new_sl

            if float(data.get('high'))>=stop_loss :
                print(security , "  ", entry , "  ",stop_loss , "  " , type , "  ","SL HIT")
                return stop_loss;




    print('somthinn wrong buddy....')
    return float(entry)




def nextBusinessDay(date):
    return findBusinessDay(date, 1);


def previousBusinessDay(date):
    return findBusinessDay(date, -1)


def findBusinessDay(date, direction):
    date = date + timedelta(direction)

    while(True):
        if date.weekday() > 4:
            date = date + timedelta(direction)
        else:
            break;

    return date;
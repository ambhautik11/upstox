from past.builtins import raw_input

from upstox_api.api import *
from datetime import datetime, timedelta
from pprint import pprint
import os, sys
import pandas as pd
import calendar
import holidays
from tempfile import gettempdir
import ORB_ATR

try:
    input = raw_input
except NameError:
    pass

u = None
s = None

break_symbol = '@'

profile = None


def main():
    global s, u

    logged_in = False

    print('Welcome to Upstox API!\n')
    print('This is an interactive Python connector to help you understand how to get connected quickly')
    print('The source code for this connector is publicly available')
    print('To get started, please create an app on the Developer Console (developer.upstox.com)')
    print('Once you have created an app, keep your app credentials handy\n')

    stored_api_key = 'SJLkbkvO203qdlfEJsj2y1Smb3q9rNvZ3qicd8wL'  # read_key_from_settings('api_key')
    stored_access_token = '7b222d7bbf5f5452f544a131d98bf8b0cacebf41' #read_key_from_settings('access_token')
    if stored_access_token is not None and stored_api_key is not None:
        print('You already have a stored access token: [%s] paired with API key [%s]' % (
            stored_access_token, stored_api_key))
        print('Do you want to use the above credentials?')
        selection = 'y'  # input('Type N for no, any key for yes:  ')
        if selection.lower() != 'n':
            try:
                u = Upstox(stored_api_key, stored_access_token)
                logged_in = True
            except requests.HTTPError as e:
                print('Sorry, there was an error [%s]. Let''s start over\n\n' % e)

    if logged_in is False:
        stored_api_key = read_key_from_settings('api_key')
        if stored_api_key is not None:
            api_key = input('What is your app''s API key [%s]:  ' % stored_api_key)
            if api_key == '':
                api_key = stored_api_key
        else:
            api_key = input('What is your app''s API key:  ')
        write_key_to_settings('api_key', api_key)

        stored_api_secret = read_key_from_settings('api_secret')
        if stored_api_secret is not None:
            api_secret = input('What is your app''s API secret [%s]:  ' % stored_api_secret)
            if api_secret == '':
                api_secret = stored_api_secret
        else:
            api_secret = input('What is your app''s API secret:  ')
        write_key_to_settings('api_secret', api_secret)

        stored_redirect_uri = read_key_from_settings('redirect_uri')
        if stored_redirect_uri is not None:
            redirect_uri = input('What is your app''s redirect_uri [%s]:  ' % stored_redirect_uri)
            if redirect_uri == '':
                redirect_uri = stored_redirect_uri
        else:
            redirect_uri = input('What is your app''s redirect_uri:  ')
        write_key_to_settings('redirect_uri', redirect_uri)

        s = Session(api_key)
        s.set_redirect_uri(redirect_uri)
        s.set_api_secret(api_secret)

        print('\n')

        print('Great! Now paste the following URL on your browser and type the code that you get in return')
        print('URL: %s\n' % s.get_login_url())

        input('Press the enter key to continue\n')

        code = input('What is the code you got from the browser:  ')

        s.set_code(code)
        try:
            access_token = '97568a26efc5a8b410ddc9c5df3017e9d034781e'
        except SystemError as se:
            print('Uh oh, there seems to be something wrong. Error: [%s]' % se)
            return
        write_key_to_settings('access_token', access_token)
        u = Upstox(api_key, access_token)

    clear_screen()
    show_home_screen()


def show_home_screen():
    global s, u
    global profile

    print('\n*** Welcome to Upstox API ***\n\n')
    print('1. Get Profile\n')
    print('2. Get Balance\n')
    print('3. Get Positions\n')
    print('4. Get Holdings\n')
    print('5. Get Order History\n')
    print('6. Get LTP Quote\n')
    print('7. Get Full Quote\n')
    print('8. Show socket example\n')
    print('9. Quit\n')
    print('10. get Historical Data\n')

    selection = 10 #input('Select your option: \n')

    try:
        int(selection)
    except:
        clear_screen()
        show_home_screen()

    selection = int(selection)
    clear_screen()
    if selection == 1:
        load_profile()
        pprint(profile)
    elif selection == 2:
        pprint(u.get_balance())
    elif selection == 3:
        pprint(u.get_positions())
    elif selection == 4:
        pprint(u.get_holdings())
    elif selection == 5:
        pprint(u.get_order_history())
    elif selection == 6:
        product = select_product()
        if product is not None:
            pprint(u.get_live_feed(product, LiveFeedType.LTP))
    elif selection == 7:
        product = select_product()
        if product is not None:
            pprint(u.get_live_feed(product, LiveFeedType.Full))
    elif selection == 8:
        socket_example()
    elif selection == 9:
        sys.exit(0)
    elif selection == 10:
        u.get_master_contract("NSE_EQ");
        data = u.get_ohlc(u.get_instrument_by_symbol('NSE_EQ', 'RELIANCE'), OHLCInterval.Minute_5,
                          datetime.strptime('01/07/2017', '%d/%m/%Y').date(),
                          datetime.strptime('07/07/2017', '%d/%m/%Y').date())

        print("sdf")
        ORB_ATR.start(u);
        selection = input('Select your option: \n')

    show_home_screen();


def getData():
    respose1 = u.get_ohlc(u.get_instrument_by_symbol('NSE_EQ', 'RELIANCE'), OHLCInterval.Minute_10,
                          datetime.strptime('01/07/2017', '%d/%m/%Y').date(),
                          datetime.strptime('07/07/2017', '%d/%m/%Y').date())
    pprint(respose1)


def load_profile():
    global profile
    # load user profile to variable
    profile = u.get_profile()


def select_product():
    global u
    exchange = select_exchange()
    product = None
    clear_screen()
    while exchange is not None:
        u.get_master_contract(exchange)
        product = find_product(exchange)
        clear_screen()
        if product is not None:
            break
        exchange = select_exchange()

    return product


def find_product(exchange):
    found_product = False
    result = None

    while not found_product:
        query = input('Type the symbol that you are looking for. Type %s to go back:  ' % break_symbol)
        if query.lower() == break_symbol:
            found_product = True
            result = None
            break
        results = u.search_instruments(exchange, query)
        if len(results) == 0:
            print('No results found for [%s] in [%s] \n\n' % (query, exchange))
            break
        else:
            for index, result in enumerate(results):
                if index > 9:
                    break
                print('%d. %s' % (index, result.symbol))
            selection = input('Please make your selection. Type %s to go back:  ' % break_symbol)

            if query.lower() == break_symbol:
                found_product = False
                result = None
                break

            try:
                selection = int(selection)
            except ValueError:
                found_product = False
                result = None
                break

            if 0 <= selection <= 9 and len(results) >= selection + 1:
                found_product = True
                result = results[selection]
                break

            found_product = False

    return result


def select_exchange():
    global profile
    if profile is None:
        load_profile()

    back_to_home_screen = False
    valid_exchange_selected = False

    while not valid_exchange_selected:
        print('** Live quote streaming example **\n')
        for index, item in enumerate(profile[u'exchanges_enabled']):
            print('%d. %s' % (index + 1, item))
        print('9. Back')
        print('\n')

        selection = input('Select exchange: ')

        try:
            selection = int(selection)
        except ValueError:
            break

        if selection == 9:
            valid_exchange_selected = True
            back_to_home_screen = True
            break

        selected_index = selection - 1

        if 0 <= selected_index < len(profile[u'exchanges_enabled']):
            valid_exchange_selected = True
            break

    if back_to_home_screen:
        return None

    return profile[u'exchanges_enabled'][selected_index]


def socket_example():
    print('Press Ctrl+C to return to the main screen\n')
    u.set_on_quote_update(event_handler_quote_update)
    u.get_master_contract('NSE_EQ')
    try:
        u.subscribe(u.get_instrument_by_symbol('NSE_EQ', 'TATASTEEL'), LiveFeedType.Full)
    except:
        pass
    try:
        u.subscribe(u.get_instrument_by_symbol('NSE_EQ', 'RELIANCE'), LiveFeedType.LTP)
    except:
        pass
    u.start_websocket(False)


def event_handler_quote_update(message):
    pprint("Quote Update: %s" % str(message))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def write_key_to_settings(key, value):
    filename = os.path.join(gettempdir(), 'interactive_api.json')
    try:
        file = open(filename, 'r')
    except IOError:
        data = {"api_key": "", "api_secret": "", "redirect_uri": "", "access_token": ""}
        with open(filename, 'w') as output_file:
            json.dump(data, output_file)
    file = open(filename, 'r')
    try:
        data = json.load(file)
    except:
        data = {}
    data[key] = value
    with open(filename, 'w') as output_file:
        json.dump(data, output_file)


def read_key_from_settings(key):
    filename = os.path.join(gettempdir(), 'interactive_api.json')
    try:
        file = open(filename, 'r')
    except IOError:
        file = open(filename, 'w')
    file = open(filename, 'r')
    try:
        data = json.load(file)
        return data[key]
    except:
        pass
    return None




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

if __name__ == "__main__":
    main()
    #indianHolidays = holidays.India()
    today = datetime.today()
    date = previousBusinessDay(today)
    pprint(calendar.day_name[date.weekday()])
    date = previousBusinessDay(date)
    pprint(calendar.day_name[date.weekday()])
    date = previousBusinessDay(date)
    pprint(calendar.day_name[date.weekday()])


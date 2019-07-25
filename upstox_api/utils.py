from collections import namedtuple
import re

Instrument = namedtuple('Instrument', ['exchange', 'token', 'parent_token', 'symbol',
                                       'name', 'closing_price', 'expiry', 'strike_price',
                                       'tick_size', 'lot_size', 'instrument_type', 'isin'])


class CustomEnum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
    def __setattr__(self, name, value):
        raise RuntimeError("Cannot override values")
    def __delattr__(self, name):
        raise RuntimeError("Cannot delete values")


class PyCurlVerbs(CustomEnum):
    PUT = 'PUT'
    DELETE = 'DELETE'
    GET = 'GET'
    POST = 'POST'


class OHLCInterval(CustomEnum):
    Minute_1 = '1'
    Minute_5 = '5'
    Minute_10 = '10'
    Minute_15 = '15'
    Minute_30 = '30'
    Minute_60 = '60'
    Day_1 = 'DAY'
    Week_1 = 'WEEK'
    Month_1 = 'MONTH'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == '1':
            return OHLCInterval.Minute_1
        if str == '5':
            return OHLCInterval.Minute_5
        if str == '10':
            return OHLCInterval.Minute_10
        if str == '15':
            return OHLCInterval.Minute_15
        if str == '30':
            return OHLCInterval.Minute_30
        if str == '60':
            return OHLCInterval.Minute_60
        if str == 'DAY':
            return OHLCInterval.Day_1
        if str == 'WEEK':
            return OHLCInterval.Week_1
        if str == 'MONTH':
            return OHLCInterval.Month_1
        return None


class TransactionType(CustomEnum):
    Buy = 'B'
    Sell = 'S'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == 'B':
            return TransactionType.Buy
        if str == 'S':
            return TransactionType.Sell
        return None


class OrderType(CustomEnum):
    Market = 'M'
    Limit = 'L'
    StopLossLimit = 'SL'
    StopLossMarket = 'SL-M'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == 'M':
            return OrderType.Market
        if str == 'L':
            return OrderType.Limit
        if str == 'SL':
            return OrderType.StopLossLimit
        if str == 'SL-M':
            return OrderType.StopLossMarket
        return None

class ProductType(CustomEnum):
    Intraday = 'I'
    Delivery = 'D'
    CoverOrder = 'CO'
    OneCancelsOther = 'OCO'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == 'I':
            return ProductType.Intraday
        if str == 'D':
            return ProductType.Delivery
        if str == 'CO':
            return ProductType.CoverOrder
        if str == 'OCO':
            return ProductType.OneCancelsOther
        return None


class DurationType(CustomEnum):
    DAY = 'DAY'
    IOC = 'IOC'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == 'DAY':
            return DurationType.DAY
        if str == 'IOC':
            return DurationType.IOC
        return None


class LiveFeedType(CustomEnum):
    LTP = 'LTP'
    Full = 'Full'

    @staticmethod
    def parse(str):
        str = str.upper()
        if str == 'LTP':
            return LiveFeedType.LTP
        if str == 'FULL':
            return LiveFeedType.Full
        return None


def is_status_2xx(code):
    return re.search('^2', str(code)) is not None


class SchemaConverter:
    @staticmethod
    def convert_to_long(str):
        try:
            return int(str)
        except:
            return str

    @staticmethod
    def convert_to_original(str):
        return str

    @staticmethod
    def convert_to_bool(str):
        if str == "true":
            return True
        elif str == "false":
            return False
        return str


class Schema(object):
    schema_trade_book = {};

    schema_trade_book['exchange'] = SchemaConverter.convert_to_original
    schema_trade_book['token'] = SchemaConverter.convert_to_original
    schema_trade_book['symbol'] = SchemaConverter.convert_to_original
    schema_trade_book['product'] = ProductType.parse
    schema_trade_book['order_type'] = OrderType.parse
    schema_trade_book['transaction_type'] = SchemaConverter.convert_to_original
    schema_trade_book['traded_quantity'] = SchemaConverter.convert_to_original
    schema_trade_book['exchange_order_id'] = SchemaConverter.convert_to_long
    schema_trade_book['order_id'] = SchemaConverter.convert_to_long
    schema_trade_book['exchange_time'] = SchemaConverter.convert_to_original
    schema_trade_book['time_in_micro'] = SchemaConverter.convert_to_long
    schema_trade_book['trade_id'] = SchemaConverter.convert_to_long

    schema_order_history = {};

    schema_order_history["exchange"] = SchemaConverter.convert_to_original
    schema_order_history["token"] = SchemaConverter.convert_to_original
    schema_order_history["symbol"] = SchemaConverter.convert_to_original
    schema_order_history["product"] = ProductType.parse
    schema_order_history["order_type"] = OrderType.parse
    schema_order_history["duration"] = SchemaConverter.convert_to_original
    schema_order_history["price"] = SchemaConverter.convert_to_original
    schema_order_history["trigger_price"] = SchemaConverter.convert_to_original
    schema_order_history["quantity"] = SchemaConverter.convert_to_original
    schema_order_history["disclosed_quantity"] = SchemaConverter.convert_to_original
    schema_order_history["transaction_type"] = SchemaConverter.convert_to_original
    schema_order_history["average_price"] = SchemaConverter.convert_to_original
    schema_order_history["traded_quantity"] = SchemaConverter.convert_to_original
    schema_order_history["message"] = SchemaConverter.convert_to_original
    schema_order_history["exchange_order_id"] = SchemaConverter.convert_to_long
    schema_order_history["parent_order_id"] = SchemaConverter.convert_to_long
    schema_order_history["order_id"] = SchemaConverter.convert_to_long
    schema_order_history["exchange_time"] = SchemaConverter.convert_to_original
    schema_order_history["time_in_micro"] = SchemaConverter.convert_to_long
    schema_order_history["status"] = SchemaConverter.convert_to_original
    schema_order_history["is_amo"] = SchemaConverter.convert_to_bool
    schema_order_history["valid_date"] = SchemaConverter.convert_to_original
    schema_order_history["order_request_id"] = SchemaConverter.convert_to_long
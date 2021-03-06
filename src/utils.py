
import copy
import time
import json
import numpy as np
import pandas as pd
from datetime import timezone, timedelta, datetime

def unix_ts(ts):
    return pd.to_datetime(ts).timestamp()

def parse_ts(ts):
    # times are in UTC in logs
    return np.datetime64(ts+'+0000')

def pretty_date(ts, offset=-4):
    ts = pd.to_datetime(ts).tz_localize('UTC')
    ts = ts.astimezone(timezone(timedelta(hours=offset)))
    return ts.strftime('%Y%m%d')

def pretty_ts(ts, offset=-4):
    ts = pd.to_datetime(ts).tz_localize('UTC')
    ts = ts.astimezone(timezone(timedelta(hours=offset)))
    return ts.strftime('%A %B %d %Y, %H:%M:%S %Z')

def pretty_label(ts, offset=-4):
    ts = datetime.fromtimestamp(ts).replace(tzinfo=timezone(timedelta()))
    return ts.astimezone(timezone(timedelta(hours=offset))).strftime('%H:%M:%S')

def ts():
    return datetime.utcnow().isoformat()

def now():
    return np.datetime64(ts())

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.datetime64):
            return pd.to_datetime(obj).isoformat()
        if isinstance(obj, np.float32):
            return float(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class Logger(object):

    def __init__(self, mode):
        if mode in ['log', 'scanner']:
            datestr = datetime.utcnow().strftime('%Y%m%d')
        elif mode == 'backtest':
            datestr = datetime.utcnow().strftime('%Y%m%d.%H%M%S')
        else:
            print('ERROR unknown logger mode')
            raise Exception
        file_ = '{}.{}.jsonl'.format(mode, datestr)
        self.fh = open(file_, 'a')

    def __log__(self, type_, msg):
        msg = copy.deepcopy(msg)
        template = '{{"ts": "{}", "type": "{}", "msg": {}}}\n'
        if 'ts' in msg:
            timestamp = msg['ts'].tolist().isoformat()
            del msg['ts']
        else:
            timestamp = ts()
        log = template.format(timestamp, type_, json.dumps(msg, cls=NumpyEncoder))
        self.fh.write(log)
        print(log, end='')

    def operation(self, msg):
        self.__log__('OPERATION', msg)

    def data(self, msg):
        self.__log__('DATA', msg)

    def order(self, msg):
        self.__log__('ORDER', msg)

    def execution(self, msg):
        self.__log__('EXECUTION', msg)

    def misc(self, msg):
        self.__log__('MISC', msg)


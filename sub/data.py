import datetime
import json
import requests
import pandas as pd
from io import BytesIO

def get_date_stock(date: str = datetime.datetime.today().strftime("%Y%m%d")) -> pd.DataFrame:
    gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    gen_otp_data = {
        'mktId': 'ALL', #ALL: 전체, STK: 코스피, KSQ: 코스닥
        'trdDd': date,
        'money': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT01501'
    }
    headers = {'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader'}
    otp = requests.post(gen_otp_url, gen_otp_data, headers=headers).text
    down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
    down_sector_KS  = requests.post(down_url, {'code':otp}, headers=headers)
    data = pd.read_csv(BytesIO(down_sector_KS.content), encoding='EUC-KR')
    if pd.isna(data.loc[0,'시가총액']):
        yasterday = datetime.datetime.strptime(date, "%Y%m%d") - datetime.timedelta(days=1)
        return get_date_stock(yasterday.strftime("%Y%m%d"))
    else: 
        for col in data.columns:
            data[col] = data[col].astype('str')
        return data, date

def start_local_data(date=None) -> dict:
    if date==None:
         current_data, date = get_date_stock()
    else:
         current_data, date = get_date_stock(date)
    startdate = date
    grouped = current_data.groupby('종목코드').agg(list)
    result = {
        key: {col: val if col in ['종가', '거래량', '거래대금'] else val[0]
        for col, val in zip(grouped.columns, values)}
        for key, values in zip(grouped.index, grouped.values)
    }

    for _ in range(9):
        yasterday = datetime.datetime.strptime(date, "%Y%m%d") - datetime.timedelta(days=1)
        current_data, date = get_date_stock(yasterday.strftime("%Y%m%d"))
        for ticker in list(result):
            indices = current_data.index[current_data['종목코드'] == ticker].tolist()
            if not indices:
                result.pop(ticker, None)
            else:
                for category in ['종가', '거래량', '거래대금']:
                    result[ticker][category].append(current_data.loc[indices[0],category])
    return result, startdate, date

def get_local_data():
    with open("data\\data.txt",'r') as f:
        return json.load(f)
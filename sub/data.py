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
    return pd.read_csv(BytesIO(down_sector_KS.content), encoding='EUC-KR')

def start_local_data(date=None) -> dict:
    if date==None:
         current_data = get_date_stock()
    else:
         current_data = get_date_stock(date)
    grouped = current_data.groupby('종목코드').agg(list)
    result = {
        key: {col: val if col in ['종가', '거래량', '거래대금'] else val[0]
        for col, val in zip(grouped.columns, values)}
        for key, values in zip(grouped.index, grouped.values)
    }
    return result

def get_local_data():
    with open("data\\data.txt",'r') as f:
        return json.load(f)
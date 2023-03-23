import datetime
import json
import requests
import pandas as pd
from io import BytesIO

def get_date_stock(date: str = datetime.datetime.today().strftime("%Y%m%d"), next_timedelta=1) -> pd.DataFrame:
	gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
	gen_otp_data = {
		'mktId': 'KSQ', #ALL: 전체, STK: 코스피, KSQ: 코스닥
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
		yasterday = datetime.datetime.strptime(date, "%Y%m%d") + datetime.timedelta(days=next_timedelta)
		return get_date_stock(yasterday.strftime("%Y%m%d"),next_timedelta=next_timedelta)
	else: 
		for col in data.columns:
			data[col] = data[col].astype('str')
		return data, date

def start_local_data(date=None, next_timedelta=1) -> dict:
	if date==None:
		 current_data, date = get_date_stock(next_timedelta=next_timedelta)
	else:
		 current_data, date = get_date_stock(date, next_timedelta)
	startdate = date
	grouped = current_data.groupby('종목코드').agg(list)
	result = {
		key: {col: val if col in ['거래량', '거래대금'] else val[0]
		for col, val in zip(grouped.columns, values)}
		for key, values in zip(grouped.index, grouped.values)
	}

	for _ in range(10):
		date = datetime.datetime.strptime(date, "%Y%m%d") + datetime.timedelta(days=-1)
		current_data, date = get_date_stock(date.strftime("%Y%m%d"), next_timedelta=-1)
		for ticker in list(result):
			indices = current_data.index[current_data['종목코드'] == ticker].tolist()
			if not indices:
				result.pop(ticker, None)
			else:
				for category in ['거래량', '거래대금']:
					result[ticker][category].append(current_data.loc[indices[0],category])
	return result, startdate, date

def get_local_data():
	with open("data\\data.txt",'r') as f:
		return json.load(f)

class data_handler:
	def __init__(self, start_date: str, analysis_period: int):
		self.analysis_period = analysis_period
		self.start_data, self.start_date = get_date_stock(start_date)
		self.ticker_list = list(self.start_data['종목코드'])
		self.trading_volume = { row['종목코드']: [ row['거래량'] ] for index, row in self.start_data.iterrows() }
		self.transaction_amount = { row['종목코드']: [ row['거래대금'] ] for index, row in self.start_data.iterrows() }

		temp_date = start_date
		for _ in range(analysis_period):
			temp_data, temp_date = get_date_stock(date= temp_date, next_timedelta= -1)
			temp_date = datetime.datetime.strptime(temp_date, "%Y%m%d") + datetime.timedelta(days=-1)
			temp_date = temp_date.strftime("%Y%m%d")
			for ticker in list(self.ticker_list):
				indices = temp_data.index[temp_data['종목코드'] == ticker].tolist()
				if indices:
					self.trading_volume[ticker].append(temp_data.loc[indices[0],'거래량'])
					self.transaction_amount[ticker].append(temp_data.loc[indices[0],'거래대금'])
				else:
					self.trading_volume.pop(ticker, None)
					self.transaction_amount.pop(ticker, None)
					self.ticker_list.remove(ticker)
	
	def get_pointer_date(self):
		return self.start_date
	
	def get_today_data(self):
		grouped = self.start_data.groupby('종목코드').agg(list)
		result = {
			key: {col: val[0]
			for col, val in zip(grouped.columns, values) }	
			for key, values in zip(grouped.index, grouped.values)
		}
		for ticker in list(result):
			if ticker not in self.trading_volume:
				result.pop(ticker, None)
				continue
			result[ticker]['거래량'] = list(self.trading_volume[ticker])
			result[ticker]['거래대금'] = list(self.transaction_amount[ticker])

		return result, self.start_date
	
	def fetch_next_data(self):
		self.start_date = (datetime.datetime.strptime(self.start_date, "%Y%m%d") + datetime.timedelta(days=1)).strftime("%Y%m%d")
		self.start_data, self.start_date = get_date_stock(self.start_date)

		for ticker in list(self.ticker_list):
			indices = self.start_data.index[self.start_data['종목코드'] == ticker].tolist()
			if indices:
				self.trading_volume[ticker].insert(0, self.start_data.loc[indices[0],'거래량'])
				self.trading_volume[ticker].pop()
				self.transaction_amount[ticker].insert(0, self.start_data.loc[indices[0],'거래대금'])
				self.transaction_amount[ticker].pop()
			else:
				self.trading_volume.pop(ticker, None)
				self.transaction_amount.pop(ticker, None)
				self.ticker_list.remove(ticker)
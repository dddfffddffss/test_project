import datetime
import json
import traceback
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

import sub.data as data
import sub.pocket as pocket

matplotlib.rcParams['font.family'] ='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] =False

wallet, result={}, []

def make_start_data(date):
    with open("data/"+date+".txt",'w') as f:
        d, startdate, enddate = data.start_local_data(date)
        json.dump(d, f, indent=4, ensure_ascii=False)

def get_web_data(date, next_timedelta):
    return data.start_local_data(date, next_timedelta)

def get_local_data():
    return data.get_local_data()

def show_trade_amount():
	li = []
	data = get_local_data()
	for ticker in data:
		l = np.array(data[ticker]["거래량"]).astype(int)
		s = np.std(l)/np.mean(l)
		if not np.isnan(s):
			li.append((data[ticker], s, ticker))

	li.sort(key=lambda x: x[1])
	for i in li[:30]:
		print(i[0])
		print(i[1])
		print()

	l1 = li[-2600:-2610:-1]
	l1.extend(li[-1:-10:-1])
	for i in l1:
		l = np.array(i[0]["거래량"]).astype(int)
		plt.plot(l/np.mean(l),label=i[0]["종목명"])
		print(i[0]["종목명"], i[2], i[0], "\n")
	plt.legend(loc=1)
	plt.show()

ssss = []
try:
	start_date = "20180301"
	for i in range(180):
		current_data, start_date, end_date = get_web_data(start_date, next_timedelta=1)
		for ticker in current_data:
			l = np.array(current_data[ticker]["거래량"]).astype(int)
			m = np.mean(l)
			if m==0:
				continue
			else:
				indexed_l = l/m
				if indexed_l[0]>=3 and (ticker in wallet):
					denominator = wallet.pop(ticker, None)
					current = int(current_data[ticker]["시가"])
					result.append(100*(current-denominator)/denominator)
				elif np.count_nonzero(indexed_l>=3)>=1:
					pass
				elif np.count_nonzero((indexed_l[:-1]-indexed_l[1:])<0)>=8 and (ticker not in wallet):
					wallet[ticker] = int(current_data[ticker]["종가"])
		men = np.mean(result) if result else 0
		ssss.append(men)
		print(start_date, len(result), men)
		print()
		start_date = (datetime.datetime.strptime(start_date, "%Y%m%d") + datetime.timedelta(days=1)).strftime("%Y%m%d")
		
	with open("data/result.txt",'w') as f:
		json.dump(result, f, indent=4, ensure_ascii=False)
		
	with open("data/ssss.txt",'w') as f:
		json.dump(ssss, f, indent=4, ensure_ascii=False)
except:
	print(traceback.format_exc())
	print(start_date, result, ssss)
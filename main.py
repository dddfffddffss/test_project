import datetime
import json
import traceback
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

import sub.data as data

matplotlib.rcParams['font.family'] ='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] =False

def ddd():
	#ksq_pool = {'112240', '151910', '73490', '19590', '48870', '78350', '65450', '30530', '225650', '37440', '42500', '900130', '130500', '66900', '64260', '121890', '195990', '41190', '900110', '6140', '101670', '111870', '58400', '215200', '205470', '171010', '93380', '95300', '217820', '187790', '54920', '215100', '25870', '220260', '224110', '134580', '36710', '91590', '45340', '115500', '91580', '214680', '217600', '60230', '65650', '204440', '32580', '54340', '47920', '42370', '45660', '214310', '114190', '119500', '68930', '47770', '11320', '194610', '32080', '21045', '215480', '50890', '26910', '43360', '53160', '2680', '84180', '60250', '900090', '49120', '37070', '25270', '31510', '80010', '150840', '208350', '106080', '126640', '35610', '119860', '123040', '204840', '86830', '17510', '208370', '226350', '214870', '80580', '219550', '40610', '10470', '187270', '30350', '32820', '222810', '218410', '13810', '72950', '66910', '142280', '42600', '131290', '98120', '139670', '14200', '24830', '37330', '38460', '43590', '115610', '218150', '17650', '198440', '2290', '150900', '19770', '25440', '950110', '105330', '104040', '224060', '36090', '45520', '37400', '208870', '219860', '52270', '101390', '39740', '217270', '149980', '94190', '89890', '54040', '36500', '67730', '39240', '53610', '193250', '131390', '222080', '65950', '90150', '1000', '7530', '140520', '32860', '60570', '208640', '10240', '79170', '208140', '207720', '100030', '32280', '48470', '59210', '54950', '136510', '47080', '49470', '191410', '14470', '59120', '232140', '203650', '53290', '130580', '123570', '96690', '86250', '9780', '153490', '215790', '207760', '225430', '101170', '46110', '215580', '17250', '25950', '12860', '53060', '94970', '69410', '91970', '7770', '37230', '81150', '40300', '54540', '38950', '131370', '102120', '60380', '134780', '33540', '77280', '225590', '89150', '92300', '32960', '21650', '222420', '138610'}
	stk_pool = {'016740', '001529', '118000', '015260', '083610', '013367', '005620', '010660', '001020', '099350', '001290', '000327', '020120', '024900', '005740', '000725', '001067', '006740', '003010', '017550', '159650', '011230', '002840', '248170', '012280', '011155', '002995', '144620', '071970', '012205', '083420', '013700', '011700', '004985', '011300', '009470', '099340', '000545', '002250', '105840', '019490', '001420', '172580', '014910', '032350', '004200', '001515', '015020', '083620', '004415', '000040', '023800', '001065', '140890', '002450', '009070', '011280', '002000', '003960', '012800', '019170', '083370', '000075', '006340', '004410', '136490', '101140', '027970', '009190', '101530', '004565', '010145', '002140', '133820', '001260', '004310', '001799', '003060', '003465', '005030', '003535', '009140', '001270', '006890', '000227', '027410', '000970', '005745', '025890', '004987', '002787', '001140', '085310', '002355', '003580', '004989', '103590', '012600', '002785', '004720', '000220', '001620', '000300', '007340', '001070', '010580', '019175', '007540', '005390', '006345', '092220', '090370', '002410', '023960', '005725', '002870', '128820', '004100', '010640', '004270', '002780', '084670', '004365', '001755', '145210', '002880', '145995', '058650', '083570', '069730', '008355', '000325', '000225', '001525', '002150', '090355', '004545', '001745', '010420', '090080', '001527', '153360', '021820', '134790', '002005', '093240', '007575', '023450', '010770', '013520', '037270', '002760', '083380', '004105', '077970', '003415', '005980', '155660', '014990', '000590', '013360', '002720', '016710', '000547'}
	wallet, result, ssss={}, [], []
	dh = data.data_handler(start_date = "20180308", analysis_period=10)
	for _ in range(250):
		current_data, start_date = dh.get_today_data()
		current_data = {k: v for k, v in current_data.items() if k in stk_pool}
		for ticker in current_data:
			l = np.array(current_data[ticker]["거래량"]).astype(int)
			m = np.mean(l)
			if m==0:
				continue
			else:
				indexed_l = l/m
				if indexed_l[0]>=8 and (ticker in wallet):
					denominator = wallet.pop(ticker, None)
					current = int(current_data[ticker]["종가"])
					result.append(100*(current-denominator)/denominator)
				elif np.std(indexed_l)<1:
					wallet[ticker] = int(current_data[ticker]["종가"])

		men = np.mean(result) if result else 0
		ssss.append(men)
		print(start_date, len(result), men)
		print(len(wallet))
		print()
		if _!=179: dh.fetch_next_data()
ddd()

def find_pool():
	wallet1, wallet2, result, ssss=set(), set(), [], []
	dh = data.data_handler(start_date = "20170308", analysis_period=10)
	for _ in range(250):
		current_data, start_date = dh.get_today_data()
		for ticker in current_data:
			l = np.array(current_data[ticker]["거래량"]).astype(int)
			m = np.mean(l)
			if m==0:
				continue
			else:
				indexed_l = l/m
				if indexed_l[0]>=8 and (ticker not in wallet1):
					wallet1.add(ticker)
				elif indexed_l[0]>=8 and (ticker not in wallet2):
					print(indexed_l)
					wallet2.add(ticker)
		print(start_date, wallet2)
		print()
		if _!=179: dh.fetch_next_data()
#find_pool()

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

def final_star():
	wallet, result={}, []
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
					if indexed_l[0]>=5 and (ticker in wallet):
						denominator = wallet.pop(ticker, None)
						current = int(current_data[ticker]["시가"])
						result.append(100*(current-denominator)/denominator)
					elif np.count_nonzero(indexed_l>=5)>=1:
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
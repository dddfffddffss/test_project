import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import sub.data as data

matplotlib.rcParams['font.family'] ='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] =False

def make_start_data():
    with open("data/data.txt",'w') as f:
        d, startdate, enddate = data.start_local_data()
        json.dump(d, f, indent=4, ensure_ascii=False)

def get_local_data():
    return data.get_local_data()

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
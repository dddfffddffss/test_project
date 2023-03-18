import json
import sub.data as data

with open("data/data.txt",'w') as f:
    json.dump(data.start_local_data("20230314"), f, ensure_ascii=False, indent=4)
import os
import sys
import csv
import pandas as pd

# CSV 파일 Merge
csv_list = []
instance_list_data = {}

for csv in os.listdir('./'):
    if ".csv" in csv:
        csv_list.append(csv)

for csv_file in csv_list:
    instance_list_data[csv_file] = pd.read_csv(f'{csv_file}')

all_data = pd.concat(instance_list_data.values(), ignore_index=True)
all_data.to_csv('total_instance_type_list_count.csv', index=False)
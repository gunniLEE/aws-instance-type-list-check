import os
import sys
import csv

import pandas as pd
from collections import Counter


instance_list = [['인스턴스 타입', '플랫폼', '개수', '리전', '온디멘드 시간당 비용', 'Standard RI(1년) 할인율','Converterble RI(1년) 할인율',
                  'Standard RI(3년) 할인율', 'Converterble RI(3년) 할인율', 'Instance Savings Plan(1년) 할인율', 'Compute Savings Plan(1년) 할인율',
                  'Instance Savings Plan(1년) 할인율', 'Compute Savings Plan(3년) 할인율']]


#CSV 파일 생성
def open_csv(file_name):
    file_name += '.csv'
    with open(file_name, 'r') as f:
        data_list = csv.reader(f)
        return list(data_list)

def write_csv(file_name, data_list):
    file_name += '_인스턴스_타입별_리스팅.csv'
    with open(file_name, 'w', newline='') as f:
        csv_obj = csv.writer(f, delimiter=',')
        csv_obj.writerows(data_list)


# 파일에서 인스턴스 타입 가져오기
with open(sys.argv[1], "r") as f:
    instance_types = f.read().splitlines()

# 인스턴스 타입 개수 계산
instance_type_counts = Counter(instance_types)

if len(instance_type_counts) != 0:
    print(sys.argv[2] + " >>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Count\tName\tPlatform\tRegion")
    print("-----\t----\t----\t----")

    # 결과 출력
    for instance_type, count in instance_type_counts.items():
        instance_types = instance_type.split('\t')
        instance_types.append(count)
        instance_types.append(sys.argv[2])

        instance_list.append(instance_types)


        if instance_list != []:
            write_csv(sys.argv[2], instance_list)
            print(f"{count}\t{instance_type}\t{sys.argv[2]}")
        else:
            pass

    print('\n')

else:
    print(sys.argv[2] + " region dosen't have instance.\n")

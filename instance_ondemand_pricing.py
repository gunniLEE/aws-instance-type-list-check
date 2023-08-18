import csv
import json
import subprocess
import pandas as pd

pd.set_option('mode.chained_assignment',  None)

#total instance list csv 파일 조회
type_df=pd.read_csv('./total_instance_type_list_count.csv')


# AWS CLI를 사용하여 할인 정보 가져오기
for num in range(len(type_df)):
    command = f'aws pricing get-products --service-code AmazonEC2 --region us-east-1 --filters \
            "Type=TERM_MATCH,Field=instanceType,Value={type_df["인스턴스 타입"][num]}" \
            "Type=TERM_MATCH,Field=regionCode,Value={type_df["리전"][num]}" \
            "Type=TERM_MATCH,Field=operatingSystem,Value={type_df["플랫폼"][num]}" \
            "Type=TERM_MATCH,Field=preInstalledSw,Value=NA"'
    
    result = json.loads(subprocess.check_output(command, shell=True).decode('utf-8'))

    for product in result['PriceList']:
        terms = json.loads(product)
        on_demand = terms['terms']['OnDemand']
        for term_key in on_demand:
            term = on_demand[term_key]
            price_dimensions = term['priceDimensions']
            for price_dimension_key in price_dimensions:
                price_dimension = price_dimensions[price_dimension_key]
                if "On Demand {} {}".format(type_df['플랫폼'][num], type_df["인스턴스 타입"][num]) in price_dimension['description']:
                    type_df['온디멘드 시간당 비용'][num] = price_dimension['pricePerUnit']['USD']

duration = ["1년","3년"]
bill_opt = ['선결제 없음', '부분 선결제', '전체 선결제']

delete_row = len(type_df)

for num in range(len(type_df)):
    row = type_df.loc[num]
    for bill_opts in bill_opt:
        row['결제 옵션'] = bill_opts
        for durations in duration:
            row['적용 기간'] = durations
            new_row_data = [row['인스턴스 타입'],row['플랫폼'], row['개수'],row['리전'],row['온디멘드 시간당 비용'],
                            row['적용 기간'],row['결제 옵션'],row['Standard RI 할인율'],row['Converterble RI 할인율'], 
                            row['Instance Savings Plan 할인율'], row['Compute Savings Plan 할인율']]
            type_df.loc[len(type_df)] = new_row_data

type_df = type_df.drop(type_df.index[0:delete_row])

## save to csv
type_df.to_csv('total_instance_type_pricing.csv', index=False)

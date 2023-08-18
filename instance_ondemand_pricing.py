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

## save to csv
type_df.to_csv('total_instance_type_list_count.csv', index=False)

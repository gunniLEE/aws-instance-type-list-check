# aws instance type list check

AWS 전체 리전에 대해 인스턴스 타입 개수 체크 & 타입 별 온디맨드 요금 정보 수집

## instance_list.py
AWS 전체 리전에 대한 인스턴스 타입 개수 체크

## process.py
인스턴스 체크 후 csv 파일 형태로 후처리

## instance_ondemand_pricing.py
리전,운영체제,인스턴스 타입에 따른 온디멘드 가격 정보 수집

## script.sh
```
cd aws-api/
./script.sh {$profile_name}
```

## result
total_instance_type_pricing.csv 형태로 출력

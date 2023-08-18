#!/bin/sh

for var in $(aws ec2 describe-regions --query "Regions[].{Name:RegionName}" --output text --profile land-devops)
do

#echo "==================================================$var==============================================================="
aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceType,PlatformDetails]" --output text --region $var --profile land-devops > instance_types_$var.txt
python3 instance_list.py instance_types_$var.txt $var

done

rm -rf *.txt

python3 process.py
python3 instance_ondemand_pricing.py

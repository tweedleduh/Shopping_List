import boto3
import json

file = open('shopping_list_1643893105.json')
data = json.load(file)

for i in data['shopping_list']:
    print(i['name'])
    print(i['department'])

file.close

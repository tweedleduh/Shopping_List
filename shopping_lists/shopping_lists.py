import authFile_creds as auth
import boto3
import csv
import json
import os
import pprint
from shoppingInstances import shopping as si



################################################ Config ##########################################
key_id = auth.aws_key_id()
secret = auth.aws_access_key_id()

s3_Bucket = 'shopping-guru'

csv_List = []


try:
    s3 = boto3.client('s3', aws_access_key_id = key_id, aws_secret_access_key = secret)
    print("****************** successfully connected to s3 ***********************")
except NoCredentialsError:
    print("bad creds try something else")




for list in si:
    
    print("\n******************* Accessing List **************************\n")
    file = open(list)
    data = json.load(file)
    reformatted_List_Name = list.replace('.json', '.csv')
    print(f"Replaced {list} name with {reformatted_List_Name} ")

    # append to list for later access and validation
    csv_List.append(reformatted_List_Name)

    # getting access to list object and storing keys as headers
    shopping_list = data['shopping_list']
    print(shopping_list)
    headers = shopping_list[0].keys()

    #using reformatted file name, to move data into csv file
    csv_Shopping_List = open(reformatted_List_Name, 'w')
    csv_writer = csv.writer(csv_Shopping_List)
    csv_writer.writerow(headers)
    
    print("********************* Moving to items within List *******************")
    
    #while file is open, loop through items in shopping list, and write each line to open csv
    for item in shopping_list:
        #print(f"The number values attached to item:  {len(item)}")
        csv_writer.writerow(item.values())
    
    # Displaying to user program results    
    print("Program wrote to ", reformatted_List_Name )
    #print(os.stat(reformatted_List_Name))
    #file.close()


print(csv_List)
csv_List.sort()
print(csv_List)
print("************************** Uploading files to s3 *******************")
file_Number = 1
for file in csv_List:
    print(file)
    print(f"We're on file #: {file_Number}")
    #file_size = os.stat(file)
    #print(f"The file size is {file_size}")
    with open(file):
        file_size = os.stat(file)
        #print(f"The file size is {file_size}")
        try:
            s3.upload_file(file, s3_Bucket, file)
            print(len(file))
        except:
            print('ran into a problem with list: ', file)
    file_Number += 1

print (f"Number of files written: {len(csv_List)}")
print(f"Endpoint: {s3_Bucket}")

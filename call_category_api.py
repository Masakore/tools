import requests
import argparse
import pandas as pd
import datetime
import json

parser = argparse.ArgumentParser(description='csv to anonymise')
parser.add_argument('file', help='csv file to import', action='store')
args = parser.parse_args()
csv_file = args.file

date = datetime.datetime.now().strftime("%Y-%m-%d")
extraction = date + "T10:05:24.121+0000"
df = pd.read_csv(csv_file, header=None, dtype='object').fillna("")

movement = df[0].astype(str)
amount = df[1].astype(str)
transaction_code = df[2].astype(str)
description = df[3].astype(str)

# print("date", date)
# print("extraction", extraction)
# print("movement", "debit" if movement[0] == "2" else "credit")
# print("amount", amount[0])
# print("tekiyocd", transaction_code[0])

for i, m in enumerate(movement):
  params = json.dumps({
    "source": {
      "name": "OKB"
    },
    "transactions": [
      {
        "date": date,
        "extraction": extraction,
        "description": description[i],
        "movement": "debit" if m == "2" else "credit",
        "currency": "JPY",
        "amount": 1000,
        "custom_fields":[
          {
            "name": "tekiyocd",
            "value": transaction_code[i]
          }
        ]
      }
    ]
  })
  # print(params)

  response = requests.post(
    "http://127.0.0.1:8080/fpm/api/v4/categorize", 
    data=params, 
    headers={
      "Content-Type": "application/json",
      "charset": "UTF-8"
    }
  )
  #print(response.json())
  print(response.status_code)

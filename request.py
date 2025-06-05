import pandas as pd
import requests
from utils.utility import *

def send_request(payload: str):
    '''
    Send one or more requests to the server.
    '''
    response = requests.post('http://127.0.0.1:' + str(PORT) + '/api/predict', json=payload)
    return response


# Load dataset
DIR_INPUT='data/data' 

BEGIN_DATE = "2018-08-15"
END_DATE = "2018-08-31"
BEGIN_DATE_IN_DATETIME = datetime.strptime(BEGIN_DATE, '%Y-%m-%d')

transactions_df = read_files(DIR_INPUT, BEGIN_DATE, END_DATE)
print("{0} transactions loaded, containing {1} fraudulent transactions".format(len(transactions_df),transactions_df.TX_FRAUD.sum()))
transactions_df = transactions_df[transactions_df.TX_FRAUD == 0]
transactions_df['TX_DATETIME'] = transactions_df['TX_DATETIME'].astype(str)

# test_df = pd.read_csv('test.csv')
# test_df = test_df[test_df.TX_FRAUD == 1]
# print(test_df)
# print(test_df.dtypes)

length = len(transactions_df)
# print(length)
# print(transactions_df['TX_FRAUD'])
# print(transactions_df.dtypes)

predictions = []
for i in range(1):
    features_dict = transactions_df.iloc[i].to_dict() # extract the row's features as a dict
    payload = {'features': features_dict} # Create JSON payload with named features
    response = send_request(payload).json()
    print(response)
    predictions.append(response['fraud'])

print(f'All predictions: {predictions}')
print(f'Accuracy: {predictions.count(True) / length}')
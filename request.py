import pandas as pd
import requests
from utils.utility import *
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def send_request(payload: str):
    response = requests.post('http://127.0.0.1:' + str(PORT) + '/api/predict', json=payload)
    return response


# Load dataset
DIR_INPUT='data/data' 

BEGIN_DATE = "2018-08-15"
END_DATE = "2018-08-31"
BEGIN_DATE_IN_DATETIME = datetime.strptime(BEGIN_DATE, '%Y-%m-%d')

transactions_df = read_files(DIR_INPUT, BEGIN_DATE, END_DATE)
print("{0} transactions loaded, containing {1} fraudulent transactions".format(len(transactions_df),transactions_df.TX_FRAUD.sum()))
# transactions_df = transactions_df[transactions_df.TX_FRAUD == 0]
transactions_df['TX_DATETIME'] = transactions_df['TX_DATETIME'].astype(str)

# test_df = pd.read_csv('test.csv')
# test_df = test_df.sample(frac=1).reset_index(drop=True)

# test_df = test_df[test_df.TX_FRAUD == 1]
# length = len(test_df)
# print(length)
# print(test_df)
# print(test_df.dtypes)

# length = len(transactions_df)
# print(length)
# print(transactions_df['TX_FRAUD'])
# print(transactions_df.dtypes)

predictions = []
y_true = []
for i in range(100):
    features_dict = transactions_df.iloc[i].to_dict() # extract the row's features as a dict
    y_true.append(features_dict['TX_FRAUD'])
    payload = {'features': features_dict} # Create JSON payload with named features
    response = send_request(payload).json()
    # print(response)
    predictions.append(response['fraud'])
    break

print(f'All predictions: {predictions}')
print(f'True Labels: {y_true}')

accuracy = accuracy_score(y_true, predictions)
precision = precision_score(y_true, predictions)
recall = recall_score(y_true, predictions)
f1 = f1_score(y_true, predictions)
cm = confusion_matrix(y_true, predictions)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:\n", cm)

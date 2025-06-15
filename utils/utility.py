import json
from datetime import datetime
import pandas as pd
import os

# the features used to predict fraud
INPUT_FEATURES = [
    'TX_AMOUNT', 'TX_DURING_WEEKEND', 'TX_DURING_NIGHT', 'CUSTOMER_ID_NB_TX_1DAY_WINDOW',
    'CUSTOMER_ID_AVG_AMOUNT_1DAY_WINDOW', 'CUSTOMER_ID_NB_TX_7DAY_WINDOW',
    'CUSTOMER_ID_AVG_AMOUNT_7DAY_WINDOW', 'CUSTOMER_ID_NB_TX_30DAY_WINDOW',
    'CUSTOMER_ID_AVG_AMOUNT_30DAY_WINDOW', 'TERMINAL_ID_NB_TX_1DAY_WINDOW',
    'TERMINAL_ID_RISK_1DAY_WINDOW', 'TERMINAL_ID_NB_TX_7DAY_WINDOW',
    'TERMINAL_ID_RISK_7DAY_WINDOW', 'TERMINAL_ID_NB_TX_30DAY_WINDOW',
    'TERMINAL_ID_RISK_30DAY_WINDOW'
]

FRAUD_THRESHOLD = 0.8
SUSPICIOUS_THRESHOLD = 0.5
PORT = 5000

# APIs for fetching data
PREDICT_API = '/api/predict'
TRANSACTIONS_API = '/api/transactions'
FRAUDRATE_API = '/api/fraud-rate'

# APIs for fetching UI
DASHBOARD_API = '/dashboard'

def log_transaction(tx_id, tx_amount, tx_datetime, is_fraud, fraud_score):
    log_entry = {
        "id": tx_id,
        "amount": tx_amount,
        "time": tx_datetime,
        "fraud": is_fraud,
        "fraud_score": fraud_score
    }

    with open("logs/transactions.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def get_latest_transactions(n_transactions=None, log_path='logs/transactions.log'):
    """
    Read transactions.log and return a DataFrame of recent transactions.

    Args:
        log_path: Path to the log file.
        n_transactions: number of the latest transactions to return

    Returns:
        pd.DataFrame: a DataFrame with recent transactions.
    """

    records = []
    with open(log_path, 'r') as f:
        for line in f:
            try:
                record = json.loads(line.strip())
                records.append(record)
            except json.JSONDecodeError:
                continue  # skip invalid lines

    if not records:
        return pd.DataFrame(columns=["id", "amount", "time", "fraud"])

    if n_transactions == None:
        df = pd.DataFrame(records)
    else:
        df = pd.DataFrame(records).tail(n_transactions)

    return df


def read_files(dir_input, begin_date, end_date):
    data_list = []
    all_files = [os.path.join(dir_input, f) for f in os.listdir(dir_input) if f>=begin_date+'.pkl' and f<=end_date+'.pkl']
    
    for filename in all_files:
        try:
            df = pd.read_pickle(filename)
            data_list.append(df)
            del df
        except:
            continue
    return pd.concat(data_list, ignore_index=True)
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from utils.utility import *
import json
from datetime import datetime

app = Flask(__name__)


# Load trained model
with open('models/best_random_forest.pkl', 'rb') as f:
    model = pickle.load(f)


# load data scaler
with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)


def validate_features(features):
    '''
    Check if the features of the data are valid.
    '''
    if features is None:
            return jsonify({'error': 'Missing "features" key in request'}), 400

    if not isinstance(features, dict):
        return jsonify({'error': 'Input "features" must be a dictionary of named feature values'}), 400

    # Check all expected features are present
    missing_features = [f for f in INPUT_FEATURES if f not in features]
    if missing_features:
        return jsonify({'error': f'Missing features: {missing_features}'}), 400

    return None


@app.route(PREDICT_API, methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)

        # get all the features of the data received from request. this data has 23 features
        features = data.get('features', None)

        # validate the data and the data features
        validation_response = validate_features(features)
        if validation_response:
            return validation_response

        # convert to DataFrame, drop all irrelevant features. this DataFrame has 15 features from INPUT_FEATURES
        input_df = pd.DataFrame([features])[INPUT_FEATURES]

        # Predict
        prediction = model.predict(input_df)[0]
        print(model.predict_proba(input_df)[0, 1])
        print(prediction)
        is_fraud = bool(prediction)

        # log the transaction for later analysis
        log_transaction(features['TRANSACTION_ID'], features['TX_AMOUNT'], features['TX_DATETIME'], is_fraud)

        return jsonify({'fraud': is_fraud})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route(DASHBOARD_API, methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route(TRANSACTIONS_API, methods=['GET'])
def return_latest_transactions():
    with open('logs/transactions.log') as f:
        txs = [json.loads(line) for line in f.readlines()]

    total_tx = len(txs)
    frauds = sum(1 for tx in txs if tx['fraud'] == 1)
    fraud_rate = round(frauds / total_tx * 100, 2) if total_tx else 0

    latest_transactions = sorted(
        [tx for tx in txs if tx['fraud'] == 1],
        key=lambda tx: datetime.strptime(tx['time'], "%Y-%m-%d %H:%M:%S"),  # or your exact format
        reverse=True
    )[:10]

    return jsonify({
        'total_tx': total_tx,
        'frauds': frauds,
        'fraud_rate': fraud_rate,
        'latest_transactions': latest_transactions
    })


@app.route(FRAUDRATE_API)
def fraud_rate():
    # Fetch latest fraud rate
    df = get_latest_transactions()
    df['date'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d')
    fraud_rate = df.groupby('date')['fraud'].mean()
    return jsonify(labels=list(fraud_rate.index), values=list(fraud_rate.values))


if __name__ == '__main__':
    app.run(debug=True, port=PORT) 
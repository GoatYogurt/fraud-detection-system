import pandas as pd
import pickle
from utils.utility import INPUT_FEATURES, read_files
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score, precision_score, recall_score, confusion_matrix
import datetime


with open('models/best_random_forest.pkl', 'rb') as f:
    model = pickle.load(f)


with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)


DIR_INPUT='data/data'

BEGIN_DATE = "2018-09-15"
END_DATE = "2018-09-31"
BEGIN_DATE_IN_DATETIME = datetime.datetime.strptime(BEGIN_DATE, '%Y-%m-%d')

transactions_df = read_files(DIR_INPUT, BEGIN_DATE, END_DATE)
print("{0} transactions loaded, containing {1} fraudulent transactions".format(len(transactions_df),transactions_df.TX_FRAUD.sum()))
transactions_df['TX_DATETIME'] = transactions_df['TX_DATETIME'].astype(str)
y_true = transactions_df['TX_FRAUD']
transactions_df = scaler.transform(transactions_df[INPUT_FEATURES])


# test_df = pd.read_csv('test.csv')

y_prob = model.predict_proba(transactions_df)[:,1]

# print(y_pred)
# print(roc_auc_score(y_true, y_pred))

best_f1 = 0
best_threshold = 0
thresholds = [0.7, 0.8, 0.9]

for t in thresholds:
    y_pred = (y_prob >= t).astype(int)
    f1 = f1_score(y_true, y_pred)
    if f1 > best_f1:
        best_f1 = f1
        best_threshold = t

print(f"Best threshold by F1: {best_threshold:.3f}, F1 score: {best_f1:.3f}")



print("Accuracy:", accuracy_score(y_true, y_prob >= best_threshold))
print("Precision:", precision_score(y_true, y_prob >= best_threshold))
print("Recall:", recall_score(y_true, y_prob >= best_threshold))
print("F1 Score:", f1_score(y_true, y_prob >= best_threshold))
print("Confusion Matrix:\n", confusion_matrix(y_true, y_prob >= best_threshold))
print("ROC AUC: ", roc_auc_score(y_true, y_prob))



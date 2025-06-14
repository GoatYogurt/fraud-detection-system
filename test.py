import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from utils.utility import INPUT_FEATURES
from sklearn.metrics import roc_auc_score


with open('models/best_random_forest.pkl', 'rb') as f:
    model = pickle.load(f)

test_df = pd.read_csv('test.csv')

y_true = test_df['TX_FRAUD']
y_pred = model.predict_proba(test_df[INPUT_FEATURES])[:,1]
# print(y_pred)
print(roc_auc_score(y_true, y_pred))

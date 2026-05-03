import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier

# load data
df = pd.read_csv('Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv')

# target
X = df.drop(columns=['default_flag'])
y = df['default_flag']

# drop kolom yang ga dipakai
X = X.drop(columns=['risk_score', 'transaction_date', 'location', 'product_category'], errors='ignore')

# split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# kolom
num_cols = X_train.select_dtypes(include='number').columns.tolist()
cat_cols = X_train.select_dtypes(include='object').columns.tolist()

# preprocessing (NO REMAINDER)
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
])

# model
model = Pipeline([
    ('preprocess', preprocessor),
    ('model', GradientBoostingClassifier())
])

# train
model.fit(X_train, y_train)

# save
joblib.dump(model, 'classification_model.pkl')
joblib.dump(0.2, 'threshold.pkl')

print("MODEL FIXED & SAVED")
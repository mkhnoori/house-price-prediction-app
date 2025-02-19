import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Define the features we want to use
FEATURES = [
    'Lot Area', 'Overall Qual', 'Year Built', 'Total Bsmt SF',
    '1st Flr SF', 'Full Bath', 'Gr Liv Area', 'Garage Cars'
]

# Load the dataset
data = pd.read_csv('AmesHousing.csv')

# Separate features and target
X = data[FEATURES]
y = data['SalePrice']

# Create preprocessor
numeric_features = FEATURES
preprocessor = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Preprocess data
X_preprocessed = preprocessor.fit_transform(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f'MAE: ${mae:,.2f}')
print(f'RMSE: ${rmse:,.2f}')

# Save model and preprocessor
joblib.dump(model, 'house_price_model.pkl')
joblib.dump(preprocessor, 'preprocessor.pkl')

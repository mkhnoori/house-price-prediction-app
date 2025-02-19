                 # step 1 - Load the Data
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Load the dataset
data = pd.read_csv('AmesHousing.csv')

# Seperate the feature columns and the target column 'SalePrice'
X = data.drop(columns=['SalePrice'])
y = data['SalePrice']

                # Step 2 - Preprocess the Data
# Identify numeric and categorical columns
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X.select_dtypes(include=['object']).columns

# Create pipelines for the numeric and categorical data
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Combine the pipelines using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

# Use the preprocessor on the data
X_preprocessed = preprocessor.fit_transform(X)

                  # Step 3 - Splitting Data
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)


                  # step 4 - choosing a model
from sklearn.linear_model import LinearRegression

# Initialize the model
model = LinearRegression()


                  # step 5 - Training and Evaluating the Model
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import numpy as np
# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f'MAE: {mae}')
print(f'RMSE: {rmse}')


              # step 6 - Save the model
model_file = 'house_price_model.pkl'
joblib.dump(model, model_file)


# Saving the Preprocessor
import joblib

# Save the preprocessor
preprocessor_file = 'preprocessor.pkl'  # Save path for the preprocessor
joblib.dump(preprocessor, preprocessor_file)


                 # step 7 - Building a Streamlit App
import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the trained model
model = joblib.load('house_price_model.pkl')

# Load the preprocessor
preprocessor = joblib.load('preprocessor.pkl')

# Define the input fields
st.title('House Price Prediction')

# Input fields
# Here, more complex features (strings/categorical) should be made into st.selectbox etc.

# Example numeric fields for simplicity:
lot_area = st.number_input('Lot Area', value=5000)
overall_qual = st.number_input('Overall Qual', min_value=1, max_value=10, value=5)
year_built = st.number_input('Year Built', value=1990)
total_bsmt_sf = st.number_input('Total Bsmt SF', value=1000)
first_flr_sf = st.number_input('1st Flr SF', value=1000)
full_bath = st.number_input('Full Bath', value=2)
gr_liv_area = st.number_input('Gr Liv Area', value=1500)
garage_cars = st.number_input('Garage Cars', value=1)
# You need to add more fields for all the mentioned features in a similar way here...

# Create a DataFrame for the input features
# Make sure the names of input fields match the ones expected by the preprocessor
input_data = pd.DataFrame({
    'Central Air': ['Y'],  # Example of default input for categorical feature
    'House Style': ['1Story'],  # Just examples for missing fields
    'Bsmt Full Bath': [1],
    'Kitchen Qual': ['TA'],
    'Bsmt Qual': ['TA'],
    'Exter Cond': ['TA'],
    'Neighborhood': ['NAmes'],
    'Garage Qual': ['TA'],
    'Bedroom AbvGr': [3],
    'MS Zoning': ['RL'],
    'Foundation': ['PConc'],
    'Misc Val': [0],
    'Fireplaces': [0],
    'Bsmt Unf SF': [400],
    'Low Qual Fin SF': [0],
    'Land Contour': ['Lvl'],
    'Bldg Type': ['1Fam'],
    'Garage Cond': ['TA'],
    'Bsmt Cond': ['TA'],
    'Alley': ['NA'],
    'Condition 2': ['Norm'],
    'Condition 1': ['Norm'],
    'Wood Deck SF': [0],
    'Overall Cond': [5],
    'Lot Config': ['Inside'],
    'Screen Porch': [0],
    'Lot Shape': ['Reg'],
    '3Ssn Porch': [0],
    'Fence': ['NA'],
    'Exterior 1st': ['VinylSd'],
    'Land Slope': ['Gtl'],
    'Heating QC': ['Ex'],
    'Street': ['Pave'],
    'Utilities': ['AllPub'],
    'MS SubClass': [20],
    'Exterior 2nd': ['VinylSd'],
    'Roof Style': ['Gable'],
    'Open Porch SF': [20],
    'Bsmt Exposure': ['No'],
    'Kitchen AbvGr': [1],
    'Paved Drive': ['Y'],
    'Year Remod/Add': [2000],
    'Garage Area': [500],
    'Pool QC': ['NA'],
    'Electrical': ['SBrkr'],
    'Roof Matl': ['CompShg'],
    'Sale Condition': ['Normal'],
    'Mo Sold': [6],
    'Misc Feature': ['NA'],
    'Bsmt Half Bath': [0],
    'Sale Type': ['WD'],
    'Half Bath': [1],
    'Garage Type': ['Attchd'],
    'Heating': ['GasA'],
    'BsmtFin SF 1': [500],
    'Yr Sold': [2010],
    'Functional': ['Typ'],
    'Pool Area': [0],
    'Exter Qual': ['TA'],
    'Garage Finish': ['Unf'],
    'Mas Vnr Type': ['None'],
    'Mas Vnr Area': [0],
    'Garage Yr Blt': [1990],
    'Enclosed Porch': [0],
    'TotRms AbvGrd': [6],
    'Order': [1],
    'Fireplace Qu': ['NA'],
    'BsmtFin Type 2': ['NA'],
    'PID': [0],  # Note this should be handled appropriately as it may not be in preprocessing
    'BsmtFin Type 1': ['GLQ'],
    'Lot Frontage': [60],
    'BsmtFin SF 2': [0],
    '2nd Flr SF': [0],

    # Features defined by the user
    'Lot Area': [lot_area],
    'Overall Qual': [overall_qual],
    'Year Built': [year_built],
    'Total Bsmt SF': [total_bsmt_sf],
    '1st Flr SF': [first_flr_sf],
    'Full Bath': [full_bath],
    'Gr Liv Area': [gr_liv_area],
    'Garage Cars': [garage_cars],
})

# Preprocess the input features
input_features_preprocessed = preprocessor.transform(input_data)

# Predict and display the output
if st.button('Predict'):
    prediction = model.predict(input_features_preprocessed)
    st.write(f'Predicted House Price: ${prediction[0]:,.2f}')

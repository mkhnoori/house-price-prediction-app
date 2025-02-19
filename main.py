import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load model and preprocessor
model = joblib.load('models/house_price_model.pkl')
preprocessor = joblib.load('models/preprocessor.pkl')

st.title('House Price Prediction')

# Input fields for user
lot_area = st.number_input('Lot Area', value=5000)
overall_qual = st.number_input('Overall Qual', min_value=1, max_value=10, value=5)
year_built = st.number_input('Year Built', value=1990)
total_bsmt_sf = st.number_input('Total Bsmt SF', value=1000)
first_flr_sf = st.number_input('1st Flr SF', value=1000)
full_bath = st.number_input('Full Bath', value=2)
gr_liv_area = st.number_input('Gr Liv Area', value=1500)
garage_cars = st.number_input('Garage Cars', value=1)

# Convert input into DataFrame
input_data = pd.DataFrame({
    'Lot Area': [lot_area],
    'Overall Qual': [overall_qual],
    'Year Built': [year_built],
    'Total Bsmt SF': [total_bsmt_sf],
    '1st Flr SF': [first_flr_sf],
    'Full Bath': [full_bath],
    'Gr Liv Area': [gr_liv_area],
    'Garage Cars': [garage_cars]
})

# Preprocess input
input_features_preprocessed = preprocessor.transform(input_data)

# Predict
if st.button('Predict'):
    prediction = model.predict(input_features_preprocessed)
    st.write(f'Predicted House Price: ${prediction[0]:,.2f}')

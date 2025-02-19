import pytest
import numpy as np
from models.train_model import *

def test_model_training():
    # Test data preparation
    X = np.array([[1000, 7, 2000, 1500, 1500, 2, 2000, 2]])
    y = np.array([250000])
    
    # Create and train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Make prediction
    prediction = model.predict(X)
    
    # Assert prediction is reasonable
    assert prediction[0] > 0
    assert isinstance(prediction[0], (int, float))

def test_feature_preprocessing():
    # Test data
    test_data = {
        'Lot Area': [1000],
        'Overall Qual': [7],
        'Year Built': [2000],
        'Total Bsmt SF': [1500],
        '1st Flr SF': [1500],
        'Full Bath': [2],
        'Gr Liv Area': [2000],
        'Garage Cars': [2]
    }
    df = pd.DataFrame(test_data)
    
    # Create preprocessor
    preprocessor = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Fit and transform
    processed_data = preprocessor.fit_transform(df)
    
    # Assertions
    assert processed_data.shape == (1, 8)
    assert not np.isnan(processed_data).any()

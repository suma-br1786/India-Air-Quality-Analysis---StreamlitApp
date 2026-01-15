import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "green"
    elif aqi <= 100:
        return "Satisfactory", "lightgreen"
    elif aqi <= 200:
        return "Moderate", "yellow"
    elif aqi <= 300:
        return "Poor", "orange"
    elif aqi <= 400:
        return "Very Poor", "red"
    else:
        return "Severe", "darkred"

def app():
    st.title("AQI Value & Category Prediction")

    # Generate synthetic dataset (500 samples)
    np.random.seed(42)
    data = pd.DataFrame({
        "PM2.5": np.random.randint(10, 300, 500),
        "PM10": np.random.randint(20, 400, 500),
        "NO2": np.random.randint(0, 100, 500),
        "CO": np.random.uniform(0.1, 3, 500),
        "O3": np.random.randint(0, 200, 500),
    })

    # Create synthetic AQI target with noise
    data["AQI"] = (
        data["PM2.5"] * 0.5 +
        data["PM10"] * 0.3 +
        data["NO2"] * 0.2 +
        data["CO"] * 10 +
        data["O3"] * 0.1 +
        np.random.normal(0, 10, 500)  # noise
    )

    # Features and target
    X = data.drop(columns="AQI")
    y = data["AQI"]

    # Split data 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model on test data
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    st.write(f"### Model performance on test set:")
    st.write(f"R² score: {r2:.3f}")
    st.write(f"RMSE: {rmse:.3f}")

    # User inputs for prediction
    st.header("Enter pollutant values to predict AQI:")
    pm25 = st.number_input("PM2.5 (µg/m³)", min_value=0.0, max_value=500.0, value=50.0)
    pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0, max_value=500.0, value=80.0)
    no2 = st.number_input("NO2 (µg/m³)", min_value=0.0, max_value=200.0, value=20.0)
    co = st.number_input("CO (mg/m³)", min_value=0.0, max_value=10.0, value=0.8)
    o3 = st.number_input("O3 (µg/m³)", min_value=0.0, max_value=300.0, value=20.0)

    if st.button("Predict AQI"):
        input_data = pd.DataFrame([{
            "PM2.5": pm25,
            "PM10": pm10,
            "NO2": no2,
            "CO": co,
            "O3": o3
        }])
        prediction = model.predict(input_data)[0]
        category, color = get_aqi_category(prediction)

        st.success(f"Predicted AQI value: {prediction:.2f}")
        st.markdown(f"<h3 style='color:{color}'>AQI Category: {category}</h3>", unsafe_allow_html=True)

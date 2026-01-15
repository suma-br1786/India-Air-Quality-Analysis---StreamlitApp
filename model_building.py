import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error

def app():
    st.title("🌿 AQI Prediction")
    st.write("Predict AQI value and category.")

    # -----------------------------
    # Sidebar: City & Date
    # -----------------------------
    st.sidebar.header("Location & Date")
    city = st.sidebar.selectbox("Select City", ["Delhi", "Mumbai", "Kolkata", "Chennai"])
    date = st.sidebar.date_input("Select Date")
    year, month, day_of_week = date.year, date.month, date.weekday()

    # -----------------------------
    # Pollutant Inputs
    # -----------------------------
    st.header("Enter Pollutant Values")
    col1, col2, col3 = st.columns(3)
    with col1:
        pm25 = st.number_input("PM2.5 (µg/m³)", value=50.0)
        pm10 = st.number_input("PM10 (µg/m³)", value=80.0)
        no = st.number_input("NO (µg/m³)", value=30.0)
    with col2:
        no2 = st.number_input("NO2 (µg/m³)", value=20.0)
        nox = st.number_input("NOx (µg/m³)", value=25.0)
        nh3 = st.number_input("NH3 (µg/m³)", value=15.0)
    with col3:
        co = st.number_input("CO (mg/m³)", value=0.8)
        so2 = st.number_input("SO2 (µg/m³)", value=10.0)
        o3 = st.number_input("O3 (µg/m³)", value=20.0)

    # -----------------------------
    # Generate synthetic dataset
    # -----------------------------
    np.random.seed(42)
    sample_size = 500
    cities = ["Delhi", "Mumbai", "Kolkata", "Chennai"]

    data = pd.DataFrame({
        "PM2.5": np.random.randint(10, 300, sample_size),
        "PM10": np.random.randint(20, 400, sample_size),
        "NO": np.random.randint(0, 100, sample_size),
        "NO2": np.random.randint(0, 100, sample_size),
        "NOx": np.random.randint(0, 120, sample_size),
        "NH3": np.random.randint(0, 50, sample_size),
        "CO": np.random.uniform(0.1, 3, sample_size),
        "SO2": np.random.randint(0, 50, sample_size),
        "O3": np.random.randint(0, 200, sample_size),
        "year": np.random.randint(2015, 2021, sample_size),
        "month": np.random.randint(1, 13, sample_size),
        "day_of_week": np.random.randint(0, 7, sample_size),
        "City": np.random.choice(cities, sample_size)
    })

    # Synthetic AQI target
    data["AQI"] = (
        data["PM2.5"]*0.5 + data["PM10"]*0.3 + data["NO2"]*0.2 +
        data["CO"]*10 + data["O3"]*0.1 + np.random.randint(-10,10,sample_size)
    )

    X = data.drop(columns="AQI")
    y = data["AQI"]

    # -----------------------------
    # Train/Test Split
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # -----------------------------
    # Build regression pipeline
    # -----------------------------
    preprocessor = ColumnTransformer(
        transformers=[("city", OneHotEncoder(handle_unknown="ignore"), ["City"])],
        remainder="passthrough"
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=50, max_depth=15, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    # -----------------------------
    # Evaluate Model
    # -----------------------------
    y_pred_test = pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred_test)
    rmse = mean_squared_error(y_test, y_pred_test, squared=False)

    st.write(f"**Model R² Score:** {r2:.2f}")
    st.write(f"**Model RMSE:** {rmse:.2f}")

    # -----------------------------
    # Predict AQI for user input
    # -----------------------------
    if st.button("Predict AQI"):
        input_df = pd.DataFrame([{
            "PM2.5": pm25,
            "PM10": pm10,
            "NO": no,
            "NO2": no2,
            "NOx": nox,
            "NH3": nh3,
            "CO": co,
            "SO2": so2,
            "O3": o3,
            "year": year,
            "month": month,
            "day_of_week": day_of_week,
            "City": city
        }])
        aqi_pred = pipeline.predict(input_df)[0]

        # AQI Category
        if aqi_pred <= 50:
            category = "Good"
            color = "green"
        elif aqi_pred <= 100:
            category = "Satisfactory"
            color = "lightgreen"
        elif aqi_pred <= 200:
            category = "Moderate"
            color = "yellow"
        elif aqi_pred <= 300:
            category = "Poor"
            color = "orange"
        elif aqi_pred <= 400:
            category = "Very Poor"
            color = "red"
        else:
            category = "Severe"
            color = "darkred"

        st.markdown(f"### Predicted AQI: **{aqi_pred:.2f}**")
        st.markdown(f"### AQI Category: <span style='color:{color}'>{category}</span>",
                    unsafe_allow_html=True)


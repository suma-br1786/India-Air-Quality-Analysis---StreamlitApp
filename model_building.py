import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("models/aqi_model.pkl")

st.title("🌿 AQI Prediction App")
st.write("Predict Air Quality Index (AQI) based on pollutants, date, and city.")

# -----------------------------
# Sidebar for date & city
# -----------------------------
st.sidebar.header("Location & Date")
city = st.sidebar.text_input("City", value="Delhi")
date = st.sidebar.date_input("Select Date")
year, month, day_of_week = date.year, date.month, date.weekday()

# -----------------------------
# Pollutant Inputs in Columns
# -----------------------------
st.header("Pollutant Values")
col1, col2, col3 = st.columns(3)

with col1:
    pm25 = st.number_input("PM2.5", value=50.0)
    pm10 = st.number_input("PM10", value=80.0)
    no = st.number_input("NO", value=30.0)

with col2:
    no2 = st.number_input("NO2", value=20.0)
    nox = st.number_input("NOx", value=25.0)
    nh3 = st.number_input("NH3", value=15.0)

with col3:
    co = st.number_input("CO", value=0.8)
    so2 = st.number_input("SO2", value=10.0)
    o3 = st.number_input("O3", value=20.0)

# -----------------------------
# Prediction Button
# -----------------------------
if st.button("Predict AQI"):
    input_df = pd.DataFrame([{
        "PM2.5": pm25, "PM10": pm10, "NO": no,
        "NO2": no2, "NOx": nox, "NH3": nh3,
        "CO": co, "SO2": so2, "O3": o3,
        "year": year, "month": month,
        "day_of_week": day_of_week, "City": city
    }])
    
    aqi_pred = model.predict(input_df)[0]
    
    # Determine AQI category
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
    
    # Display results with color
    st.markdown(f"### Predicted AQI: **{aqi_pred:.2f}**")
    st.markdown(f"### AQI Category: <span style='color:{color}'>{category}</span>", unsafe_allow_html=True)

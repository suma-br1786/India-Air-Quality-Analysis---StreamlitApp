import streamlit as st
import pandas as pd

def app():
    st.title("🌿 AQI Prediction App")
    st.write("Enter pollutant values, date, and city to predict AQI value and category.")

    # -----------------------------
    # Sidebar: City & Date
    # -----------------------------
    st.sidebar.header("Location & Date")
    city = st.sidebar.text_input("City", value="Delhi")
    date = st.sidebar.date_input("Select Date")
    year, month, day_of_week = date.year, date.month, date.weekday()

    # -----------------------------
    # Pollutant Inputs
    # -----------------------------
    st.header("Pollutant Values")
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
    # AQI Prediction 
    # -----------------------------
    if st.button("Predict AQI"):
        
        aqi_pred = (
            pm25*0.5 + pm10*0.3 + no2*0.2 + no*0.1 + nox*0.1 +
            nh3*0.05 + co*10 + so2*0.1 + o3*0.2
        )

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

        # Display results
        st.markdown(f"### Predicted AQI: **{aqi_pred:.2f}**")
        st.markdown(
            f"### AQI Category: <span style='color:{color}'>{category}</span>",
            unsafe_allow_html=True
        )



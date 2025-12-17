import streamlit as st


def aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Satisfactory"
    if aqi <= 200:
        return "Moderate"
    if aqi <= 300:
        return "Poor"
    if aqi <= 400:
        return "Very Poor"
    return "Severe"


def pm25_aqi(pm):
    if pm <= 12: return 50
    if pm <= 35.4: return 100
    if pm <= 55.4: return 200
    if pm <= 150.4: return 300
    if pm <= 250.4: return 400
    return 500


def pm10_aqi(pm):
    if pm <= 54: return 50
    if pm <= 154: return 100
    if pm <= 254: return 200
    if pm <= 354: return 300
    if pm <= 424: return 400
    return 500


def no2_aqi(no2):
    if no2 <= 53: return 50
    if no2 <= 100: return 100
    if no2 <= 360: return 200
    if no2 <= 649: return 300
    if no2 <= 1249: return 400
    return 500


def so2_aqi(so2):
    if so2 <= 35: return 50
    if so2 <= 75: return 100
    if so2 <= 185: return 200
    if so2 <= 304: return 300
    if so2 <= 604: return 400
    return 500


def co_aqi(co):
    if co <= 4.4: return 50
    if co <= 9.4: return 100
    if co <= 12.4: return 200
    if co <= 15.4: return 300
    if co <= 30.4: return 400
    return 500


def o3_aqi(o3):
    if o3 <= 54: return 50
    if o3 <= 70: return 100
    if o3 <= 85: return 200
    if o3 <= 105: return 300
    if o3 <= 200: return 400
    return 500


def app():
    st.title("AQI Prediction (All Pollutants)")

    st.write("AQI is calculated as the maximum sub-index among pollutants.")

    pm25 = st.number_input("PM2.5 (µg/m³)", value=50.0)
    pm10 = st.number_input("PM10 (µg/m³)", value=80.0)
    no2 = st.number_input("NO2 (µg/m³)", value=30.0)
    so2 = st.number_input("SO2 (µg/m³)", value=10.0)
    co = st.number_input("CO (mg/m³)", value=0.8)
    o3 = st.number_input("O3 (µg/m³)", value=20.0)

    if st.button("Predict AQI"):
        sub_indices = {
            "PM2.5": pm25_aqi(pm25),
            "PM10": pm10_aqi(pm10),
            "NO2": no2_aqi(no2),
            "SO2": so2_aqi(so2),
            "CO": co_aqi(co),
            "O3": o3_aqi(o3),
        }

        overall_aqi = max(sub_indices.values())
        dominant_pollutant = max(sub_indices, key=sub_indices.get)

        st.subheader("AQI Result")
        st.metric("Overall AQI", overall_aqi)
        st.metric("AQI Category", aqi_category(overall_aqi))
        st.metric("Dominant Pollutant", dominant_pollutant)

        st.subheader("Pollutant-wise AQI")
        st.table(sub_indices)

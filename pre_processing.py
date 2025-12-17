import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def app():
    st.set_page_config(page_title="Data Pre-Processing", layout="wide")
    st.title("🧹 Data Pre-Processing")

    # ---------------- Load Dataset ----------------
    df = pd.read_csv("cleaned_India_air_quality.csv")

    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # ---------------- Checkboxes ----------------
    st.markdown("### 🔍 What’s Inside This Page❓")

    check_duplicate = st.checkbox("1️⃣ Identify Duplicate Values")
    check_missing = st.checkbox("2️⃣ Missing Data Analysis")
    check_outliers = st.checkbox("3️⃣ Outlier Detection & Treatment")
    check_statistics = st.checkbox("4️⃣ Descriptive Statistics")
    check_feature_engineering = st.checkbox

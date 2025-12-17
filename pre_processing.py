import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def app():
    st.title("🧹 Data Pre-Processing")

    # Load dataset
    df = pd.read_csv("cleaned_India_air_quality.csv")

    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Intro section
    st.markdown("### 🔍 What’s Inside This Page❓")
    st.markdown("📂 Expand each step to view details on data cleaning and analysis:")

    # Flags for each section
    check_duplicate = st.checkbox("1️⃣ Identify for Duplicate Values")
    check_missing = st.checkbox("2️⃣ Missing Data Analysis")
    check_outliers = st.checkbox("3️⃣ Outliers Check")
    check_statistics = st.checkbox("4️⃣ Descriptive Statistics")
    check_feature_engineering = st.checkbox("5️⃣ Feature Engineering")

    # ---------------- Check for Duplicate Values ----------------
    if check_duplicate:
        st.subheader("🧩 Duplicate Rows Check")
        duplicate_count = df.duplicated().sum()
        st.write(f"**Total Duplicate Rows:** {duplicate_count}")
        st.success("✅ Duplicate values checked!")

    # ---------------- Check for Missing Values ----------------
    if check_missing:
        st.subheader("Missing Values Overview")
        missing = df.isna().sum()
        st.dataframe(missing, use_container_width=True)

        st.subheader("📉 Missing Values (% and Count)")
        missing_df = pd.DataFrame({
            "Missing Values": df.isna().sum(),
            "Percentage (%)": (df.isna().sum() / len(df)) * 100
        })
        st.dataframe(
            missing_df.sort_values("Percentage (%)", ascending=False),
            use_container_width=True
        )

        st.subheader("🌡️ Missing Values Heatmap")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis', ax=ax)
        ax.set_title('Missing Values Heatmap')
        ax.set_xlabel('Columns')
        ax.set_ylabel('Rows')
        st.pyplot(fig)

        st.success("✅ Missing values checked!")

    # ---------------- Check for Outliers ----------------
    if check_outliers:
        st.subheader("📊 Outliers Summary")

        # select only numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            df[col] = df[col].astype(float)

            Q1 = np.percentile(df[col], 25)
            Q3 = np.percentile(df[col], 75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
            df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])

        st.success("✅ Outliers checked!")

    # ---------------- Descriptive Statistics ----------------
    if check_statistics:
        st.subheader("📈 Descriptive Statistics of the Dataset")
        st.dataframe(df.describe().T, use_container_width=True)
        st.success("✅ Descriptive statistics checked!")

    # ---------------- Feature Engineering ----------------
    if check_feature_engineering:
        st.subheader("Feature Engineering")

        # Converting the 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Extracting Year, Month, Day
        df['year'] = df['Date'].dt.year
        df['month'] = df['Date'].dt.month
        df['day'] = df['Date'].dt.day

        # Extracting Season
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            else:
                return 'Autumn'

        df['season'] = df['month'].apply(get_season)

        # Extracting Day of the Week
        df['day_of_week'] = df['Date'].dt.dayofweek
        day_map = {
            0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
            3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'
        }
        df['day_of_week'] = df['day_of_week'].map(day_map)

        st.subheader("Transformed Data Preview")
        st.dataframe(
            df[['Date', 'year', 'month', 'day', 'season', 'day_of_week']].head(),
            use_container_width=True
        )

        st.success("✅ Feature Engineering applied!")

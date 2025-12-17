import streamlit as st
import pandas as pd
import numpy as np
import import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def app():
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
    check_feature_engineering = st.checkbox("5️⃣ Feature Engineering")

    # ---------------- Duplicate Check ----------------
    if check_duplicate:
        duplicate_count = df.duplicated().sum()
        st.write(f"**Total Duplicate Rows:** {duplicate_count}")
        st.success("✅ Duplicate values checked!")

    # ---------------- Missing Values ----------------
    if check_missing:
        missing_df = pd.DataFrame({
            "Missing Count": df.isna().sum(),
            "Percentage (%)": (df.isna().sum() / len(df)) * 100
        })

        st.dataframe(
            missing_df.sort_values("Percentage (%)", ascending=False),
            use_container_width=True
        )

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis', ax=ax)
        st.pyplot(fig)

        st.success("✅ Missing values checked!")

    # ---------------- Outlier Detection ----------------
    if check_outliers:
        st.subheader("📊 Outlier Detection & Treatment")

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        skewed_cols = ['CO', 'NOx', 'PM2.5', 'PM10']

        summary = []

        for col in numeric_cols:
            if col in skewed_cols:
                safe = df[col].clip(lower=0)
                log_data = np.log1p(safe)

                Q1, Q3 = np.percentile(log_data, [25, 75])
                IQR = Q3 - Q1
                lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR

                before = ((log_data < lower) | (log_data > upper)).sum()

                df[col] = np.where(log_data > upper, np.expm1(upper), df[col])
                df[col] = np.where(log_data < lower, np.expm1(lower), df[col])

                after = ((np.log1p(df[col].clip(lower=0)) < lower) |
                         (np.log1p(df[col].clip(lower=0)) > upper)).sum()

            else:
                Q1, Q3 = np.percentile(df[col], [25, 75])
                IQR = Q3 - Q1
                lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR

                before = ((df[col] < lower) | (df[col] > upper)).sum()
                df[col] = np.clip(df[col], lower, upper)
                after = ((df[col] < lower) | (df[col] > upper)).sum()

            summary.append({
                "Column": col,
                "Outliers Before": before,
                "Outliers After": after
            })

        st.dataframe(pd.DataFrame(summary), use_container_width=True)
        st.success("✅ Outliers detected and treated!")

    # ---------------- Descriptive Statistics ----------------
    if check_statistics:
        st.dataframe(df.describe().T, use_container_width=True)
        st.success("✅ Descriptive statistics generated!")

    # ---------------- Feature Engineering ----------------
    if check_feature_engineering:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['year'] = df['Date'].dt.year
        df['month'] = df['Date'].dt.month
        df['day'] = df['Date'].dt.day
        df['day_of_week'] = df['Date'].dt.day_name()

        st.dataframe(
            df[['Date', 'year', 'month', 'day', 'day_of_week']].head(),
            use_container_width=True
        )

        st.success("✅ Feature Engineering applied!")
.pyplot as plt
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
    check_feature_engineering = st.checkbox("5️⃣ Feature Engineering")

    # ---------------- Duplicate Check ----------------
    if check_duplicate:
        st.subheader("🧩 Duplicate Rows Check")
        duplicate_count = df.duplicated().sum()
        st.write(f"**Total Duplicate Rows:** {duplicate_count}")
        st.success("✅ Duplicate values checked!")

    # ---------------- Missing Values ----------------
    if check_missing:
        st.subheader("📉 Missing Values Summary")

        missing_df = pd.DataFrame({
            "Missing Count": df.isna().sum(),
            "Percentage (%)": (df.isna().sum() / len(df)) * 100
        })

        st.dataframe(
            missing_df.sort_values("Percentage (%)", ascending=False),
            use_container_width=True
        )

        st.subheader("🌡️ Missing Values Heatmap")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(df.is

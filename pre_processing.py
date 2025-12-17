import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def app():
    st.title("🧹 Data Pre-Processing")

    # ---------------- Load Dataset ----------------
    try:
        df = pd.read_csv("cleaned_India_air_quality.csv")
    except Exception as e:
        st.error("❌ Dataset not found or failed to load")
        st.stop()

    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # ---------------- Options ----------------
    st.markdown("### 🔍 Select Preprocessing Steps")

    check_duplicate = st.checkbox("Identify Duplicate Values")
    check_missing = st.checkbox("Missing Data Analysis")
    check_outliers = st.checkbox("Outlier Detection & Treatment")
    check_statistics = st.checkbox("Descriptive Statistics")
    check_feature_engineering = st.checkbox("Feature Engineering")

    # ---------------- Duplicate Check ----------------
    if check_duplicate:
        dup_count = df.duplicated().sum()
        st.write(f"Total Duplicate Rows: **{dup_count}**")
        st.success("✅ Duplicate check completed")

    # ---------------- Missing Values ----------------
    if check_missing:
        missing_df = pd.DataFrame({
            "Missing Count": df.isna().sum(),
            "Percentage (%)": (df.isna().sum() / len(df)) * 100
        }).sort_values("Percentage (%)", ascending=False)

        st.dataframe(missing_df, use_container_width=True)

        fig, ax = plt.subplots(figsize=(12, 5))
        sns.heatmap(df.isnull(), cbar=False, ax=ax)
        st.pyplot(fig)

        st.success("✅ Missing value analysis completed")

    # ---------------- Outlier Detection ----------------
    if check_outliers:
        st.subheader("📊 Outlier Detection (IQR Method)")

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        skewed_cols = ["CO", "NOx", "PM2.5", "PM10"]

        summary = []

        for col in numeric_cols:
            if col in skewed_cols:
                safe = df[col].clip(lower=0)
                log_data = np.log1p(safe)

                Q1, Q3 = np.percentile(log_data, [25, 75])
                IQR = Q3 - Q1
                lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR

                before = ((log_data < lower) | (log_data > upper)).sum()

                df[col] = np.where(log_data > upper, np.expm1(upper), df[col])
                df[col] = np.where(log_data < lower, np.expm1(lower), df[col])

                after = ((np.log1p(df[col].clip(lower=0)) < lower) |
                         (np.log1p(df[col].clip(lower=0)) > upper)).sum()

            else:
                Q1, Q3 = np.percentile(df[col], [25, 75])
                IQR = Q3 - Q1
                lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR

                before = ((df[col] < lower) | (df[col] > upper)).sum()
                df[col] = np.clip(df[col], lower, upper)
                after = ((df[col] < lower) | (df[col] > upper)).sum()

            summary.append({
                "Column": col,
                "Outliers Before": int(before),
                "Outliers After": int(after)
            })

        st.dataframe(pd.DataFrame(summary), use_container_width=True)
        st.success("✅ Outliers detected and treated")

    # ---------------- Descriptive Statistics ----------------
    if check_statistics:
        st.dataframe(df.describe().T, use_container_width=True)
        st.success("✅ Descriptive statistics generated")

    # ---------------- Feature Engineering ----------------
    if check_feature_engineering:
        st.subheader("🛠 Feature Engineering")

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["year"] = df["Date"].dt.year
        df["month"] = df["Date"].dt.month
        df["day"] = df["Date"].dt.day
        df["day_of_week"] = df["Date"].dt.day_name()

        def season(month):
            if month in [12, 1, 2]:
                return "Winter"
            elif month in [3, 4, 5]:
                return "Spring"
            elif month in [6, 7, 8]:
                return "Summer"
            else:
                return "Autumn"

        df["season"] = df["month"].apply(season)

        st.dataframe(
            df[["Date", "year", "month", "day", "season", "day_of_week"]].head(),
            use_container_width=True
        )

        st.success("✅ Feature engineering applied")

import streamlit as st
import pandas as pd
import numpy as np
import import streamlit as st
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
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis', ax=ax)
        st.pyplot(fig)

        st.success("✅ Missing values checked!")

    # ---------------- Outlier Detection ----------------
    if check_outliers:
        st.subheader("📊 Outlier Detection & Treatment (IQR Method)")

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        outlier_summary = []

        skewed_cols = ['CO', 'NOx', 'PM2.5', 'PM10']  # Skewed pollutants

        for col in numeric_cols:
            before_count = 0
            after_count = 0

            if col in skewed_cols:
                # Avoid negative values before log
                safe_col = df[col].copy()
                safe_col[safe_col < 0] = 0

                transformed = np.log1p(safe_col)
                Q1 = np.percentile(transformed, 25)
                Q3 = np.percentile(transformed, 75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5*IQR
                upper = Q3 + 1.5*IQR

                before_count = ((transformed < lower) | (transformed > upper)).sum()

                # Cap original values using exponentiation
                df[col] = np.where(transformed > upper, np.expm1(upper), df[col])
                df[col] = np.where(transformed < lower, np.expm1(lower), df[col])

                # Count after capping
                safe_col_after = df[col].copy()
                safe_col_after[safe_col_after < 0] = 0
                transformed_after = np.log1p(safe_col_after)
                after_count = ((transformed_after < lower) | (transformed_after > upper)).sum()

            else:
                # Normal IQR for other columns
                Q1 = np.percentile(df[col], 25)
                Q3 = np.percentile(df[col], 75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5*IQR
                upper = Q3 + 1.5*IQR

                before_count = ((df[col] < lower) | (df[col] > upper)).sum()

                df[col] = np.where(df[col] < lower, lower, df[col])
                df[col] = np.where(df[col] > upper, upper, df[col])

                after_count = ((df[col] < lower) | (df[col] > upper)).sum()

            outlier_summary.append({
                "Column": col,
                "Outliers Before": before_count,
                "Outliers After": after_count,
                "Status": "✅ OK" if after_count == 0 else "⚠️ Outliers Remain"
            })

        st.subheader("🚨 Outlier Detection Summary")
        outlier_df = pd.DataFrame(outlier_summary)
        st.dataframe(outlier_df, use_container_width=True)
        st.success("✅ Outliers detected and treated successfully!")

    # ---------------- Descriptive Statistics ----------------
    if check_statistics:
        st.subheader("📈 Descriptive Statistics")
        st.dataframe(df.describe().T, use_container_width=True)
        st.success("✅ Descriptive statistics generated!")

    # ---------------- Feature Engineering ----------------
    if check_feature_engineering:
        st.subheader("🛠 Feature Engineering")

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['year'] = df['Date'].dt.year
        df['month'] = df['Date'].dt.month
        df['day'] = df['Date'].dt.day

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
        df['day_of_week'] = df['Date'].dt.day_name()

        st.subheader("🗂 Transformed Columns Preview")
        st.dataframe(
            df[['Date', 'year', 'month', 'day', 'season', 'day_of_week']].head(),
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
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis', ax=ax)
        st.pyplot(fig)

        st.success("✅ Missing values checked!")

    # ---------------- Outlier Detection ----------------
    if check_outliers:
        st.subheader("📊 Outlier Detection & Treatment (IQR Method)")

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        outlier_summary = []

        skewed_cols = ['CO', 'NOx', 'PM2.5', 'PM10']  # Skewed pollutants

        for col in numeric_cols:
            before_count = 0
            after_count = 0

            if col in skewed_cols:
                # Avoid negative values before log
                safe_col = df[col].copy()
                safe_col[safe_col < 0] = 0

                transformed = np.log1p(safe_col)
                Q1 = np.percentile(transformed, 25)
                Q3 = np.percentile(transformed, 75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5*IQR
                upper = Q3 + 1.5*IQR

                before_count = ((transformed < lower) | (transformed > upper)).sum()

                # Cap original values using exponentiation
                df[col] = np.where(transformed > upper, np.expm1(upper), df[col])
                df[col] = np.where(transformed < lower, np.expm1(lower), df[col])

                # Count after capping
                safe_col_after = df[col].copy()
                safe_col_after[safe_col_after < 0] = 0
                transformed_after = np.log1p(safe_col_after)
                after_count = ((transformed_after < lower) | (transformed_after > upper)).sum()

            else:
                # Normal IQR for other columns
                Q1 = np.percentile(df[col], 25)
                Q3 = np.percentile(df[col], 75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5*IQR
                upper = Q3 + 1.5*IQR

                before_count = ((df[col] < lower) | (df[col] > upper)).sum()

                df[col] = np.where(df[col] < lower, lower, df[col])
                df[col] = np.where(df[col] > upper, upper, df[col])

                after_count = ((df[col] < lower) | (df[col] > upper)).sum()

            outlier_summary.append({
                "Column": col,
                "Outliers Before": before_count,
                "Outliers After": after_count
            })

        st.subheader("🚨 Outlier Detection Summary")
        st.dataframe(pd.DataFrame(outlier_summary), use_container_width=True)
        st.success("✅ Outliers detected and treated successfully!")

    # ---------------- Descriptive Statistics ----------------
    if check_statistics:
        st.subheader("📈 Descriptive Statistics")
        st.dataframe(df.describe().T, use_container_width=True)
        st.success("✅ Descriptive statistics generated!")

    # ---------------- Feature Engineering ----------------
    if check_feature_engineering:
        st.subheader("🛠 Feature Engineering")

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['year'] = df['Date'].dt.year
        df['month'] = df['Date'].dt.month
        df['day'] = df['Date'].dt.day

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
        df['day_of_week'] = df['Date'].dt.day_name()

        st.subheader("🗂 Transformed Columns Preview")
        st.dataframe(
            df[['Date', 'year', 'month', 'day', 'season', 'day_of_week']].head(),
            use_container_width=True
        )
        st.success("✅ Feature Engineering applied!")

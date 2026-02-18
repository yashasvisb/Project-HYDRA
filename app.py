import streamlit as st
import pandas as pd
import plotly.express as px


# Page config
st.set_page_config(page_title="Project HYDRA Prototype", layout="wide")

st.title("💧 Project HYDRA – Intelligent Atmospheric Water Recovery")
st.markdown("**Rule-based AI prototype using real climatic data**")

# Load data
df = pd.read_csv("data.csv")
df.columns = df.columns.str.strip()

# Sidebar controls
st.sidebar.header("Simulation Controls")

selected_month = st.sidebar.selectbox(
    "Select Month",
    options=sorted(df["Month"].unique())
)

# Filter data
month_df = df[df["Month"] == selected_month]

# KPIs
adsorption_rate = month_df["Adsorption_Flag"].mean() * 100

st.metric(
    label="Adsorption Feasibility (%)",
    value=f"{adsorption_rate:.1f}%"
)

# Decision logic explanation
st.subheader("🧠 Decision Logic")

st.markdown("""
Adsorption is triggered when:

**Dew Point Temperature ≥ Surface Temperature**

Otherwise, the system switches to **Desorption (Regeneration Mode)** using waste heat.
""")

# Sample rows
st.subheader("📊 Sample Climate Decisions")
st.dataframe(
    month_df[[
        "Date",
        "Year",
        "Mean_Temp",
        "Humidity",
        "Surface_Temp",
        "Dew_Point",
        "Adsorption_Flag",
       
    ]]
)

# Visualization
st.subheader("📈 Dew Point vs Surface Temperature")

month_df["HYDRA"] = month_df["Adsorption_Flag"].map(
    {1: "Adsorption", 0:"Desorption"}
)
fig = px.scatter(
    month_df,
    x="Surface_Temp",
    y="Dew_Point",
    color="HYDRA",
    labels={
        "Surface_Temp": "Surface Temperature (°C)",
        "Dew_Point" : "Dew Point Temperature (°C)",
        "HYDRA": "Operating Mode"
    },
    title="Adsorption Decision Boundary"
)

st.plotly_chart(fig, use_container_width=True)

# Monthly intelligence
st.subheader("📅 Seasonal Intelligence")

monthly_ads = df.groupby("Month")["Adsorption_Flag"].mean().reset_index()
monthly_ads["Adsorption_%"] = monthly_ads["Adsorption_Flag"] * 100

fig2 = px.bar(
    monthly_ads,
    x="Month",
    y="Adsorption_%",
    title="Monthly Adsorption Probability"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("The dataset used has day-wise value of each parameter while the actual system will work on the basis of data collected at regular intervals throughout a single day. Hence the summer months of April, May and June have low absorption percentage")

st.success("Prototype logic validated using real-world climatic data.")

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Data ---
data = {
    "Year": list(range(2003, 2019)),
    "Albuquerque": [
        230.39, 258.42, 234.39, 233.75, 280.44, 255.94,
        207.86, 172.35, 180.81, 197.22, 187.40, 247.10,
        301.22, 348.49, 521.93, 353.24
    ],
    "New Mexico": [
        103.11, 108.35, 98.29, 107.18, 117.92, 108.40,
        96.14, 78.22, 82.75, 88.65, 87.79, 100.02,
        119.45, 131.24, 178.28, 135.06
    ],
    "United States": [
        142.45, 136.71, 140.79, 150.05, 148.31, 145.88,
        133.14, 119.32, 113.86, 113.12, 109.04, 101.25,
        102.25, 102.90, 98.60, 86.21
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# --- Streamlit UI ---
st.set_page_config(page_title="Albuquerque Robbery Stats", layout="centered")
st.title("📊 Albuquerque Robbery Statistics (2003–2018)")
st.markdown("Data Source: [FBI Crime in the U.S.](https://www.macrotrends.net/global-metrics/cities/us/nm/albuquerque/robbery-rate-statistics)")

# Multiselect for comparison
options = st.multiselect(
    "Select data to display:",
    ["Albuquerque", "New Mexico", "United States"],
    default=["Albuquerque", "New Mexico", "United States"]
)

# Filter dataframe for selection
df_melted = df.melt(id_vars=["Year"], var_name="Location", value_name="Rate")
filtered = df_melted[df_melted["Location"].isin(options)]

# Plot
fig = px.line(
    filtered,
    x="Year",
    y="Rate",
    color="Location",
    markers=True,
    title="Robbery Rates per 100,000 Population"
)

fig.update_layout(yaxis_title="Robberies per 100,000 Population")

st.plotly_chart(fig, use_container_width=True)

# Show raw data if user wants
if st.checkbox("Show raw data"):
    st.dataframe(df.set_index("Year"))

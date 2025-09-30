import streamlit as st
import pandas as pd
import plotly.express as px

# --- Historical Data (2003–2018) ---
historical_data = {
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

historical_df = pd.DataFrame(historical_data)

# --- NM Cities Latest Data (2018 snapshot) ---
cities_data = {
    "City": [
        "San Ysidro", "Albuquerque", "Gallup", "Red River", "Belen", "Farmington",
        "Los Lunas", "Springer", "Santa Fe", "Taos", "Raton", "Las Vegas", "Grants", "Deming",
        "Roswell", "Hobbs", "Bernalillo", "Moriarty", "Portales", "Carlsbad", "Las Cruces",
        "Socorro", "Eunice", "Rio Rancho", "Milan", "Bosque Farms", "Ruidoso", "Edgewood",
        "Lovington", "Alamogordo", "Aztec", "Bloomfield", "Cloudcroft", "Tularosa",
        "Truth Or Consequences", "Angel Fire", "Anthony", "Bayard", "Texico", "Tatum",
        "Taos Ski Valley", "Capitan", "Santa Rosa", "Cimarron", "Clayton", "Logan",
        "Corrales", "Santa Clara", "Dexter", "Ruidoso Downs", "Estancia", "Questa",
        "Peralta", "Mesilla", "Magdalena", "Hatch", "Los Alamos", "Hope", "Hurley",
        "Lordsburg"
    ],
    "Rate": [
        507.61, 353.24, 295.72, 214.59, 169.95, 154.31,
        122.05, 110.74, 105.73, 88.31, 83.89, 76.43, 66.80, 63.86,
        62.92, 62.63, 60.97, 56.27, 50.99, 48.01, 38.16,
        35.87, 33.77, 29.78, 27.44, 26.39, 25.91, 25.57,
        17.90, 15.96, 15.30, 12.62, 0.00, 0.00,
        0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
        0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
        0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
        0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
        0.00, 0.00
    ]
}

cities_df = pd.DataFrame(cities_data)

# --- Streamlit UI ---
st.set_page_config(page_title="Albuquerque Robbery Stats", layout="wide")
st.title("📊 Albuquerque Robbery Statistics (2003–2018)")
st.markdown("Data Source: [FBI Crime in the U.S.](https://www.macrotrends.net/global-metrics/cities/us/nm/albuquerque/robbery-rate-statistics)")

# Tabs for different views
tab1, tab2 = st.tabs(["Historical (2003–2018)", "NM Cities Snapshot (2018)"])

# --- Tab 1: Historical Data ---
with tab1:
    st.subheader("📈 Historical Trends")
    options = st.multiselect(
        "Select data to display:",
        ["Albuquerque", "New Mexico", "United States"],
        default=["Albuquerque", "New Mexico", "United States"]
    )

    df_melted = historical_df.melt(id_vars=["Year"], var_name="Location", value_name="Rate")
    filtered = df_melted[df_melted["Location"].isin(options)]

    fig = px.line(
        filtered,
        x="Year",
        y="Rate",
        color="Location",
        markers=True,
        title="Robbery Rates per 100,000 Population (2003–2018)"
    )
    fig.update_layout(yaxis_title="Robberies per 100,000 Population")

    st.plotly_chart(fig, use_container_width=True)

    if st.checkbox("Show raw historical data"):
        st.dataframe(historical_df.set_index("Year"))

# --- Tab 2: NM Cities Snapshot ---
with tab2:
    st.subheader("🏙️ 2018 Robbery Rates by City (New Mexico)")

    # Sort cities by rate descending
    sorted_cities = cities_df.sort_values(by="Rate", ascending=False)

    fig2 = px.bar(
        sorted_cities.head(20),
        x="Rate",
        y="City",
        orientation="h",
        title="Top 20 NM Cities by Robbery Rate (2018)",
        text="Rate"
    )
    fig2.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig2.update_layout(yaxis={'categoryorder': 'total ascending'})

    st.plotly_chart(fig2, use_container_width=True)

    if st.checkbox("Show full city dataset"):
        st.dataframe(sorted_cities.reset_index(drop=True))
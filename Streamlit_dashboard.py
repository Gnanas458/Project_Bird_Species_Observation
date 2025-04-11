import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Bird Species Observation Dashboard", layout="wide")

# Function to load data from MySQL
@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",         # Change to your MySQL username
        password="240996",     # Change to your MySQL password
        database="Birds"
    )
    query = "SELECT * FROM bird_data"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load data
df = load_data()

# Dashboard title
st.title("🕊️ Bird Species Observation Dashboard")

# Optional raw data display
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Section: Top 10 bird species by total observations
st.subheader("📌 Top 10 Bird Species Observed")

top_10_species = df["common_name"].value_counts().nlargest(10).index
top_species_df = df[df["common_name"].isin(top_10_species)]

# Group by season for heatmap
heatmap_species_season = top_species_df.groupby(["common_name", "season"]).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(heatmap_species_season, annot=True, fmt="d", cmap="magma", ax=ax)
plt.title("Top 10 Bird Species Observed by Season")
plt.xlabel("Season")
plt.ylabel("Common Name")
st.pyplot(fig)

# Section: Most Active Observers
st.subheader("🧑‍🔬 Most Active Observers")
observer_counts = df["observer"].value_counts().nlargest(10)
st.bar_chart(observer_counts)

# Section: Seasonal Distribution
st.subheader("🌦️ Seasonal Bird Observation Count")
season_counts = df["season"].value_counts()
st.bar_chart(season_counts)

# Section: Filter by Observer and Region
st.subheader("🔎 Filter Observations")

with st.expander("Filter Options"):
    observer_filter = st.multiselect("Select Observer(s)", df["observer"].dropna().unique())
    region_filter = st.multiselect("Select Region(s)", df["admin_unit_code"].dropna().unique())

filtered_df = df.copy()
if observer_filter:
    filtered_df = filtered_df[filtered_df["observer"].isin(observer_filter)]
if region_filter:
    filtered_df = filtered_df[filtered_df["admin_unit_code"].isin(region_filter)]

st.write(f"Filtered Observations: {len(filtered_df)}")
st.dataframe(filtered_df)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Project: Bird Species Observation Analysis")

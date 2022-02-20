import re
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Global Airport Data", page_icon=":airplane:", layout="wide"
)


@st.cache
def load_data():
    df = pd.read_csv("https://davidmegginson.github.io/ourairports-data/airports.csv")
    return df


df = load_data().dropna(subset=["iata_code"])


# --- SIDEBAR ---
st.sidebar.header("Please filter here:")

cols = st.sidebar.multiselect(
    "Select columns to show",
    options=list(df.columns),
    default=["iso_country", "iata_code"],
)

country = st.sidebar.multiselect(
    "Filter country", options=df["iso_country"].unique(), default=None
)
ap_type = st.sidebar.multiselect(
    "Filter airport type", options=df["type"].unique(), default=None
)

l1 = st.sidebar.text_input("Filter by first letter of IATA")
l2 = st.sidebar.text_input("Filter by second letter of IATA")
l3 = st.sidebar.text_input("Filter by third letter of IATA")


df_selection = df.query(
    "iso_country == @country & type == @ap_type & iata_code.str[0] == @l1 | iata_code.str[1] == @l2 | iata_code.str[2] == @l3"
)

#  --- MAIN PAGE ---
st.title(":airplane:  Global Airport Data")
st.text(" ")

if st.checkbox("Show full raw data"):
    st.subheader("All raw data")
    st.dataframe(df)

st.text(" ")
st.dataframe(df_selection[cols])

with st.expander("Show map"):
    st.map(df_selection.rename(columns={"longitude_deg": "lon", "latitude_deg": "lat"}))

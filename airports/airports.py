import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Global Airport Data", page_icon=":airplane:", layout="wide"
)


@st.cache
def load_data():
    df = pd.read_csv("https://davidmegginson.github.io/ourairports-data/airports.csv")
    return df


original = load_data()
df = load_data().dropna(subset=["iata_code"])


# --- SIDEBAR ---
st.sidebar.header("Please filter here:")

cols = st.sidebar.multiselect(
    "Select columns to show",
    options=list(df.columns),
    default=["municipality", "iso_country", "name", "iata_code"],
)

country = st.sidebar.multiselect(
    "Filter iso_country", options=df["iso_country"].unique(), default="US"
)

# --- TYPE ---
type_container = st.sidebar.container()
all_ap_type = st.sidebar.checkbox("Select all")

if all_ap_type:
    ap_type = type_container.multiselect(
        "Filter type",
        options=df["type"].unique(),
        default=df["type"].unique(),
    )
else:
    ap_type = type_container.multiselect(
        "Filter airport type",
        options=df["type"].unique(),
        default="large_airport",
    )

# --- IATA LETTERS ---
st.sidebar.write("Filter iata_code by letters:")
col1, col2, col3 = st.sidebar.columns(3)

with col1:
    l1 = st.text_input("Letter 1", value="A")

with col2:
    l2 = st.text_input("Letter 2")

with col3:
    l3 = st.text_input("Letter 3")


df_selection = df.query(
    "(iso_country == @country) and (type == @ap_type) and (iata_code.str[0] == @l1 or iata_code.str[1] == @l2 or iata_code.str[2] == @l3)"
)

#  --- MAIN PAGE ---
st.title("Global IATA Airport Data :airplane:")
st.write(
    "Inspired by [Airportle](https://airportle.scottscheapflights.com/), a Wordle game for airports | Data updates nightly."
)
st.write("***")
st.write("\n")

if st.checkbox("Show full raw data"):
    st.subheader("All raw data")
    st.dataframe(original)

st.text(" ")
st.write(
    "Currently showing `{}` in `{}` with letters `{}{}{}` respectively in `iata_code`:".format(
        ", ".join(ap_type), ", ".join(country), l1, l2, l3
    )
)
st.dataframe(df_selection[cols])
st.caption(
    "{} (out of {}) rows accross {} columns".format(
        df_selection[cols].shape[0], original.shape[0], df_selection[cols].shape[1]
    )
)

with st.expander("Visualize selection on map"):
    st.map(df_selection.rename(columns={"longitude_deg": "lon", "latitude_deg": "lat"}))


st.write("\n\n")
st.caption("[Data source](https://ourairports.com/data/)")

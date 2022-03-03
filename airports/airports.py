import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import country_converter as coco
import plotly.express as px


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

# --- COUNTRIES ---
country_container = st.sidebar.container()
all_countries = st.sidebar.checkbox("All countries")
ccdict = coco.agg_conc("ISO2", "name_short", as_dataframe=False)
country = "all countries"

if not all_countries:
    country = country_container.multiselect(
        "Filter iso_country",
        options=df["iso_country"].dropna().unique(),
        default="US",
        format_func=ccdict.get,
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

if all_countries:
    df_selection = df.query(
        "(type == @ap_type) and (iata_code.str[0] == @l1 or iata_code.str[1] == @l2 or iata_code.str[2] == @l3)"
    )
else:
    df_selection = df.query(
        "(iso_country == @country) and (type == @ap_type) and (iata_code.str[0] == @l1 or iata_code.str[1] == @l2 or iata_code.str[2] == @l3)"
    )

#  --- MAIN PAGE ---
st.title("Global IATA Airport Data :airplane:")
st.write(
    "Inspired by [Airportle](https://airportle.scottscheapflights.com/), a Wordle game for airports."
)
st.write("***")
st.write("\n")

if st.checkbox("Show full raw data"):
    st.subheader("All raw data")
    st.dataframe(original)

st.text(" ")
st.write(
    "Currently showing `{}` in `{}` with letters `{}{}{}` respectively in `iata_code`:".format(
        ", ".join(ap_type),
        country if country == "all countries" else ", ".join(country),
        l1,
        l2,
        l3,
    )
)
st.dataframe(df_selection[cols])
st.caption(
    "{} (out of {}) rows accross {} columns".format(
        df_selection[cols].shape[0], original.shape[0], df_selection[cols].shape[1]
    )
)

# --- MAP ---
fig = px.scatter_mapbox(
    df_selection,
    lat="latitude_deg",
    lon="longitude_deg",
    hover_name="iata_code",
    hover_data={
        "name": True,
        "municipality": True,
        "type": True,
        "latitude_deg": False,
        "longitude_deg": False,
    },
    color_discrete_sequence=["#ff4b4b"],
    zoom=1,
    height=400,
)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_layout(
    hoverlabel_font={"family": "Open Sans", "color": "#FFFFFF"},
    hoverlabel_bordercolor="#ff4b4b",
)
fig.update_traces(textposition="top center")
with st.expander("Visualize selection on map"):
    st.plotly_chart(fig, True)


st.write("\n\n")
st.caption("[Data source](https://ourairports.com/data/) (updates nightly)")

components.html("""<script id="help-ukraine-win" async="true" 
                src="https://helpukrainewinwidget.org/cdn/widget.js" data-type="four" data-position="bottom-left"></script>
""")
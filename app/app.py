import streamlit as st
import numpy as np
import time
import pandas as pd
import pandas_gbq
import plotly.express as px
import folium
from streamlit_folium import st_folium
from google.oauth2 import service_account
from google.cloud import bigquery


MAP_CENTER = (47.391, 9.103014)

cantons = [
    "AG",
    "AI",
    "AR",
    "BE",
    "BL",
    "BS",
    "FR",
    "GE",
    "GL",
    "GR",
    "JU",
    "LU",
    "NE",
    "NW",
    "OW",
    "SG",
    "SH",
    "SZ",
    "SO",
    "TG",
    "TI",
    "UR",
    "VS",
    "VD",
    "ZG",
    "ZH",
]

st.set_page_config(
    page_title=None,
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",  # "auto"
    menu_items=None,
)

# Setup the data connection

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 100 min.
# @st.cache_data(ttl=6000)
# def run_query(query):
#     query_job = client.query(query)
#     rows_raw = query_job.result()
#     # Convert to list of dicts. Required for st.cache_data to hash the return value.
#     rows = [dict(row) for row in rows_raw]
#     return rows


# rows = run_query("SELECT word FROM `bigquery-public-data.samples.shakespeare` LIMIT 10")

# # Print results.
# st.write("Some wise words from Shakespeare:")
# for row in rows:
#     st.write("✍️ " + row["word"])


# Uses st.cache_data to only rerun when the query changes or after 100 min.
@st.cache_data(ttl=6000)
def get_offer_df():
    query = "SELECT * FROM `farm-screener.farm_screener.offers`"

    offers_df = pandas_gbq.read_gbq(
        query, project_id=credentials.project_id, credentials=credentials
    )
    return offers_df


@st.cache_data(ttl=6000)
def get_farms_df():
    query = "SELECT * FROM `farm-screener.farm_screener.farms`"

    df = pandas_gbq.read_gbq(
        query, project_id=credentials.project_id, credentials=credentials
    )
    return df


df = get_offer_df()
farms_df = get_farms_df()


@st.cache_data(ttl=6000)
def get_merged_df(offers_df, farms_df):

    merged_df = pd.merge(farms_df, offers_df, on="farm_id", how="inner")

    # farms_geo_df = farms_df.copy()
    farms_geo_df = merged_df.copy()
    farms_geo_df.dropna(inplace=True)
    return farms_geo_df

merged_df = get_merged_df(df,farms_df)

#####################################

st.header("Swiss Farmers´ Direct Selling Offers")
# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))
st.sidebar.header("Settings")
n_largest = st.sidebar.slider("Number of Bars to Display", 0, 30, 10)


column_config = {
    "product_name": st.column_config.TextColumn(
        "Product",
        help="Streamlit **widget** commands 🎈",
        default=None,
        max_chars=50,
        width="medium",
        # validate="^st\.[a-z_]+$",
    )
}

# offer_counts = df.groupby(by=["product_name"]).count()
offer_counts = (
    df.product_name.value_counts()
    .reset_index()
    .rename(columns={"index": "value", 0: "count"})
)
offer_counts["rank"] = offer_counts["count"].rank(method="first", ascending=False)


offers_sorted = offer_counts.nlargest(n_largest, "count").sort_values(
    by=["count", "product_name"], ascending=False
)

offer_counts_copy = offer_counts.copy()
# offer_counts_copy.loc[offer_counts_copy["count"] < 200, "count"] = "Other products"  # Represent only large product counts

fig = px.pie(
    offer_counts_copy,
    values="count",
    names="product_name",
    title="Distribution of Product Offers Based on All Offers",
)
fig.update_traces(
    textposition="inside",
    textinfo="percent",
)  # "percent+label"
fig.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")
st.plotly_chart(fig, theme=None)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Number of Farms with Offers", value=len(df.farm_id.unique())
    )  # , delta="1.2 °F")

with col2:
    st.metric(label="Number of Products", value=len(df.product_name.unique()))

with col3:
    st.metric(
        label="Number of Unique Product Offers",
        value=len(offer_counts.loc[offer_counts["count"] == 1]),
    )


st.divider()

tab1, tab2, tab3 = st.tabs(
    [
        "Most Common Product Offers",
        "Least Common Product Offers",
        "Unique Product Offers",
    ]
)

with tab1:
    fig = px.bar(
        offers_sorted,
        x="product_name",
        y="count",
        title="Most Common Product Offers",
    )
    fig.update_layout(xaxis_title="Product", yaxis_title="Count")
    st.plotly_chart(fig, theme="streamlit")
with tab2:
    offers_sorted_smallest = offer_counts.nsmallest(n_largest, "count").sort_values(
        by=["count", "product_name"], ascending=False
    )
    fig = px.bar(
        offers_sorted_smallest,
        x="product_name",
        y="count",
        title="Least Common Product Offers",
    )
    fig.update_layout(xaxis_title="Product", yaxis_title="Count")
    st.plotly_chart(fig, theme="streamlit")
with tab3:
    fig = px.bar(
        offer_counts.loc[offer_counts["count"] == 1], x="product_name", y="count"
    )
    fig.update_layout(xaxis_title="Product", yaxis_title="Count")
    st.plotly_chart(fig, theme="streamlit")

# 'st.write("This is an interactive table")
# st.dataframe(df.style.highlight_max(axis=0))'

st.dataframe(offer_counts, column_config=column_config, hide_index=True)


col4, col5 = st.columns(2)
with col4:
    product_selection = st.selectbox("Select your desired product", df["product_name"].unique())

with col5:
    cantons_all = ["ALL"]
    cantons_all = cantons_all + cantons

    canton_selection = st.multiselect(
        "Select the canton", cantons_all, default="ALL"
    )
    if "ALL" in canton_selection:
        canton_selection = cantons

    elif canton_selection is None:
        canton_selection = cantons
    #st.write(canton_selection)

# "You selected: ", product_selection


# x = st.slider("x", key="number_slider")  # 👈 this is a widget
# st.write(x, "squared is", x * x)

# st.session_state.number_slider


# left_column, right_column = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column.button("Press me!")

# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         "Sorting hat", ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")
#     )
#     st.write(f"You are in {chosen} house!")

# # Add a selectbox to the sidebar:
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?", ("Email", "Home phone", "Mobile phone")
# )


# st.write("Explore the mapping function:")

# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
# )

# st.dataframe(merged_df, hide_index=True)

filtered_df = merged_df.loc[(merged_df["product_name"]==product_selection) & (merged_df["canton"].isin(canton_selection))]


# Creating a map to display the farms
map = folium.Map(location=MAP_CENTER, zoom_start=9, control_scale=True)
# Loop through each row in the dataframe
for i, row in filtered_df.iterrows():
    # Setup the content of the popup
    iframe = folium.IFrame(
        str(
            f"""
                               <b> {row["farm_name"]}</b> <br>
                               {row["street"]} <br>
                               {row["zip"]} {row["city"]} <br>
                               phone: {row["telephone"]} 
                               """
        )
    )

    # Initialise the popup using the iframe
    popup = folium.Popup(iframe, min_width=200, max_width=300)

    # Add each row to the map
    folium.Marker(
        location=[row["lat"], row["lon"]], popup=popup, c=row["canton"]
    ).add_to(map)

st_folium_map = st_folium(map, width=725)


column_config_farms = {
    "product_name": st.column_config.TextColumn(
        "Product",
        help="Streamlit **widget** commands 🎈",
        default=None,
        max_chars=50,
        width="medium",
        # validate="^st\.[a-z_]+$",
    )
}


display_columns = [
    "farm_name",
    "street",
    "zip",
    "city",
    "canton",
    "telephone",
    "websitehttp://www.vb-hof.ch",
]

st.dataframe(filtered_df[display_columns], column_config=column_config_farms, hide_index=True)

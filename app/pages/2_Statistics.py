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
from data import get_farms_df, get_offer_df, get_merged_df

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


# Setup the data connection

# # Create API client.
# credentials = service_account.Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"]
# )
# client = bigquery.Client(credentials=credentials)

# # Uses st.cache_data to only rerun when the query changes or after 100 min.
# @st.cache_data(ttl=6000)
# def get_offer_df():
#     query = "SELECT * FROM `farm-screener.farm_screener.offers`"

#     offers_df = pandas_gbq.read_gbq(
#         query, project_id=credentials.project_id, credentials=credentials
#     )
#     return offers_df


# @st.cache_data(ttl=6000)
# def get_farms_df():
#     query = "SELECT * FROM `farm-screener.farm_screener.farms`"

#     df = pandas_gbq.read_gbq(
#         query, project_id=credentials.project_id, credentials=credentials
#     )
#     return df


df = get_offer_df()
farms_df = get_farms_df()


# @st.cache_data(ttl=6000)
# def get_merged_df(offers_df, farms_df):

#     merged_df = pd.merge(farms_df, offers_df, on="farm_id", how="inner")

#     # farms_geo_df = farms_df.copy()
#     farms_geo_df = merged_df.copy()
#     farms_geo_df.dropna(inplace=True)
#     return farms_geo_df

merged_df = get_merged_df(df, farms_df)

#####################################

st.header("Swiss Farmers´ Direct Selling Offers")
# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))
#st.sidebar.header("Settings")
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

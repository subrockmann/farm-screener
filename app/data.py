import streamlit as st
#import numpy as np
#import time
import pandas as pd
import pandas_gbq
from google.oauth2 import service_account
from google.cloud import bigquery


st.set_page_config(
    page_title=None,
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",  # "auto"
    menu_items=None,
)
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

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)


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

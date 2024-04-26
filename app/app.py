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


df = get_offer_df()
farms_df = get_farms_df()
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



filtered_df = merged_df.loc[(merged_df["product_name"]==product_selection) & (merged_df["canton"].isin(canton_selection))]


MAP_CENTER = (47.391, 9.103014)
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
        location=[row["lat"], row["lon"]], 
        popup=popup, 
        #c=row["canton"]
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
    "website",
]

st.dataframe(filtered_df[display_columns], column_config=column_config_farms, hide_index=True)

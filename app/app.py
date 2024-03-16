import streamlit as st
import numpy as np
import time
import pandas as pd


st.write("Hello world")

df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

st.table(df)


st.write("This is an interactive table")
st.dataframe(df.style.highlight_max(axis=0))

option = st.selectbox("Which number do you like best?", df["first column"])

"You selected: ", option

st.line_chart(df)

x = st.slider("x", key="number_slider")  # 👈 this is a widget
st.write(x, "squared is", x * x)

st.session_state.number_slider


left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button("Press me!")

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        "Sorting hat", ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")
    )
    st.write(f"You are in {chosen} house!")

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?", ("Email", "Home phone", "Mobile phone")
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))

st.write("Explore the mapping function:")

# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
# )

# st.map(map_data)

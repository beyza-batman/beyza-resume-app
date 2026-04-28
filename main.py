import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
# This sets the browser tab title and the favicon (emoji).
st.set_page_config(page_title="My First App", page_icon="🚀")

# 2. Titles and Text
# Various ways to display text on the screen.
st.title("Learning Streamlit 🎈")
st.header("This is a Header")
st.write("This is standard text. It supports Markdown like **bold**, *italic*, or `code` snippets.")

# 3. Interactive Widgets
# These allow the user to interact with your app.
st.divider() # Adds a horizontal separator line
st.subheader("Interactive Section")

# The values selected by the user are stored directly in variables.
user_name = st.text_input("What is your name?")
user_age = st.slider("How old are you?", min_value=0, max_value=100, value=25)

# Actions triggered by a button click.
if st.button("Introduce Me"):
    st.success(f"Hello {user_name}! You are {user_age} years old.")

# 4. Data and Charts
# Streamlit is designed specifically for data visualization.
st.divider()
st.subheader("Data Visualization")

# Create a sample DataFrame with random numbers
data = pd.DataFrame(
    np.random.randn(10, 2),
    columns=['Speed', 'Performance']
)

# Display the first 3 rows as a static table
st.table(data.head(3))

# Display the data as an interactive line chart
st.line_chart(data)

# 5. Sidebar
# Use 'with st.sidebar' to move elements to the left panel.
with st.sidebar:
    st.title("Settings")
    theme_choice = st.selectbox("Color Theme", ["Dark", "Light"])
    st.write(f"Selected theme: {theme_choice}")

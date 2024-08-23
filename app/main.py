import sys
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from notebooks.task1_script import *

# Set page configuration
st.set_page_config(page_title="Solar Data Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load and preprocess data
@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    return data.head(1000)  # Limit to 1000 rows for faster processing


# Add a title and introduction
st.title("🌞 Solar Data Analysis Dashboard")
st.markdown("""
Welcome to the Solar Data Analysis Dashboard! This tool allows you to explore and visualize solar energy data, 
including solar radiation components, temperature measures, and wind conditions. Use the options in the sidebar 
to navigate through different analyses and visualizations.
""")

# Sidebar for navigation
st.sidebar.header("Navigation")
sidebar_option = st.sidebar.radio("Select Analysis", [
    "Summary Statistics",
    "Missing Values",
    "Outliers",
    "Negative Values",
    "Time Series Plot",
    "Area Plot",
    "Impact of Cleaning",
    "Correlation Analysis",
    "Wind Analysis",
    "Temperature Analysis",
    "Histograms"
])

# Load the data
data_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if data_file is not None:
    benin_data = load_data(data_file)
else:
    st.warning("Please upload a CSV file to get started.")
    st.stop()

# Display selected analysis
if sidebar_option == "Summary Statistics":
    st.header("Summary Statistics")
    st.write(calc(benin_data, 'Benin'))

elif sidebar_option == "Missing Values":
    st.header("Missing Values")
    st.write(check_missing_values(benin_data, 'Benin'))

elif sidebar_option == "Outliers":
    st.header("Outliers")
    st.write(check_outliers(benin_data, 'Benin'))

elif sidebar_option == "Negative Values":
    st.header("Negative Values")
    st.write(check_negative_values(benin_data, 'Benin'))

elif sidebar_option == "Time Series Plot":
    st.header("Time Series Plot")
    fig = plot_time_series(benin_data, 'Benin')
    st.pyplot(fig)

elif sidebar_option == "Area Plot":
    st.header("Area Plot")
    fig = plot_area(benin_data, 'Benin Area Plot')
    st.pyplot(fig)

elif sidebar_option == "Impact of Cleaning":
    st.header("Impact of Cleaning")
    fig = evaluate_cleaning_impact(benin_data)
    st.pyplot(fig)

elif sidebar_option == "Correlation Analysis":
    st.header("Correlation Analysis")
    fig = correlation_analysis(benin_data)
    st.pyplot(fig)

elif sidebar_option == "Wind Analysis":
    st.header("Wind Speed and Direction Analysis")
    fig = wind_analysis(benin_data)
    st.pyplot(fig)

elif sidebar_option == "Temperature Analysis":
    st.header("Temperature Analysis")
    fig = temperature_analysis(benin_data)
    st.pyplot(fig)

elif sidebar_option == "Histograms":
    st.header("Histograms")
    fig = plot_histograms(benin_data)
    st.pyplot(fig)

# Add footer
st.markdown("""
---
Made with ❤️ by [Your Name]. For more details, visit [Your GitHub](https://github.com/yourgithub).
""")

# Apply custom CSS for additional styling
st.markdown("""
    <style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #fafafa;
    }
    .sidebar .sidebar-header {
        background: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

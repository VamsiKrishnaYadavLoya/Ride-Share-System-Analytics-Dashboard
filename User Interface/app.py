# app.py
import streamlit as st
from analysis import load_data, get_monthly_usage_trends, plot_monthly_usage_trends

# Load data (adjust the filepath to your dataset's location)
df = load_data('merged_and_cleaned_tripdata.csv')

def main_page():
    st.title('Scooter Usage Dashboard')

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button('Classic Bikes'):
            st.session_state.page = 'classic_bikes'
    with col2:
        if st.button('Electric Bikes'):
            st.session_state.page = 'electric_bikes'
    # Additional buttons or content can be added here

def classic_bikes_page():
    st.title('Classic Bikes Analysis')
    
    # Interactive temporal filtering (optional)
    year = st.selectbox('Select Year', options=df['started_at'].dt.year.unique())

    # Generate and display the usage trends visualization
    trends = get_monthly_usage_trends(df[df['started_at'].dt.year == year], 'classic_bike')
    fig = plot_monthly_usage_trends(trends)
    st.plotly_chart(fig)

# Add more page functions as needed

# Navigation
def show_page():
    if 'page' not in st.session_state:
        st.session_state.page = 'main'
    
    if st.session_state.page == 'main':
        main_page()
    elif st.session_state.page == 'classic_bikes':
        classic_bikes_page()
    # Add more pages as elif blocks

show_page()

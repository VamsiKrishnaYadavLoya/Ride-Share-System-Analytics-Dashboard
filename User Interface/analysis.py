# analysis.py
import pandas as pd
import plotly.express as px

def load_data(filepath):
    """Loads the cleaned scooter usage data."""
    df = pd.read_csv(filepath, parse_dates=['started_at', 'ended_at'])
    return df

def get_monthly_usage_trends(df, scooter_type):
    """Returns a DataFrame with monthly usage trends for a specific scooter type."""
    filtered_df = df[df['rideable_type'] == scooter_type]
    trends = filtered_df.resample('M', on='started_at').size().reset_index(name='count')
    trends['month'] = trends['started_at'].dt.strftime('%Y-%m')
    return trends

def plot_monthly_usage_trends(trends):
    """Generates a Plotly line chart showing monthly usage trends."""
    fig = px.line(trends, x='month', y='count', title='Monthly Usage Trends')
    return fig

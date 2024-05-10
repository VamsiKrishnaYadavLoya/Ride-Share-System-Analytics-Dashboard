import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import calendar
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))



def load_and_prepare_data(file_pattern):
    df = pd.read_csv(file_pattern)
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    df.drop_duplicates(inplace=True)
    return df

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def calculate_distances(df):
    df['distance_km'] = df.apply(lambda x: haversine_distance(x['start_lat'], x['start_lng'], x['end_lat'], x['end_lng']), axis=1)
    return df

# New function to encapsulate data analysis and return summary metrics
# Data_Analysis.py modification

def calculate_metrics_by_type(file_pattern):
    df = load_and_prepare_data(file_pattern)
    df = calculate_distances(df)

    # Assuming 'scooter_type' is a column in your dataframe that describes the type of each scooter
    metrics_by_type = {}
    for scooter_type, group in df.groupby('scooter_type'):
        average_distance_km = group['distance_km'].mean()
        most_common_start_location = group['start_station_name'].mode()[0]
        group['month'] = group['started_at'].dt.month
        most_preferred_month = group['month'].value_counts().idxmax()
        most_preferred_month_name = calendar.month_name[most_preferred_month]
        monthly_distance_sum = group.groupby('month')['distance_km'].sum()
        most_distance_month = monthly_distance_sum.idxmax()
        most_distance_month_name = calendar.month_name[most_distance_month]
        group['duration_minutes'] = (group['ended_at'] - group['started_at']).dt.total_seconds() / 60
        average_duration = group['duration_minutes'].mean()

        metrics_by_type[scooter_type] = {
            "average_distance_km": average_distance_km,
            "most_common_start_location": most_common_start_location,
            "most_preferred_month_name": most_preferred_month_name,
            "most_distance_month_name": most_distance_month_name,
            "total_distance": monthly_distance_sum.max(),
            "average_duration": average_duration
        }

    return metrics_by_type


# If you wish to run and visualize directly from this script
def main():
    metrics = calculate_metrics_by_type("C:/Users/vbodavul/Downloads/archive (2)/merged_and_cleaned_tripdata.csv")
    print(metrics)

if __name__ == "__main__":
    main()

import pandas as pd

df_2018 = pd.read_csv(r"Divvy_Trips_2018_Q1.csv")
df_2018.shape
df_2018.columns

df_2018.columns = ['rentID','start_time','end_time','bikeID','Duration in (Sec)','start_station_id','start_station_name','end_station_id','end_station_name','user_type','gender','DOB']

df1 = pd.read_csv(r"202301-divvy-tripdata.csv")
df2 = pd.read_csv(r"202302-divvy-tripdata.csv")
df3 = pd.read_csv(r"202303-divvy-tripdata.csv")
df4 = pd.read_csv(r"202304-divvy-tripdata.csv")
df5 = pd.read_csv(r"202305-divvy-tripdata.csv")
df6 = pd.read_csv(r"202306-divvy-tripdata.csv")
df7 = pd.read_csv(r"202307-divvy-tripdata.csv")
df8 = pd.read_csv(r"202308-divvy-tripdata.csv")
df8_1 = pd.read_csv(r"202309-divvy-tripdata.csv")
df9 = pd.read_csv(r"202310-divvy-tripdata.csv")
df10 = pd.read_csv(r"202311-divvy-tripdata.csv")
df11 = pd.read_csv(r"202312-divvy-tripdata.csv")
df12 = pd.read_csv(r"202401-divvy-tripdata.csv")


df12.columns

df2.shape
df3.shape
rides_df = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df8_1,df9,df10,df11,df12,],axis=0)

rides_df.shape

rides_df.columns

# # Data Cleaning

rides_df.isna().sum()
df_2018.isna().sum()

rides_df.dropna(subset=['end_lat'], inplace=True)
rides_df.isna().sum()

#Data Imputation
#drop end_latitute and end longitude
# Refill nan values in start_station_name,end_station_name using start_lat,start_long & end_lat,end_log
# from geopy.distance import geodesic

# def find_nearest_station(row, stations):
#     min_dist = float('inf')
#     nearest_station = None
#     for _, station in stations.iterrows():
#         dist = geodesic((row['start_lat'], row['start_lng']), (station['start_lat'], station['start_lng'])).meters
#         if dist < min_dist:
#             min_dist = dist
#             nearest_station = station['start_station_name']
#             print(nearest_station)
#     return nearest_station

# # Create a DataFrame containing only stations
# stations = rides_df[['start_station_name', 'start_lat', 'start_lng']].dropna().drop_duplicates()

# # Fill missing start_station_name values
# rides_df['start_station_name'] = rides_df.apply(
#     lambda row: find_nearest_station(row, stations) if pd.isnull(row['start_station_name']) else row['start_station_name'], 
#     axis=1
# )


rides_df['Ride_start_timestamp'] = pd.to_datetime(rides_df['started_at'], format="mixed")
rides_df['Ride_end_timestamp'] = pd.to_datetime(rides_df['ended_at'], format="mixed")


df_2018['Ride_start_timestamp'] = pd.to_datetime(df_2018['start_time'], format="mixed")
df_2018['Ride_end_timestamp'] = pd.to_datetime(df_2018['end_time'], format="mixed")

rides_df['month'] = pd.to_datetime(rides_df['started_at']).dt.month
rides_df['year'] = pd.to_datetime(rides_df['started_at']).dt.year

df_2018['month'] = pd.to_datetime(df_2018['start_time']).dt.month
df_2018['year'] = pd.to_datetime(df_2018['start_time']).dt.year

rides_df.head(10)

rides_df['trip_duration'] = rides_df['Ride_end_timestamp'] - rides_df['Ride_start_timestamp']

df_2018['trip_duration'] = df_2018['Ride_end_timestamp'] - df_2018['Ride_start_timestamp']

df_2018.head()

# ## summary statistics


# Summary statistics for trip durations in 2018
statistics_2018 = df_2018[df_2018['year'] == 2018]['trip_duration'].describe()

# Summary statistics for trip durations in 2023
statistics_2023 = rides_df[rides_df['year'] == 2023]['trip_duration'].describe()
statistics_2018

statistics_2023

rides_df.head(2)

df_2018.head(1)


rides_df['started_at'] = pd.to_datetime(rides_df['started_at'])
rides_df['day'] = rides_df['started_at'].dt.date

df_2018['start_time'] = pd.to_datetime(df_2018['start_time'])
df_2018['day'] = df_2018['start_time'].dt.date


#daily_counts = rides_df.groupby('day').size()
#weekly_counts = rides_df.groupby('week').size()

import matplotlib.pyplot as plt

monthly_counts = rides_df.groupby('month').size()
daily_counts = rides_df.groupby('day').size()
monthly_counts_2018 = df_2018.groupby('month').size()
daily_counts_2018 = df_2018.groupby('day').size()

# Plot time series plots
plt.figure(figsize=(12, 6))

plt.subplot(4, 1, 1)
monthly_counts.plot(kind='line')
plt.title('Monthly Bike Rentals in 2023-2024')
plt.xlabel('Month')
plt.ylabel('Number of Rentals')

plt.subplot(4, 1, 2)
daily_counts.plot(kind='line')
plt.title('Daily Bike Rentals in 2023-2024')
plt.xlabel('Day')
plt.ylabel('Number of Rentals')


plt.subplot(4, 1, 3)
monthly_counts_2018.plot(kind='line')
plt.title('Monthly Bike Rentals in 2018')
plt.xlabel('Month')
plt.ylabel('Number of Rentals')


plt.subplot(4, 1, 4)
daily_counts_2018.plot(kind='line')
plt.title('Daily Bike Rentals in 2018')
plt.xlabel('Day')
plt.ylabel('Number of Rentals')

plt.tight_layout()
plt.show()


rides_df['started_at'] = pd.to_datetime(rides_df['started_at'])

# Extract the day of the week (0=Monday, 6=Sunday)
rides_df['day_of_week'] = rides_df['started_at'].dt.dayofweek

# Map day of the week to weekday/weekend
rides_df['day_type'] = rides_df['day_of_week'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')

# Group by weekday/weekend and count the number of trips
ridership_by_daytype = rides_df.groupby('day_type').size()

# Plot ridership patterns
plt.figure(figsize=(8, 6))
ridership_by_daytype.plot(kind='bar', color=['blue', 'orange'])
plt.title('Ridership Patterns: Weekdays vs. Weekends 2023-2024')
plt.xlabel('Day Type')
plt.ylabel('Number of Trips')
plt.xticks(rotation=0)
plt.show()




df_2018['start_time'] = pd.to_datetime(df_2018['start_time'])

# Extract the day of the week (0=Monday, 6=Sunday)
df_2018['day_of_week'] = df_2018['start_time'].dt.dayofweek

# Map day of the week to weekday/weekend
df_2018['day_type'] = df_2018['day_of_week'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')

# Group by weekday/weekend and count the number of trips
ridership_by_daytype = df_2018.groupby('day_type').size()

# Plot ridership patterns
plt.figure(figsize=(8, 6))
ridership_by_daytype.plot(kind='bar', color=['blue', 'orange'])
plt.title('Ridership Patterns: Weekdays vs. Weekends 2018')
plt.xlabel('Day Type')
plt.ylabel('Number of Trips')
plt.xticks(rotation=0)
plt.show()


rides_df.to_csv('cleaned_2023_24_bikerides.csv',index=False)

df_2018.to_csv('cleaned_2018_bikerides.csv',index=False)


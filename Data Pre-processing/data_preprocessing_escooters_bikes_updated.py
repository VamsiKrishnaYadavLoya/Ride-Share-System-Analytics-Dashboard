import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind


escooter = pd.read_csv('cleaned_e_scooter_trip_data.csv')
bike1 = pd.read_csv('cleaned_bike_rides_data_2022_2023.csv')

bike2 = pd.read_csv('cleaned_2018_bikerides.csv')

bike1['rideable_type'].value_counts()
test1 = bike1[['ride_id','Ride_start_timestamp','Ride_end_timestamp']]

test2 = bike2[['rentID','Ride_start_timestamp','Ride_end_timestamp']]

test2.columns = ['ride_id','Ride_start_timestamp','Ride_end_timestamp']

test2.columns

escooter.columns

bike_data = pd.concat([test1,test2])

bike_data.columns

# Convert the timestamp column to datetime type
bike_data['Ride_start_timestamp'] = pd.to_datetime(bike_data['Ride_start_timestamp'])

# Extract the hour of the day
bike_data['hour_of_day'] = bike_data['Ride_start_timestamp'].dt.hour


bike_data.head()

# Group by hour_of_day and count ride_id
hourly_counts = bike_data.groupby('hour_of_day').size()

# Plotting the bar chart
hourly_counts.plot(kind='bar', color='skyblue')
plt.title('Hourly Ride Counts for Bikes')
plt.xlabel('Hour of the Day')
plt.ylabel('Count of Rides')
plt.xticks(rotation=0)
plt.show()


# Convert the timestamp column to datetime type
escooter['Start Time'] = pd.to_datetime(escooter['Start Time'])
# Extract the hour of the day
escooter['hour_of_day'] = escooter['Start Time'].dt.hour


hourly_counts = escooter.groupby('hour_of_day').size()

# Plotting the bar chart
hourly_counts.plot(kind='bar', color='skyblue')
plt.title('Hourly Ride Counts for Escooters')
plt.xlabel('Hour of the Day')
plt.ylabel('Count of Rides')
plt.xticks(rotation=0)
plt.show()


# # Bike-shares season


# Define function to map months to seasons
def get_season(month):
    if 3 <= month <= 5:
        return 'Spring'
    elif 6 <= month <= 8:
        return 'Summer'
    elif 9 <= month <= 11:
        return 'Fall'
    else:
        return 'Winter'

# Extract month from timestamp and map to season
bike_data['season'] = bike_data['Ride_start_timestamp'].dt.month.map(get_season)
escooter['season'] = escooter['Start Time'].dt.month.map(get_season)
escooter['season'].value_counts()
bike_data['season'].value_counts()


# Group by season and count ride_id
season_counts = bike_data.groupby('season').size()

# Plotting the bar chart
season_counts.plot(kind='bar', color='skyblue')
plt.title('Ride Counts by Season - Bikes')
plt.xlabel('Season')
plt.ylabel('Count of Rides')
plt.xticks(rotation=0)
plt.show()



# Group by season and count ride_id
season_counts = escooter.groupby('season').size()

# Plotting the bar chart
season_counts.plot(kind='bar', color='skyblue')
plt.title('Ride Counts by Season - escooter')
plt.xlabel('Season')
plt.ylabel('Count of Rides')
plt.xticks(rotation=0)
plt.show()


# # Bike shares - Trip Duration


# Convert start_timestamp and end_timestamp columns to datetime
bike_data['Ride_start_timestamp'] = pd.to_datetime(bike_data['Ride_start_timestamp'])
bike_data['Ride_end_timestamp'] = pd.to_datetime(bike_data['Ride_end_timestamp'])

# Calculate trip duration
bike_data['trip_duration'] = bike_data['Ride_end_timestamp'] - bike_data['Ride_start_timestamp']

# Convert trip duration to minutes
bike_data['trip_duration_minutes'] = bike_data['trip_duration'].dt.total_seconds() / 60


escooter['Start Time'] = pd.to_datetime(escooter['Start Time'])
escooter['End Time'] = pd.to_datetime(escooter['End Time'])

# Calculate trip duration
escooter['trip_duration'] = escooter['End Time'] - escooter['Start Time']

# Convert trip duration to minutes
escooter['trip_duration_minutes'] = escooter['trip_duration'].dt.total_seconds() / 60



escooter_trip = escooter[['Trip ID','Start Time','End Time','trip_duration','trip_duration_minutes']]

escooter_trip['transportation'] = 'escooter'


bike_data['transportation'] = 'bike'


bike_data_1 = bike_data[['ride_id', 'Ride_start_timestamp', 'Ride_end_timestamp','trip_duration_minutes', 'transportation']]

bike_data_1.shape

escooter_trip.columns

escooter_trip_1 = escooter_trip[['Trip ID', 'Start Time', 'End Time','trip_duration_minutes', 'transportation']]
escooter_trip_1.columns = ['ride_id', 'Ride_start_timestamp', 'Ride_end_timestamp','trip_duration_minutes','transportation']
merged_df = pd.concat([escooter_trip_1, bike_data_1])
merged_df

shuffled_df = merged_df.sample(frac=1)

shuffled_df

# Split data into two groups based on transportation type
escooter_trips = merged_df[merged_df['transportation'] == 'escooter']['trip_duration_minutes']
bike_trips = merged_df[merged_df['transportation'] == 'bike']['trip_duration_minutes']

# Perform t-test
t_stat, p_value = ttest_ind(escooter_trips, bike_trips, equal_var=False)

# Check significance
if p_value < 0.05:
    print("There is a significant difference between trip durations for escooter and bike rides.")
else:
    print("There is no significant difference between trip durations for escooter and bike rides.")


# Calculate average trip duration for each transportation type
avg_trip_duration_escooter = merged_df[merged_df['transportation'] == 'escooter']['trip_duration_minutes'].mean()
avg_trip_duration_bike = merged_df[merged_df['transportation'] == 'bike']['trip_duration_minutes'].mean()

# Use the average trip duration as the benchmark
benchmark_duration = (avg_trip_duration_escooter + avg_trip_duration_bike) / 2

print("Average trip duration for escooter rides:", avg_trip_duration_escooter)
print("Average trip duration for bike rides:", avg_trip_duration_bike)
print("Benchmark duration:", benchmark_duration)


merged_df['preference'] = merged_df['trip_duration_minutes'].apply(lambda x: 'escooter' if x > benchmark_distance else 'bike')


# Calculate average trip duration for each transportation type
avg_trip_duration = merged_df.groupby('transportation')['trip_duration_minutes'].mean()

# Plot bar chart
avg_trip_duration.plot(kind='bar', color=['skyblue', 'lightgreen'])
plt.title('Average Trip Duration by Transportation')
plt.xlabel('Transportation')
plt.ylabel('Average Trip Duration (minutes)')
plt.xticks(rotation=0)
plt.legend()
plt.show()


escooter.to_csv('escooter_with_trip_duration.xlsx',index=False)
bike_data.to_csv('bike_data_with_trip_duration.xlsx',index=False)
merged_df.to_csv('merged_data_bike_escooter.xlsx',index=False)
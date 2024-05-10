
import pandas as pd


df1 = pd.read_csv(r"202301-divvy-tripdata.csv")
df2 = pd.read_csv(r"202302-divvy-tripdata.csv")
df3 = pd.read_csv(r"202303-divvy-tripdata.csv")
df4 = pd.read_csv(r"202304-divvy-tripdata.csv")
df5 = pd.read_csv(r"202205-divvy-tripdata.csv")
df6 = pd.read_csv(r"202206-divvy-tripdata.csv")
df7 = pd.read_csv(r"202207-divvy-tripdata.csv")
df8 = pd.read_csv(r"202208-divvy-tripdata.csv")
df9 = pd.read_csv(r"202210-divvy-tripdata.csv")
df10 = pd.read_csv(r"202211-divvy-tripdata.csv")
df11 = pd.read_csv(r"202212-divvy-tripdata.csv")
df12 = pd.read_csv(r"202209-divvy-publictripdata.csv")



escooter_data = pd.read_csv(r"E-Scooter_Trips_20240215.csv")


rides_df = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,],axis=0)



rides = rides_df.dropna()

#remove null values
rides.shape
df1['start_station_name'].value_counts()
df1['end_station_name'].value_counts()
rides['rideable_type'].value_counts()
rides['start_lat'].value_counts()
rides['member_casual'].value_counts()

rides['start_lat'].max()

rides['start_lat'].min()

#Features generation
#1. date time columns, new columns month and year
#3. drop null values
#2. Generate new columns (ridecount) #perform groupby based on start and end location

rides['month'] = pd.to_datetime(rides['started_at']).dt.month
rides['year'] = pd.to_datetime(rides['started_at']).dt.year
rides.head()
rides.dtypes


# Example custom format: "DD/MM/YYYY HH:MM"
rides['Ride_start_timestamp'] = pd.to_datetime(rides['started_at'], format="mixed")
rides['Ride_end_timestamp'] = pd.to_datetime(rides['ended_at'], format="mixed")

rides_final = rides[['ride_id', 'rideable_type','start_station_name', 'start_station_id', 'end_station_name','end_station_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng','member_casual', 'Ride_start_timestamp', 'Ride_end_timestamp', 'month','year']]
rides_final.shape

rides_final.head(2)

rides_final.to_csv('cleaned_bike_rides_data_2022_2023.csv',index=False)


# #  Exploratory Data analysis

# Check how many count of rides taking places from start location to end location in a month
# To check reperated patterns from start statiom to end station for each month
import pandas as pd
import matplotlib.pyplot as plt


ride_counts = rides.groupby(['start_station_id', 'end_station_id', 'month'])['ride_id'].count().unstack()

# Group months together for comparison
monthly_counts = ride_counts.sum(axis=0)

# Plot using Matplotlib
monthly_counts.plot(kind='bar')
plt.xlabel("Start Location - End Location")
plt.ylabel("Total Rides per Month")
plt.title("Monthly Ride Counts by Start and End Location")
plt.show()



# Assuming you have the value counts already:
station_counts = rides['start_station_name'].value_counts()

# Option 1: Using nlargest()
top_4_stations = station_counts.nlargest(4).index.tolist()
top_4_stations

# Assuming you have the value counts already:
end_station_counts = rides['end_station_name'].value_counts()

# Option 1: Using nlargest()
top_4_end_stations = end_station_counts.nlargest(4).index.tolist()
top_4_end_stations

#Improving the heatmaps:
#Filter for weekdays or weekends to see if ride patterns differ.
#Create separate heatmaps for each month to analyze seasonal variations.
#The heatmap provide insights on most popular start and end locations for a ride in a particular month 
# we can extend it to particular days, seansons,weekends and weekdays 


import seaborn as sns

# Plot heatmap
# for one month == 01,02

##Chosen 
filtered_rides = rides[rides['month'].isin([1, 2,3,4,5,6,7,8,9])]
filtered_rides = filtered_rides[filtered_rides['start_station_name'].isin(top_4_stations)]
filtered_rides = filtered_rides[filtered_rides['end_station_name'].isin(top_4_end_stations)]
ride_counts = filtered_rides.groupby(['start_station_id', 'end_station_id', 'month'])['ride_id'].count().unstack()

sns.heatmap(ride_counts)
plt.xlabel("Start Location")
plt.ylabel("End Location")
plt.title("Monthly Ride Counts by Start and End Location")
plt.show()


##Scatter Plot
import matplotlib.pyplot as plt

x = df1['start_lat']
y = df1['end_lat']

min_start_lat = df1['start_lat'].min()
max_start_lat = df1['start_lat'].max()
min_end_lat = df1['end_lat'].min()
max_end_lat = df1['end_lat'].max()


color_mapping = {
    "electric_bike": "blue",
    "classic_bike": "red",
    "docked_bike":"green"
}

colors = [color_mapping[value] for value in df1["rideable_type"]]

# Create the scatter plot
plt.scatter(x, y, c=colors)

# Add labels and title
plt.xlabel("Start Latitude")
plt.ylabel("End Latitude")
plt.title("Scatter Plot of Start vs. End Latitudes")

# Set axis limits
plt.xlim(min_start_lat, max_start_lat)
plt.ylim(min_end_lat, max_end_lat)

# Increase ticks and adjust labels
plt.xticks(np.arange(min_start_lat, max_start_lat + 0.1, 0.1))
plt.yticks(np.arange(min_end_lat, max_end_lat + 0.1, 0.1))


# Show the plot
plt.show()
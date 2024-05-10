import pandas as pd

df = pd.read_csv('bike_data_with_trip_duration.xlsx')
merged_df = pd.read_csv('merged_data_bike_escooter.xlsx')

merged_df.columns


##Features ----->   Season,Duration(min),distance(KM)


final_merged_df['Ride_start_timestamp'] = pd.to_datetime(final_merged_df['Ride_start_timestamp'])

# Extract the hour of the day
final_merged_df['hour_of_day'] = final_merged_df['Ride_start_timestamp'].dt.hour



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
final_merged_df['season'] = final_merged_df['Ride_start_timestamp'].dt.month.map(get_season)
final_merged_df['season'].value_counts()


#-------------------------------------------------------------Model part ---------------------------------------------

import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels
from statsmodels.genmod.families import Poisson
from statsmodels.tools.eval_measures import rmse

#from sklearn.cross_validation import train_test_split
from sklearn import metrics 
from sklearn.metrics import r2_score 
from sklearn.linear_model import LinearRegression 
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings("ignore")

statsmodels.__version__


# poisson regression prediction
def pr_predict(x, y):
    #############################
    #here is for train/test ratio 80:20 
    size = 0.2

    #train r2, rmse
    print("PR train r2 and rmse")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = size)
    print(y_train, y_test)
    pm_train = sm.GLM(y_train, x_train, family=sm.families.Poisson()).fit()
    print(np.sqrt(metrics.mean_squared_error(y_train, pm_train.predict(x_train))))
    #test r2, rmse
    print("PR test r2 and rmse")
    pm_test = sm.Poisson(y_train, x_train).fit()
    y_pred = pm_test.predict(x_test)
    
    threshold = 0.5
    binary_predictions = (y_pred >= threshold).astype(int)
    
    print("\n********************************")
    print(np.sqrt(metrics.mean_squared_error(y_test, binary_predictions)))
     
    df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    df1 = df.head(20000)
    df1.sort_index(inplace=True)
    plt.plot(df1['Actual'], c="blue", label="actual", linewidth=2)
    plt.plot(df1['Predicted'], c="red", label="predicted", linewidth=2)
    plt.savefig( "weather_pr_line.png")
    plt.show()
    plt.clf()
    plt.cla()
    plt.close()



# poisson regression
def poission_regression(df):
    # create a poisson regression model
    print("\--------------------------------------")
    print("\poisson regression with constant")
    print("\--------------------------------------")
    pd.set_option('display.max_columns', None)
    df = pd.concat((df, pd.get_dummies(df['season'])), axis=1)
    print(df.columns)
    
#     transportation_encoding = pd.get_dummies(df['transportation'])
#     print("Encoding mapping:")
#     print(transportation_encoding)
    
#     df['transportation_encoded'] = pd.get_dummies(df['transportation'])['escooter']
#     # Change data type to integer
#     df['transportation_encoded'] = df['transportation_encoded'].astype(int)
    
    # Create a mapping dictionary
#     transportation_map = {'bike': 0, 'escooter': 1}

#     # Map the values in the 'transportation' column using the mapping dictionary
#     df['transportation_encoded'] = df['transportation'].map(transportation_map)

    y = df['transportation_encoded']
    #x = df[['Spring', 'Summer','Fall','Winter']]
    #x = df[['distance']]
    x = df[['trip_duration_minutes']]
    x = sm.add_constant(x)
    x = x.astype(float)

    pm = sm.GLM(y, x, family=sm.families.Poisson()).fit()
    print(pm.summary().as_latex())
    print("poisson regression's rmse value")
    print(sm.tools.eval_measures.rmse(y, pm.fittedvalues, axis=0))

    pr_predict(x, y)


final_merged_df.shape


# Splitting the DataFrame based on 'transportation' values
bike_df = final_merged_df[final_merged_df['transportation'] == 'bike']
escooter_df = final_merged_df[final_merged_df['transportation'] == 'escooter']

# Sampling from each DataFrame to match the counts
bike_sampled = bike_df.sample(n=20723, random_state=42)
escooter_sampled = escooter_df.sample(n=20723, random_state=42)

# Concatenating the sampled DataFrames
sampled_df = pd.concat([bike_sampled, escooter_sampled])

# Shuffle the DataFrame to ensure randomness
sampled_df = sampled_df.sample(frac=1, random_state=42)

sampled_df['transportation'].value_counts()


sampled_df.head()
#sampled_df.drop(columns=['transportation_encoded'], inplace=True)
sampled_df.columns


# # Run Model

poission_regression(sampled_df)


# # Distance Calculation
import pandas as pd
import math
escooter = pd.read_csv('cleaned_e_scooter_trip_data.csv')
bike1 = pd.read_csv('cleaned_bike_rides_data_2022_2023.csv')
escooter.columns = ['ride_id', 'Start Time', 'End Time', 'Vendor',
       'Start Community Area Number', 'End Community Area Number',
       'Start Community Area Name', 'End Community Area Name',
       'start_lat', 'start_lng',
       'Start Centroid Location', 'end_lat',
       'end_lng', 'End Centroid Location',
       'Trip Distance (miles)', 'Trip Duration (minutes)']

#Calculate the distance based on the radius
def distance(row):
    radius = 6373.0 # km
    lat1 = math.radians(float(row['start_lat']))
    lat2 = math.radians(float(row['start_lng']))
    lon1 = math.radians(float(row['end_lat']))
    lon2 = math.radians(float(row['end_lng']))

    #print(lat1, lat2, lon1, lon2)
    dlat = lat2-lat1
    dlon = lon2-lon1
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d



escooter['distance'] = escooter.apply(distance, axis=1)
bike1.columns
temp1 = bike1[['ride_id','distance']]
temp2 = escooter[['ride_id','distance']]
final_temp = pd.concat([temp1, temp2], ignore_index=True)
final_temp.columns
merged_df.columns

final_merged_df = pd.merge(merged_df, final_temp, on='ride_id')
final_merged_df.shape
final_merged_df.columns
merged_df.isna().sum()

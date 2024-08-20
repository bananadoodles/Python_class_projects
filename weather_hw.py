# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import modules
import requests
import sys
#import os
import pandas as pd
from datetime import timedelta

#Erin Blake


#api key from weather app
api_key = 'd5a1ee02376a9de1ca27683738f22a4e'
 
#ARGENTINA IS SPELLED WRONG ON THE ASSIGNMENT
cities=["Buenos Aires, Argentina","Guangzhou, China","Wichita, Kansas","Niskayuna, New York","Gwangmyeong, South Korea","Taipei, Taiwan",
        "Nanaimo, British Columbia","Chennai, India","Barrington, Illinois","Littleton, Colorado","Peterhead, Scotland","Vizag, India",
        "Des Moines, Iowa","Beijing, China","Killeen, Texas","Morehead City, North Carolina"]

#do a loop to go through all the cities in the list above

final_weather_df=pd.DataFrame()
for i in cities:
    URL = 'http://api.openweathermap.org/geo/1.0/direct'
    city = i
    geo = f'{URL}?q={city}&limit=5&appid={api_key}'
    resp = requests.get( geo )

    if resp.status_code != 200:  # Failure?
        print( f'Error geocoding {city}: {resp.status_code}' )
        sys.exit( 1 )
 
    #  OpenWeatherMap returns a list of matching cities, up to the limit specified
    #  in the API call; even if you only ask for one city (limit=5), it's still
    #  returned as a 1-element list
    if len( resp.json() ) == 0:  # No such city?
        print( f'Error locating city {city}; {resp.status_code}' )
        sys.exit( 2 )

    rj = resp.json()
    if type( rj ) == list:  # List of cities?
        lat = rj[ 0 ][ 'lat' ]
        lon = rj[ 0 ][ 'lon' ]
   
    else:  # Unknown city?
        print(type( rj ))
        print(str(rj))
        print( f'Error, invalid data returned for city {city}, {resp.status_code}' )
        sys.exit( 3 )


    #  Use latitude and longitude to get it's 5-day forecast in 3-hour
    #  blocks

    URL2 = 'http://api.openweathermap.org/data/2.5/forecast'
    forecast = f'{URL2}?lat={lat}&lon={lon}&appid={api_key}'
    resp = requests.get( forecast )

    if resp.status_code != 200:  # Failure?
        print( f'Error retrieving data: {resp.status_code}' )
        sys.exit( 4 )

    #get the JSON response from api call
    data = resp.json()

    #make dataframe out of the JSON response
    weather_df= pd.json_normalize(data['list'])
    weather_df=weather_df[['main.temp_min','main.temp_max','dt_txt']]
    weather_df['City']=city
    final_weather_df=pd.concat([final_weather_df,weather_df])
   

#move columns around
final_weather_df.insert(0, "City", final_weather_df.pop('City'))
final_weather_df.insert(1, "dt_txt", final_weather_df.pop('dt_txt'))

#make dt_txt a datetime object and extract the day and hour compoenent
final_weather_df['dt_txt']=pd.to_datetime(final_weather_df['dt_txt'],format="%Y-%m-%d %H:%M:%S")

#USE this to convert values from Kelvin to Celsius
K=273.15


#get hour and day components of the datetime column
final_weather_df['day'] = final_weather_df['dt_txt'].dt.date
final_weather_df['hour']=final_weather_df['dt_txt'].dt.hour
final_weather_df['main.temp_min']=final_weather_df['main.temp_min']-K
final_weather_df['main.temp_max']=final_weather_df['main.temp_max']-K
final_weather_df.insert(2, "day", final_weather_df.pop('day'))
final_weather_df.insert(3, "hour", final_weather_df.pop('hour'))


#get the min date that has midnight hour
min_date=final_weather_df.loc[final_weather_df['hour']==0,"day"].min()

#add days to this date
max_date=min_date+ timedelta(days=4)

#get subset of these 4 days
subset_weather_df=final_weather_df[(final_weather_df['day']>=min_date)&(final_weather_df['day']<max_date)]

#get the min and max temps for each of the four days, rounded to 2 decimal points
#sort here make sure it keeps its order
min_agg_weather_df=subset_weather_df.groupby(['City','day'],as_index=False,sort=False).agg(min_temp=('main.temp_min', 'min')).round(2)
max_agg_weather_df=subset_weather_df.groupby(['City','day'],as_index=False,sort=False).agg(max_temp=('main.temp_max','max')).round(2)


#pivot wider and include new labels
min_df=min_agg_weather_df.pivot_table('min_temp', 'City', min_agg_weather_df.groupby('City',sort=False,as_index=False).cumcount()+1,sort=False).add_prefix('Min ')
max_df=max_agg_weather_df.pivot_table('max_temp', 'City', max_agg_weather_df.groupby('City',sort=False,as_index=False).cumcount()+1,sort=False).add_prefix('Max ')


#make sure the amounts are rounded to two decimal points
min_df['Min Avg']=round(min_df.mean(axis=1),2)
max_df['Max Avg']=round(max_df.mean(axis=1),2)

#reset the index so that city is in the csv correclty
output=min_df.merge(max_df,on='City').reset_index()

#put the columns in the right order, probably could have done this more automated but I lost the will
output.insert(1, "Min 1", output.pop('Min 1'))
output.insert(2, "Max 1", output.pop('Max 1'))
output.insert(3, "Min 2", output.pop('Min 2'))
output.insert(4, "Max 2", output.pop('Max 2'))
output.insert(5, "Min 3", output.pop('Min 3'))
output.insert(6, "Max 3", output.pop('Max 3'))
output.insert(7, "Min 4", output.pop('Min 4'))
output.insert(8, "Max 4", output.pop('Max 4'))
output.insert(len(output.columns)-2, "Min Avg", output.pop('Min Avg'))
output.insert(len(output.columns)-1, "Max Avg", output.pop('Max Avg'))

#write to csv, make sure it is writing to two decimalpoints
output.to_csv('temp.csv',index=False, float_format='%.2f')


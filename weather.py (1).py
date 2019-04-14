#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import json
# Import API key
from config import gkey

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# In[2]:


# Creating List to hold the latitude and longitude and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# In[3]:


# Starting URL for Weather Map API Call
url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID=" + gkey


# In[4]:


#convert into Dataframe

loc = pd.DataFrame()
loc['lat_values'] = [np.random.uniform(-90,90) for x in range(1500)]
loc['lng_values'] = [np.random.uniform(-180, 180) for x in range(1500)]

loc.head()
loc['city'] = ""
loc['country'] = ""

count = 0
for index, row in loc.iterrows():
    near_city = citipy.nearest_city(row['lat_values'], row['lng_values']).city_name
    near_country = citipy.nearest_city(row['lat_values'], row['lng_values']).country_code
    loc.set_value(index,"city",near_city)
    loc.set_value(index,"country",near_country)
loc.head()


# In[5]:


len(loc)


# In[6]:


loc=loc.drop_duplicates(['city','country'],keep = "first")
loc['Temperature'] = ""
loc['Humidity'] = ""
loc['Cloudiness'] = ""
loc['Wind Speed'] = ""
loc["Latitude"] =" "
loc["Longitude"] =" "


# In[7]:


#500 cities to sample and show headers
sample_size = 500
target_url = 'http://api.openweathermap.org/data/2.5/weather?q='
units = 'imperial'


# In[8]:


loc.head()


# In[9]:


#generate
record = 0
for index, row in loc.iterrows():
    city_name = row['city']
    country_code = row['country']
    url = target_url + city_name + ',' + country_code + '&units=' + units + '&APPID=' + gkey
    print (url)
    
    try: 
        
        weather_response = req.get(url)
        weather_json = weather_response.json()
        
        latitude  = weather_json["coord"]["lat"]
        longitude = weather_json["coord"]["lon"]
        temp      = weather_json["main"]["temperature"]
        humidity  = weather_json["main"]["humidity"]
        cloud     = weather_json["clouds"]["all"]
        wind      = weather_json["wind"]["speed"]
        
        
        loc.set_value(index,"Temperature", temp)
        loc.set_value(index,"Humidity",humidity)
        loc.set_value(index,"Wind Speed", wind)
        loc.set_value(index,"Cloudiness",cloud)
        loc.set_value(index,"Latitude", latitude)
        loc.set_value(index,"Longitude",longitude)
        
        print("No found data for %s, %s" % (city_name,country_code))
    except:    
        print("Processing Record for %s, %s" % (city_name, country_code))
    record += 1
    if record % 59 == 0:
        time.sleep(60)


# In[10]:


loc.head(20)


# In[16]:


loc['Latitude'] = pd.to_numeric(loc['Latitude'])
loc['Temperature'] = pd.to_numeric(loc['Temperature'])
loc['Humidity'] = pd.to_numeric(loc['Humidity'])
loc['Wind Speed'] = pd.to_numeric(loc['Wind Speed'])
loc['Cloudiness'] = pd.to_numeric(loc['Cloudiness'])


# In[14]:


loc.head(50)


# In[15]:


#set up axes
x_axis = loc['Latitude']
y_axis = loc['Temperature']


x_min=x_axis.min()-10
x_max=x_axis.max()+10

y_min=y_axis.min()-10
y_max=y_axis.max()+10

plt.title("Temperature (F) vs. Latitude")
plt.xlabel("Latitude\n")
plt.ylabel("\nTemp (degrees F)")

#generating plot.blue color

plt.scatter(x_axis, y_axis, marker="o", color="b")
plot.show()


# In[ ]:





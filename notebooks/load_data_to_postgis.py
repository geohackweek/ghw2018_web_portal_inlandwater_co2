# coding: utf-8

# In[1]:


# # start with same libraries as vector tutorial
# get_ipython().run_line_magic('matplotlib', 'inline')

from __future__ import (absolute_import, division, print_function)
import os
import sys
import json
import psycopg2


from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from geopandas import GeoSeries, GeoDataFrame


# In[2]:


# load data
co2_data_table = pd.read_excel("/usr/src/app/data/co2.xlsx", skiprows=range(1, 2))

# set up geometry
geometry = [Point(xy) for xy in zip(co2_data_table['Longitude'], co2_data_table['Latitude'])]
geometry = GeoSeries(geometry)
geometry.crs = {'init': 'epsg:4326'}

co2_geo_data_table = GeoDataFrame(co2_data_table, geometry=geometry, crs=geometry.crs)


# # Lets view our data from the Excel File!

# In[3]:


# print(len(co2_geo_data_table))
# print(co2_geo_data_table.columns)
# co2_geo_data_table.head(3)


# We are going to select all the unique locations from the Exel file, drop any columns where there are null values and reset the index to create a new clean locations dataframe.

# In[4]:


co2_data_locations = co2_geo_data_table[["Latitude", "Longitude", "Altitude", "Site Type"]].drop_duplicates()
# good_co2_data_locations = co2_data_locations.dropna()
# co2_data_locations_clean = good_co2_data_locations.reset_index(drop='index')
co2_data_locations_clean = co2_data_locations.reset_index(drop='index')
# co2_data_locations_clean.head(5)
# len(co2_data_locations_clean)
# co2_data_locations_clean.head(10)


# We are going to transform our dataframe above into a Geodataframe which will allow us to spaitally join our locations back to out samples. We are also creating a new column "location_id" which is going to be the index of our locations when we load them into the postgis db.

# In[5]:


geometry = [Point(xy) for xy in zip(co2_data_locations_clean['Longitude'], co2_data_locations_clean['Latitude'])]
geometry = GeoSeries(geometry)
geometry.crs = {'init': 'epsg:4326'}
co2_geometries = GeoDataFrame(co2_data_locations_clean, geometry=geometry, crs=geometry.crs)
co2_geometries
co2_geometries.loc[:, 'location_id'] = co2_geometries.index


# In[6]:


# print(len(co2_geometries))
# co2_geometries.head(10)


# Join our locations back to the samples geodataframe where the "Sample Point Geometry" equals the "Location Point Geometry"

# In[7]:



samples = gpd.sjoin(co2_geo_data_table, co2_geometries, how="inner", op='intersects')


# Get all the samples with CO2 data, remove duplicates and where CO2 sample measure is null

# In[8]:


co2_samples = samples[["DateTime", "CO2", "location_id"]]
# print(len(co2_samples))
# print(len(co2_samples.drop_duplicates()))
# print(len(co2_samples.loc[co2_samples["CO2"].notnull()].drop_duplicates()))
# co2_samples.head(10)


# Add the Sample Type CO2 with Unit 'uatm' since we are only currenlty loading CO2 observations and clean the joined sample data to prepare to load into postgis

# In[9]:


co2_samples["SampleType"] = 'CO2'
co2_samples["Unit"] = 'uatm'
co2_samples = co2_samples[["DateTime", "SampleType", "Unit", "CO2", "location_id"]]
legit_co2_samples = co2_samples[co2_samples.CO2.notnull()]
clean_co2_samples = legit_co2_samples.drop_duplicates().reset_index(drop='index')
clean_co2_samples["Index"] = clean_co2_samples.index
# print(len(clean_co2_samples))
# clean_co2_samples.head(10)


# Get all the samples with CO2 Flux data, remove duplicates and where CO2 Flux sample measure is null

# In[10]:


co2_flux_samples = samples[["DateTime", "CO2 Flux", "location_id"]]
# print(len(co2_flux_samples))
# print(len(co2_flux_samples.drop_duplicates()))
# print(len(co2_flux_samples.loc[co2_flux_samples["CO2 Flux"].notnull()].drop_duplicates()))
# co2_flux_samples.head(10)


# In[11]:


co2_flux_samples["SampleType"] = 'CO2 Flux'
co2_flux_samples["Unit"] = 'uatm'
co2_flux_samples = co2_flux_samples[["DateTime", "SampleType", "Unit", "CO2 Flux", "location_id"]]
legit_co2_flux_samples = co2_flux_samples[co2_flux_samples["CO2 Flux"].notnull()]
clean_co2_flux_samples = legit_co2_flux_samples.drop_duplicates().reset_index(drop='index')
clean_co2_flux_samples["Index"] = clean_co2_flux_samples.index
# print(len(clean_co2_flux_samples))
# clean_co2_flux_samples.head(10)


# In[12]:


# cast all the datetime column to datetime type
# Dirty data so we can't apply date_time to incorrect str formats
# samples.apply(lambda row:pd.to_datetime(row["DateTime"]), axis=1)


# ## Set up our DB Connection

# Read DB configuration and use to connect to database. Initialize cursor in the DB.

# In[13]:


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.json")) as f:
    db_conn_dict = json.load(f)

conn = psycopg2.connect(**db_conn_dict)
cur = conn.cursor()


# Create string template of SQL procedure to load the sitelocations into the database

# In[14]:


insert_locations_string = """
    INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point)
    values ({0}, LEFT('{1}', 150), {2}, {3}, cast(coalesce(nullif('{4}', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('{5}'), 4326))
"""


# In[15]:


co2_data_locations_clean[["location_id", "Site Type", "Latitude", "Longitude", "Altitude", "geometry"]].head(3)


# Iterate through the dataframe to load all the points into the DB finally!!!

# In[16]:


for index, row in co2_data_locations_clean[["location_id", "Site Type", "Latitude", "Longitude", "Altitude", "geometry"]].iterrows():

        print(insert_locations_string.format(row["location_id"], str(row["Site Type"]), float(row["Latitude"]), float(row["Longitude"]), float(row["Altitude"]), row["geometry"]))
        cur.execute(insert_locations_string.format(row["location_id"], str(row["Site Type"]), float(row["Latitude"]), float(row["Longitude"]), float(row["Altitude"]), row["geometry"]))
        conn.commit()


# Another template to load the data into Samples now.

# In[17]:


insert_samples_string = """
    INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id)
    values ('{0}', '{1}', '{2}', cast(coalesce(nullif('{3}', 'nan'), '0') as float), {4})
"""


# In[18]:


# clean_co2_samples.head(1)
# print(len(clean_co2_samples))


# Iterate through the dataframe to load all the co2 samples into the DB finally!!!

# In[19]:


for index, row in clean_co2_samples.iterrows():

        print(insert_samples_string.format(str(row["DateTime"]), str(row["SampleType"]), str(row["Unit"]), float(row["CO2"]), int(row["location_id"])))
        cur.execute(insert_samples_string.format(str(row["DateTime"]), str(row["SampleType"]), str(row["Unit"]), float(row["CO2"]), int(row["location_id"])))
        conn.commit()


# And CO2 Flux Samples...

# In[20]:


# clean_co2_flux_samples.head(1)
# print(len(clean_co2_flux_samples))


# In[21]:


for index, row in clean_co2_flux_samples.iterrows():

        print(insert_samples_string.format(str(row["DateTime"]), str(row["SampleType"]), str(row["Unit"]), float(row["CO2 Flux"]), int(row["location_id"])))
        cur.execute(insert_samples_string.format(str(row["DateTime"]), str(row["SampleType"]), str(row["Unit"]), float(row["CO2 Flux"]), int(row["location_id"])))
        conn.commit()


# Delete Cursur, Close DB Connection, AND FINISHED!!!

# In[22]:


cur.close()
conn.close()



```python
# start with same libraries as vector tutorial
%matplotlib inline

from __future__ import (absolute_import, division, print_function)
import os
import sys
import json
import psycopg2

import matplotlib as mpl
import matplotlib.pyplot as plt
import folium
from folium.plugins import TimeSliderChoropleth

from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from geopandas import GeoSeries, GeoDataFrame
```

    /root/miniconda/envs/backend/lib/python3.6/importlib/_bootstrap.py:219: RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility. Expected 96, got 88
      return f(*args, **kwds)



```python
%run -i load_data.py
```

# Lets view our data from the Excel File!


```python
print(len(co2_geo_data_table))
print(co2_geo_data_table.columns)
co2_geo_data_table.head(3)
```

    4569
    Index(['Reference', 'Site Type', 'Latitude', 'Longitude', 'DateTime',
           'Altitude', 'Discharge', 'Stream Slope', 'Width', 'Depth',
           'Flow Velocity', 'Wind Speed', 'POC', 'DOC', 'TOC', 'pH',
           'Water Temperature', 'Air Temperature', 'DO', 'Chl a', 'CO2', 'k',
           'k600', 'CO2 Flux', 'CO2 Flux.1', 'Source', 'geometry'],
          dtype='object')





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Reference</th>
      <th>Site Type</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>DateTime</th>
      <th>Altitude</th>
      <th>Discharge</th>
      <th>Stream Slope</th>
      <th>Width</th>
      <th>Depth</th>
      <th>...</th>
      <th>Air Temperature</th>
      <th>DO</th>
      <th>Chl a</th>
      <th>CO2</th>
      <th>k</th>
      <th>k600</th>
      <th>CO2 Flux</th>
      <th>CO2 Flux.1</th>
      <th>Source</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Alin and Richey, 2012</td>
      <td>small stream</td>
      <td>-10.066</td>
      <td>-67.606</td>
      <td>20040701</td>
      <td>150.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>28.1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>140.5</td>
      <td>NaN</td>
      <td>-18.104</td>
      <td>1381.28</td>
      <td>NaN</td>
      <td>Alin, S.R., and J.E. Richey. 2012. LBA-ECO CD-...</td>
      <td>POINT (-67.60599999999999 -10.066)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Alin and Richey, 2012</td>
      <td>small stream</td>
      <td>-10.066</td>
      <td>-67.606</td>
      <td>20040701</td>
      <td>150.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>28.1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>140.5</td>
      <td>NaN</td>
      <td>-18.320</td>
      <td>1267.75</td>
      <td>NaN</td>
      <td>Alin, S.R., and J.E. Richey. 2012. LBA-ECO CD-...</td>
      <td>POINT (-67.60599999999999 -10.066)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Alin and Richey, 2012</td>
      <td>small stream</td>
      <td>-10.066</td>
      <td>-67.606</td>
      <td>20040701</td>
      <td>150.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>28.1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>140.5</td>
      <td>NaN</td>
      <td>-35.512</td>
      <td>1449.39</td>
      <td>NaN</td>
      <td>Alin, S.R., and J.E. Richey. 2012. LBA-ECO CD-...</td>
      <td>POINT (-67.60599999999999 -10.066)</td>
    </tr>
  </tbody>
</table>
<p>3 rows × 27 columns</p>
</div>



We are going to select all the unique locations from the Exel file, drop any columns where there are null values and reset the index to create a new clean locations dataframe.


```python
co2_data_locations = co2_geo_data_table[["Latitude", "Longitude", "Altitude", "Site Type"]].drop_duplicates()
# good_co2_data_locations = co2_data_locations.dropna()
# co2_data_locations_clean = good_co2_data_locations.reset_index(drop='index')
co2_data_locations_clean = co2_data_locations.reset_index(drop='index')
co2_data_locations_clean.head(5)
len(co2_data_locations_clean)
co2_data_locations_clean.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Altitude</th>
      <th>Site Type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-10.066</td>
      <td>-67.606</td>
      <td>150.0</td>
      <td>small stream</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-9.751</td>
      <td>-67.672</td>
      <td>150.0</td>
      <td>small stream</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-9.016</td>
      <td>-68.584</td>
      <td>150.0</td>
      <td>small river</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-9.029</td>
      <td>-68.593</td>
      <td>150.0</td>
      <td>small river</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-3.063</td>
      <td>-60.272</td>
      <td>70.0</td>
      <td>large river</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-2.289</td>
      <td>-54.824</td>
      <td>60.0</td>
      <td>large lake/river</td>
    </tr>
    <tr>
      <th>6</th>
      <td>-2.454</td>
      <td>-54.482</td>
      <td>60.0</td>
      <td>large river</td>
    </tr>
    <tr>
      <th>7</th>
      <td>-3.058</td>
      <td>-60.288</td>
      <td>70.0</td>
      <td>large river</td>
    </tr>
    <tr>
      <th>8</th>
      <td>-2.418</td>
      <td>-54.875</td>
      <td>60.0</td>
      <td>large lake/river</td>
    </tr>
    <tr>
      <th>9</th>
      <td>-2.462</td>
      <td>-54.630</td>
      <td>60.0</td>
      <td>large river</td>
    </tr>
  </tbody>
</table>
</div>



We are going to transform our dataframe above into a Geodataframe which will allow us to spaitally join our locations back to out samples. We are also creating a new column "location_id" which is going to be the index of our locations when we load them into the postgis db.


```python
geometry = [Point(xy) for xy in zip(co2_data_locations_clean['Longitude'], co2_data_locations_clean['Latitude'])]
geometry = GeoSeries(geometry)
geometry.crs = {'init': 'epsg:4326'}
co2_geometries = GeoDataFrame(co2_data_locations_clean, geometry=geometry, crs=geometry.crs)
co2_geometries
co2_geometries.loc[:, 'location_id'] = co2_geometries.index
```


```python
print(len(co2_geometries))
co2_geometries.head(10)
```

    1414





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Altitude</th>
      <th>Site Type</th>
      <th>geometry</th>
      <th>location_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-10.066</td>
      <td>-67.606</td>
      <td>150.0</td>
      <td>small stream</td>
      <td>POINT (-67.60599999999999 -10.066)</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-9.751</td>
      <td>-67.672</td>
      <td>150.0</td>
      <td>small stream</td>
      <td>POINT (-67.672 -9.750999999999999)</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-9.016</td>
      <td>-68.584</td>
      <td>150.0</td>
      <td>small river</td>
      <td>POINT (-68.584 -9.016)</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-9.029</td>
      <td>-68.593</td>
      <td>150.0</td>
      <td>small river</td>
      <td>POINT (-68.593 -9.029)</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-3.063</td>
      <td>-60.272</td>
      <td>70.0</td>
      <td>large river</td>
      <td>POINT (-60.272 -3.063)</td>
      <td>4</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-2.289</td>
      <td>-54.824</td>
      <td>60.0</td>
      <td>large lake/river</td>
      <td>POINT (-54.824 -2.289)</td>
      <td>5</td>
    </tr>
    <tr>
      <th>6</th>
      <td>-2.454</td>
      <td>-54.482</td>
      <td>60.0</td>
      <td>large river</td>
      <td>POINT (-54.482 -2.454)</td>
      <td>6</td>
    </tr>
    <tr>
      <th>7</th>
      <td>-3.058</td>
      <td>-60.288</td>
      <td>70.0</td>
      <td>large river</td>
      <td>POINT (-60.288 -3.058)</td>
      <td>7</td>
    </tr>
    <tr>
      <th>8</th>
      <td>-2.418</td>
      <td>-54.875</td>
      <td>60.0</td>
      <td>large lake/river</td>
      <td>POINT (-54.875 -2.418)</td>
      <td>8</td>
    </tr>
    <tr>
      <th>9</th>
      <td>-2.462</td>
      <td>-54.630</td>
      <td>60.0</td>
      <td>large river</td>
      <td>POINT (-54.63 -2.462)</td>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>



Join our locations back to the samples geodataframe where the "Sample Point Geometry" equals the "Location Point Geometry"


```python

samples = gpd.sjoin(co2_geo_data_table, co2_geometries, how="inner", op='intersects')
```

Get all the samples with CO2 data, remove duplicates and where CO2 sample measure is null 


```python
co2_samples = samples[["DateTime", "CO2", "location_id"]]
print(len(co2_samples))
print(len(co2_samples.drop_duplicates()))
print(len(co2_samples.loc[co2_samples["CO2"].notnull()].drop_duplicates()))
co2_samples.head(10)
```

    4620
    3658
    1378





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DateTime</th>
      <th>CO2</th>
      <th>location_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20040701</td>
      <td>140.5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20040701</td>
      <td>140.5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20040701</td>
      <td>140.5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20040701</td>
      <td>140.5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20040701</td>
      <td>140.5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>256</th>
      <td>20050830</td>
      <td>2662.2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>257</th>
      <td>20050830</td>
      <td>2662.2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>258</th>
      <td>20050830</td>
      <td>2662.2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>259</th>
      <td>20050830</td>
      <td>2662.2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>0</th>
      <td>20040701</td>
      <td>140.5</td>
      <td>63</td>
    </tr>
  </tbody>
</table>
</div>



Add the Sample Type CO2 with Unit 'uatm' since we are only currenlty loading CO2 observations and clean the joined sample data to prepare to load into postgis


```python
co2_samples["SampleType"] = 'CO2'
co2_samples["Unit"] = 'uatm'
co2_samples = co2_samples[["DateTime", "SampleType", "Unit", "CO2", "location_id"]]
legit_co2_samples = co2_samples[co2_samples.CO2.notnull()]
clean_co2_samples = legit_co2_samples.drop_duplicates().reset_index(drop='index')
clean_co2_samples["Index"] = clean_co2_samples.index
print(len(clean_co2_samples))
clean_co2_samples.head(10)
```

    1378


    load_data.py:1: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      #!/bin/env python
    load_data.py:2: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      # Elena C Reinisch 20180912





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DateTime</th>
      <th>SampleType</th>
      <th>Unit</th>
      <th>CO2</th>
      <th>location_id</th>
      <th>Index</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20040701</td>
      <td>CO2</td>
      <td>uatm</td>
      <td>140.5</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20050830</td>
      <td>CO2</td>
      <td>uatm</td>
      <td>2662.2</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20040701</td>
      <td>CO2</td>
      <td>uatm</td>
      <td>140.5</td>
      <td>63</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20050830</td>
      <td>CO2</td>
      <td>uatm</td>
      <td>2662.2</td>
      <td>63</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20040702</td>
      <td>CO2</td>
      <td>uatm</td>
      <td>860.3</td>
      <td>60</td>
      <td>4</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20050826</td>
      <td>CO2</td>
      <td>uatm</td>
      <td>3228.9</td>
      <td>60</td>
      <td>5</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20040702</td>
      <td>CO2</td>
      <td>uatm</td>
      <td>860.3</td>
      <td>61</td>
      <td>6</td>
    </tr>
    <tr>
      <th>7</th>
      <td>20050826</td>
      <td>CO2</td>
      <td>uatm</td>
      <td>3228.9</td>
      <td>61</td>
      <td>7</td>
    </tr>
    <tr>
      <th>8</th>
      <td>20040702</td>
      <td>CO2</td>
      <td>uatm</td>
      <td>860.3</td>
      <td>1</td>
      <td>8</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20050826</td>
      <td>CO2</td>
      <td>uatm</td>
      <td>3228.9</td>
      <td>1</td>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>



Get all the samples with CO2 Flux data, remove duplicates and where CO2 Flux sample measure is null 


```python
co2_flux_samples = samples[["DateTime", "CO2 Flux", "location_id"]]
print(len(co2_flux_samples))
print(len(co2_flux_samples.drop_duplicates()))
print(len(co2_flux_samples.loc[co2_flux_samples["CO2 Flux"].notnull()].drop_duplicates()))
co2_flux_samples.head(10)
```

    4620
    3890
    583





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DateTime</th>
      <th>CO2 Flux</th>
      <th>location_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20040701</td>
      <td>1381.28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20040701</td>
      <td>1267.75</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20040701</td>
      <td>1449.39</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20040701</td>
      <td>1025.55</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20040701</td>
      <td>1411.55</td>
      <td>0</td>
    </tr>
    <tr>
      <th>256</th>
      <td>20050830</td>
      <td>1188.28</td>
      <td>0</td>
    </tr>
    <tr>
      <th>257</th>
      <td>20050830</td>
      <td>1002.84</td>
      <td>0</td>
    </tr>
    <tr>
      <th>258</th>
      <td>20050830</td>
      <td>1059.61</td>
      <td>0</td>
    </tr>
    <tr>
      <th>259</th>
      <td>20050830</td>
      <td>1097.45</td>
      <td>0</td>
    </tr>
    <tr>
      <th>0</th>
      <td>20040701</td>
      <td>1381.28</td>
      <td>63</td>
    </tr>
  </tbody>
</table>
</div>




```python
co2_flux_samples["SampleType"] = 'CO2 Flux'
co2_flux_samples["Unit"] = 'uatm'
co2_flux_samples = co2_flux_samples[["DateTime", "SampleType", "Unit", "CO2 Flux", "location_id"]]
legit_co2_flux_samples = co2_flux_samples[co2_flux_samples["CO2 Flux"].notnull()]
clean_co2_flux_samples = legit_co2_flux_samples.drop_duplicates().reset_index(drop='index')
clean_co2_flux_samples["Index"] = clean_co2_flux_samples.index
print(len(clean_co2_flux_samples))
clean_co2_flux_samples.head(10)
```

    583


    load_data.py:1: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      #!/bin/env python
    load_data.py:2: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      # Elena C Reinisch 20180912





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DateTime</th>
      <th>SampleType</th>
      <th>Unit</th>
      <th>CO2 Flux</th>
      <th>location_id</th>
      <th>Index</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20040701</td>
      <td>CO2 Flux</td>
      <td>uatm</td>
      <td>1381.28</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20040701</td>
      <td>CO2 Flux</td>
      <td>uatm</td>
      <td>1267.75</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>20040701</td>
      <td>CO2 Flux</td>
      <td>uatm</td>
      <td>1449.39</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20040701</td>
      <td>CO2 Flux</td>
      <td>uatm</td>
      <td>1025.55</td>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>20040701</td>
      <td>CO2 Flux</td>
      <td>uatm</td>
      <td>1411.55</td>
      <td>0</td>
      <td>4</td>
    </tr>
    <tr>
      <th>5</th>
      <td>20050830</td>
      <td>CO2 Flux</td>
      <td>uatm</td>
      <td>1188.28</td>
      <td>0</td>
      <td>5</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20050830</td>
      <td>CO2 Flux</td>
      <td>uatm</td>
      <td>1002.84</td>
      <td>0</td>
      <td>6</td>
    </tr>
    <tr>
      <th>7</th>
      <td>20050830</td>
      <td>CO2 Flux</td>
      <td>uatm</td>
      <td>1059.61</td>
      <td>0</td>
      <td>7</td>
    </tr>
    <tr>
      <th>8</th>
      <td>20050830</td>
      <td>CO2 Flux</td>
      <td>uatm</td>
      <td>1097.45</td>
      <td>0</td>
      <td>8</td>
    </tr>
    <tr>
      <th>9</th>
      <td>20040701</td>
      <td>CO2 Flux</td>
      <td>uatm</td>
      <td>1381.28</td>
      <td>63</td>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>




```python
# cast all the datetime column to datetime type 
# Dirty data so we can't apply date_time to incorrect str formats
# samples.apply(lambda row:pd.to_datetime(row["DateTime"]), axis=1)
```

## Set up our DB Connection

Read DB configuration and use to connect to database. Initialize cursor in the DB.


```python
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.json")) as f:
    db_conn_dict = json.load(f)
    
conn = psycopg2.connect(**db_conn_dict)
cur = conn.cursor()

```

Create string template of SQL procedure to load the sitelocations into the database


```python
insert_locations_string = """
    INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
    values ({0}, LEFT('{1}', 150), {2}, {3}, cast(coalesce(nullif('{4}', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('{5}'), 4326))
"""
```


```python
co2_data_locations_clean[["location_id", "Site Type", "Latitude", "Longitude", "Altitude", "geometry"]].head(3)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>location_id</th>
      <th>Site Type</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Altitude</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>small stream</td>
      <td>-10.066</td>
      <td>-67.606</td>
      <td>150.0</td>
      <td>POINT (-67.60599999999999 -10.066)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>small stream</td>
      <td>-9.751</td>
      <td>-67.672</td>
      <td>150.0</td>
      <td>POINT (-67.672 -9.750999999999999)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>small river</td>
      <td>-9.016</td>
      <td>-68.584</td>
      <td>150.0</td>
      <td>POINT (-68.584 -9.016)</td>
    </tr>
  </tbody>
</table>
</div>



Iterate through the dataframe to load all the points into the DB finally!!!


```python
for index, row in co2_data_locations_clean[["location_id", "Site Type", "Latitude", "Longitude", "Altitude", "geometry"]].iterrows():

        print(insert_locations_string.format(row["location_id"], str(row["Site Type"]), float(row["Latitude"]), float(row["Longitude"]), float(row["Altitude"]), row["geometry"]))
        cur.execute(insert_locations_string.format(row["location_id"], str(row["Site Type"]), float(row["Latitude"]), float(row["Longitude"]), float(row["Altitude"]), row["geometry"]))
        conn.commit()
```

    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (0, LEFT('small stream', 150), -10.066, -67.606, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-67.60599999999999 -10.066)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1, LEFT('small stream', 150), -9.751, -67.672, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-67.672 -9.750999999999999)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (2, LEFT('small river', 150), -9.016, -68.584, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-68.584 -9.016)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (3, LEFT('small river', 150), -9.029, -68.593, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-68.593 -9.029)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (4, LEFT('large river', 150), -3.063, -60.272, cast(coalesce(nullif('70.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.272 -3.063)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (5, LEFT('large lake/river', 150), -2.289, -54.824, cast(coalesce(nullif('60.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.824 -2.289)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (6, LEFT('large river', 150), -2.454, -54.482, cast(coalesce(nullif('60.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.482 -2.454)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (7, LEFT('large river', 150), -3.058, -60.288, cast(coalesce(nullif('70.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.288 -3.058)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (8, LEFT('large lake/river', 150), -2.418, -54.875, cast(coalesce(nullif('60.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.875 -2.418)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (9, LEFT('large river', 150), -2.462, -54.63, cast(coalesce(nullif('60.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.63 -2.462)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (10, LEFT('small stream', 150), -2.93, -59.974, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-59.974 -2.93)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (11, LEFT('large river', 150), -3.253, -60.012, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.012 -3.253)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (12, LEFT('main river channel between santarem and alter do chao', 150), -2.376, -54.849, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.849 -2.376)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (13, LEFT('lake', 150), -2.506, -54.963, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.963 -2.506)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (14, LEFT('mainstem amazonas', 150), -2.454, -54.482, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.482 -2.454)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (15, LEFT('mainstem river amazonas', 150), -2.461, -54.57, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.57 -2.461)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (16, LEFT('mainstem amazonas river', 150), -2.461, -54.57, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.57 -2.461)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (17, LEFT('minor river channel of mainstem', 150), -2.314, -54.596, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.596 -2.314)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (18, LEFT('huge lake w/o trees; very windy', 150), -2.3, -54.664, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.664 -2.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (19, LEFT('river, approximately 600 m from alter do chao and water shallower (4-5 m); perhaps slower here', 150), -2.489, -55.014, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.014 -2.489)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (20, LEFT('mainstem amazonas river', 150), -2.088, -55.343, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.343 -2.088)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (21, LEFT('bay, river', 150), -1.788, -51.417, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-51.417 -1.788)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (22, LEFT('30-40 m width river; with influence of the bay (near site RCu-2)', 150), -1.729, -51.456, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-51.456 -1.729)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (23, LEFT('igarape - 3-4 m width river (near site RCu-1)', 150), -1.707, -51.474, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-51.474 -1.707)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (24, LEFT('medium river', 150), -1.778, -51.471, cast(coalesce(nullif('150.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-51.471 -1.778)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (25, LEFT('main river channel of Negro; river all in one channel (not anastomosed); wide', 150), -1.196, -61.289, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.289 -1.196)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (26, LEFT('igarape river - very black water; wide (8-10 m); no clear bdry - flooded veg; dominated by a small palm tree', 150), -0.694, -63.203, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-63.203 -0.694)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (27, LEFT('igarape river - very black water', 150), -0.398, -63.315, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-63.315 -0.398)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (28, LEFT('igarape river - very black water', 150), -0.39, -64.6, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-64.59999999999999 -0.39)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (29, LEFT('at least 300-400 m wide river; right/left means 10-20 m off shore; center = where water flows fastest', 150), -0.42, -64.604, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-64.604 -0.42)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (30, LEFT('at least 300-400 m wide river; right/left means 10-20 m off shore; center = where water flows fastest', 150), -0.437, -64.607, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-64.607 -0.437)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (31, LEFT('at least 300-400 m wide river; right/left means 10-20 m off shore; center = where water flows fastest', 150), -0.473, -64.62, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-64.62 -0.473)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (32, LEFT('at least 300-400 m wide river; right/left means 10-20 m off shore; center = where water flows fastest', 150), -0.402, -65.211, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-65.211 -0.402)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (33, LEFT('at least 300-400 m wide river; right/left means 10-20 m off shore; center = where water flows fastest', 150), -0.405, -65.227, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-65.227 -0.405)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (34, LEFT('at least 300-400 m wide river; right/left means 10-20 m off shore; center = where water flows fastest', 150), -0.42, -65.232, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-65.232 -0.42)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (35, LEFT('igarape river- very black water', 150), -0.366, -66.569, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-66.569 -0.366)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (36, LEFT('at least 300-400 m wide river; right/left means 10-20 m off shore; center = where water flows fastest', 150), -0.361, -66.563, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-66.563 -0.361)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (37, LEFT('at least 300-400 m wide river; right/left means 10-20 m off shore; center = where water flows fastest', 150), -0.356, -66.566, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-66.566 -0.356)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (38, LEFT('at least 300-400 m wide river; right/left means 10-20 m off shore; center = where water flows fastest', 150), -0.34, -66.569, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-66.569 -0.34)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (39, LEFT('river, Sao Gabriel Cachoeira - only place where could see upwelling of water; downstream from rapids/waterfalls; some rocky outcrops in water where sampling', 150), -0.144, -67.079, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-67.07899999999999 -0.144)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (40, LEFT('at least 300-400 m wide river; right/left means 10-20 m off shore; center = where water flows fastest', 150), -0.142, -67.064, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-67.06399999999999 -0.142)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (41, LEFT('igarape river- very black water', 150), -0.434, -67.06, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-67.06 -0.434)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (42, LEFT('clearwater river; lots of phytoplankton; nothing notable about flow', 150), -1.261, -61.836, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.836 -1.261)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (43, LEFT('river, vegetation like Campinarana (very wet - flooded; not closed canopy); landscape mosaic of <1 km lakes - in one of them', 150), -1.417, -61.577, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.577 -1.417)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (44, LEFT('large blackwater tributary to Negro river- approximately 200-300 m wide', 150), -1.64, -61.58, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.58 -1.64)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (45, LEFT('mainstem of Negro river near confluence with Solimoes', 150), -3.056, -60.293, cast(coalesce(nullif('17.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.293 -3.056)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (46, LEFT('river, sampling in channel on one side of large island (channel width approximately 500 m wide)', 150), -3.748, -61.442, cast(coalesce(nullif('25.5', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.442 -3.748)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (47, LEFT('river, sampling in channel on one side of large island (channel width approximately 500 m wide)', 150), -3.797, -61.423, cast(coalesce(nullif('18.8', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.423 -3.797)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (48, LEFT('igarape/small stream', 150), -2.93, -59.974, cast(coalesce(nullif('53.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-59.974 -2.93)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (49, LEFT('approximately 1 km across river; 10-20 m offshore', 150), -3.405, -58.771, cast(coalesce(nullif('13.2', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.771 -3.405)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (50, LEFT('approximately 1 km across river', 150), -3.472, -58.778, cast(coalesce(nullif('16.6', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.778 -3.472)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (51, LEFT('mainstem of Solimoes river; upstream of confluence with Negro', 150), -3.285, -60.041, cast(coalesce(nullif('17.8', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.041 -3.285)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (52, LEFT('medium river', 150), -2.688, -60.324, cast(coalesce(nullif('17.8', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.324 -2.688)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (53, LEFT('medium river', 150), -2.688, -60.324, cast(coalesce(nullif('18.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.324 -2.688)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (54, LEFT('small river/large stream', 150), -2.728, -60.453, cast(coalesce(nullif('18.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.453 -2.728)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (55, LEFT('medium river', 150), -2.812, -60.474, cast(coalesce(nullif('20.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.474 -2.812)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (56, LEFT('small river; dry season; 200-300 m at most; very smoky', 150), -7.682, -72.66, cast(coalesce(nullif('170.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-72.66 -7.682)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (57, LEFT('river, somewhat toward blackwater; approximately 50-100 m wide', 150), -7.652, -72.7, cast(coalesce(nullif('166.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-72.7 -7.652)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (58, LEFT('100-200 m wide river; whitewater', 150), -8.17, -70.391, cast(coalesce(nullif('173.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-70.39100000000001 -8.17)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (59, LEFT('100-200 m wide river; whitewater', 150), -8.175, -70.773, cast(coalesce(nullif('160.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-70.773 -8.175000000000001)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (60, LEFT('igarape river - 1-2 m wide; higher cation exchange capacity soil; pH near 6', 150), -9.751, -67.672, cast(coalesce(nullif('173.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-67.672 -9.750999999999999)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (61, LEFT('igarape - 1-2 m wide; higher cation exchange capacity soil; pH near 6', 150), -9.751, -67.672, cast(coalesce(nullif('173.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-67.672 -9.750999999999999)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (62, LEFT('150-250 m river channel width; whitewater; pH 6.8-8.6', 150), -8.999, -68.596, cast(coalesce(nullif('125.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-68.596 -8.999000000000001)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (63, LEFT('igarape river - 1-2 m wide; low cation exchange capacity soil; more acidic than Humaita (pH avg 5-5.x)', 150), -10.066, -67.606, cast(coalesce(nullif('193.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-67.60599999999999 -10.066)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (64, LEFT('100-200 m wide river; whitewater; maybe a little smaller', 150), -10.011, -67.843, cast(coalesce(nullif('129.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-67.843 -10.011)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (65, LEFT('2 km upstream from PVH; single river channel; low water (drought!); close to rocks but before rapids; channel width approximately 500 m', 150), -8.801, -63.95, cast(coalesce(nullif('50.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-63.95 -8.801)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (66, LEFT('rivers less than 100 m wide', 150), -11.398, -61.445, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.445 -11.398)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (67, LEFT('rivers less than 100 m wide', 150), -11.507, -61.356, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.356 -11.507)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (68, LEFT('rivers less than 100 m wide', 150), -11.073, -61.922, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.922 -11.073)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (69, LEFT('rivers less than 100 m wide', 150), -11.133, -61.901, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.901 -11.133)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (70, LEFT('rivers less than 100 m wide', 150), -11.727, -61.645, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.645 -11.727)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (71, LEFT('rivers less than 100 m wide', 150), -11.727, -61.545, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.545 -11.727)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (72, LEFT('rivers less than 100 m wide', 150), -11.76, -61.778, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.778 -11.76)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (73, LEFT('rivers less than 100 m wide', 150), -10.813, -62.119, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.119 -10.813)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (74, LEFT('rivers less than 100 m wide', 150), -10.75, -62.17, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.17 -10.75)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (75, LEFT('rivers less than 100 m wide', 150), -10.954, -62.256, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.256 -10.954)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (76, LEFT('rivers less than 100 m wide', 150), -10.969, -62.269, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.269 -10.969)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (77, LEFT('rivers less than 100 m wide', 150), -10.952, -62.262, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.262 -10.952)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (78, LEFT('rivers less than 100 m wide', 150), -10.024, -61.821, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.821 -10.024)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (79, LEFT('rivers less than 100 m wide', 150), -11.081, -61.819, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.819 -11.081)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (80, LEFT('rivers less than 100 m wide', 150), -11.082, -61.746, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.746 -11.082)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (81, LEFT('rivers less than 100 m wide', 150), -11.082, -61.715, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.715 -11.082)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (82, LEFT('rivers less than 100 m wide', 150), -11.083, -61.691, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.691 -11.083)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (83, LEFT('rivers less than 100 m wide', 150), -11.084, -61.663, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-61.663 -11.084)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (84, LEFT('rivers less than 100 m wide', 150), -10.63, -62.565, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.565 -10.63)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (85, LEFT('rivers less than 100 m wide', 150), -10.455, -62.386, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.386 -10.455)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (86, LEFT('rivers less than 100 m wide', 150), -10.811, -62.427, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.427 -10.811)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (87, LEFT('rivers less than 100 m wide', 150), -11.031, -62.681, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.681 -11.031)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (88, LEFT('rivers less than 100 m wide', 150), -11.096, -62.737, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.737 -11.096)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (89, LEFT('rivers less than 100 m wide', 150), -11.161, -62.793, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.793 -11.161)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (90, LEFT('rivers less than 100 m wide', 150), -11.244, -62.208, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.208 -11.244)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (91, LEFT('rivers less than 100 m wide', 150), -11.292, -62.233, cast(coalesce(nullif('180.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-62.233 -11.292)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (92, LEFT('reservoir', 150), 49.3, -122.4, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-122.4 49.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (93, LEFT('reservoir', 150), 59.6, -118.2, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-118.2 59.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (94, LEFT('reservoir', 150), 49.4, -123.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-123.3 49.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (95, LEFT('reservoir', 150), 50.3, -117.9, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-117.9 50.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (96, LEFT('reservoir', 150), -1.9, -59.5, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-59.5 -1.9)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (97, LEFT('reservoir', 150), -22.5, -48.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-48.6 -22.5)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (98, LEFT('reservoir', 150), 46.7, -75.8, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-75.8 46.7)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (99, LEFT('reservoir', 150), 49.7, -70.2, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-70.2 49.7)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (100, LEFT('reservoir', 150), 46.4, 10.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (10 46.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (101, LEFT('reservoir', 150), 54.7, -70.4, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-70.40000000000001 54.7)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (102, LEFT('reservoir', 150), 49.4, -122.9, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-122.9 49.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (103, LEFT('reservoir', 150), 47.5, -76.7, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-76.7 47.5)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (104, LEFT('reservoir', 150), 46.6, -75.8, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-75.8 46.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (105, LEFT('reservoir', 150), 50.08333, -56.71, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-56.71 50.08333)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (106, LEFT('reservoir', 150), 46.2, -91.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-91 46.2)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (107, LEFT('reservoir', 150), -18.0, -48.5, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-48.5 -18)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (108, LEFT('reservoir', 150), -2.8, -54.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.3 -2.8)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (109, LEFT('reservoir', 150), 46.2, -90.9, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-90.90000000000001 46.2)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (110, LEFT('reservoir', 150), 39.6, -106.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.1 39.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (111, LEFT('reservoir', 150), 46.1, 7.4, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (7.4 46.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (112, LEFT('reservoir', 150), 54.4, -126.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-126 54.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (113, LEFT('reservoir', 150), 46.6, -116.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-116.3 46.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (114, LEFT('reservoir', 150), 52.8, -76.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-76.59999999999999 52.8)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (115, LEFT('reservoir', 150), 53.5, -77.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-77.09999999999999 53.5)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (116, LEFT('reservoir', 150), 47.9, -118.8, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-118.8 47.9)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (117, LEFT('reservoir', 150), -22.5, -44.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-44.6 -22.5)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (118, LEFT('reservoir', 150), -20.7, -46.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-46.3 -20.7)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (119, LEFT('reservoir', 150), 9.2, -82.2, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-82.2 9.199999999999999)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (120, LEFT('reservoir', 150), 9.2, -79.9, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-79.90000000000001 9.199999999999999)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (121, LEFT('reservoir', 150), 48.9, -75.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-75 48.9)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (122, LEFT('reservoir', 150), 50.5, -90.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-90 50.5)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (123, LEFT('reservoir', 150), 46.6, 8.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (8.300000000000001 46.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (124, LEFT('reservoir', 150), 46.7, 7.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (7.1 46.7)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (125, LEFT('reservoir', 150), 49.7, -57.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-57.1 49.7)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (126, LEFT('reservoir', 150), 62.6, 17.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.1 62.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (127, LEFT('reservoir', 150), -25.4, -54.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.6 -25.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (128, LEFT('reservoir', 150), -18.4, -49.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-49.1 -18.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (129, LEFT('reservoir', 150), 49.4, -122.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-122 49.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (130, LEFT('reservoir', 150), 49.4, -116.8, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-116.8 49.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (131, LEFT('reservoir', 150), -20.2, -47.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-47.3 -20.2)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (132, LEFT('reservoir', 150), 54.5, -78.5, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-78.5 54.5)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (133, LEFT('reservoir', 150), 53.8, -76.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-76 53.8)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (134, LEFT('reservoir', 150), 54.2, -76.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-76.09999999999999 54.2)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (135, LEFT('reservoir', 150), 53.6, -73.2, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-73.2 53.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (136, LEFT('reservoir', 150), 50.3, -96.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-96 50.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (137, LEFT('reservoir', 150), 50.1, -70.5, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-70.5 50.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (138, LEFT('reservoir', 150), 54.2, -72.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-72.59999999999999 54.2)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (139, LEFT('reservoir', 150), 55.0, -70.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-70.3 55)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (140, LEFT('reservoir', 150), 62.5, 14.5, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (14.5 62.5)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (141, LEFT('reservoir', 150), 62.1, 15.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.1 62.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (142, LEFT('reservoir', 150), 67.8, 27.7, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.7 67.8)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (143, LEFT('reservoir', 150), 65.8, 21.2, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.2 65.8)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (144, LEFT('reservoir', 150), 46.8, 9.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (9 46.8)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (145, LEFT('reservoir', 150), 46.6, 9.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (9.1 46.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (146, LEFT('reservoir', 150), 48.4, -56.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-56.6 48.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (147, LEFT('reservoir', 150), 49.4, -68.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-68.59999999999999 49.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (148, LEFT('reservoir', 150), 49.8, -69.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-69 49.8)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (149, LEFT('reservoir', 150), 50.2, -69.2, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-69.2 50.2)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (150, LEFT('reservoir', 150), 51.3, -68.8, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-68.8 51.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (151, LEFT('reservoir', 150), -14.9, -55.8, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.8 -14.9)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (152, LEFT('reservoir', 150), 48.3, -57.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-57.6 48.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (153, LEFT('reservoir', 150), 46.0, -91.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-91.09999999999999 46)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (154, LEFT('reservoir', 150), 46.1, -91.5, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-91.5 46.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (155, LEFT('reservoir', 150), 38.0, -120.5, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-120.5 38)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (156, LEFT('reservoir', 150), 39.6, -121.4, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-121.4 39.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (157, LEFT('reservoir', 150), 45.9, -74.7, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-74.7 45.9)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (158, LEFT('reservoir', 150), 50.0, -68.5, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-68.5 50)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (159, LEFT('reservoir', 150), 50.3, -69.2, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-69.2 50.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (160, LEFT('reservoir', 150), 49.3, -72.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-72 49.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (161, LEFT('reservoir', 150), 5.1, -53.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-53 5.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (162, LEFT('reservoir', 150), 50.6, -96.2, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-96.2 50.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (163, LEFT('reservoir', 150), 50.3, -95.5, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-95.5 50.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (164, LEFT('reservoir', 150), 68.0, 26.8, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.8 68)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (165, LEFT('reservoir', 150), 49.3, -57.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-57.1 49.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (166, LEFT('reservoir', 150), 51.0, -118.2, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-118.2 51)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (167, LEFT('reservoir', 150), -22.7, -43.9, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-43.9 -22.7)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (168, LEFT('reservoir', 150), 53.7, -77.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-77 53.7)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (169, LEFT('reservoir', 150), 51.0, -59.9, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-59.9 51)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (170, LEFT('reservoir', 150), 50.5, -67.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-67.09999999999999 50.5)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (171, LEFT('reservoir', 150), 51.7, -67.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-67 51.7)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (172, LEFT('reservoir', 150), -8.8, -63.4, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-63.4 -8.800000000000001)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (173, LEFT('reservoir', 150), 49.4, -57.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-57.1 49.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (174, LEFT('reservoir', 150), 46.6, 8.8, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (8.800000000000001 46.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (175, LEFT('reservoir', 150), -13.9, -48.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-48.3 -13.9)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (176, LEFT('reservoir', 150), 56.0, -120.4, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-120.4 56)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (177, LEFT('reservoir', 150), 50.1, -96.0, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-96 50.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (178, LEFT('reservoir', 150), 40.9, -122.4, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-122.4 40.9)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (179, LEFT('reservoir', 150), 47.1, 8.8, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (8.800000000000001 47.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (180, LEFT('reservoir', 150), 64.5, 20.7, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.7 64.5)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (181, LEFT('reservoir', 150), 64.0, 18.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.3 64)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (182, LEFT('reservoir', 150), 50.2, -95.4, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-95.40000000000001 50.2)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (183, LEFT('reservoir', 150), 49.3, -122.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-122.3 49.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (184, LEFT('reservoir', 150), 50.1, -68.4, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-68.40000000000001 50.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (185, LEFT('reservoir', 150), -18.2, -45.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-45.3 -18.2)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (186, LEFT('reservoir', 150), -20.4, -45.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-45.3 -20.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (187, LEFT('reservoir', 150), -3.9, -49.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-49.6 -3.9)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (188, LEFT('reservoir', 150), 63.8, 20.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.1 63.8)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (189, LEFT('reservoir', 150), 48.3, -56.5, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-56.5 48.3)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (190, LEFT('reservoir', 150), 48.6, -56.5, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-56.5 48.6)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (191, LEFT('reservoir', 150), 45.9, -119.2, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-119.2 45.9)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (192, LEFT('reservoir', 150), 49.1, -117.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-117.6 49.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (193, LEFT('reservoir', 150), 49.1, -116.1, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-116.1 49.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (194, LEFT('reservoir', 150), 56.2, -124.2, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-124.2 56.2)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (195, LEFT('reservoir', 150), 55.8, -123.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-123.6 55.8)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (196, LEFT('reservoir', 150), 56.1, -123.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-123.3 56.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (197, LEFT('reservoir', 150), 50.0, 7.3, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (7.3 50)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (198, LEFT('reservoir', 150), 46.4, 7.43333, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (7.43333 46.4)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (199, LEFT('lake', 150), -2.0484, 29.28603, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.28603 -2.0484)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (200, LEFT('lake', 150), -2.01706, 29.28339, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.28339 -2.01706)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (201, LEFT('lake', 150), -2.34024, 28.97672, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.97672 -2.34024)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (202, LEFT('lake', 150), -2.26949, 28.98427, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.98427 -2.26949)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (203, LEFT('lake', 150), -2.15708, 28.96258, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.96258 -2.15708)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (204, LEFT('lake', 150), -2.02447, 28.98786, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.98786 -2.02447)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (205, LEFT('lake', 150), -1.89855, 29.02995, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.02995 -1.89855)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (206, LEFT('lake', 150), -1.77587, 29.07218, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.07218 -1.77587)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (207, LEFT('lake', 150), -1.66165, 29.11592, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.11592 -1.66165)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (208, LEFT('lake', 150), -1.62, 29.04957, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.04957 -1.62)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (209, LEFT('lake', 150), -1.82458, 29.16453, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.16453 -1.82458)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (210, LEFT('lake', 150), -1.98638, 29.21653, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.21653 -1.98638)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (211, LEFT('lake', 150), -2.1072, 29.19296, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.19296 -2.1072)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (212, LEFT('lake', 150), -2.19067, 29.13648, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.13648 -2.19067)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (213, LEFT('lake', 150), -2.28522, 29.06318, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.06318 -2.28522)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (214, LEFT('lake', 150), -2.45232, 28.85508, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.85508 -2.45232)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (215, LEFT('lake', 150), -1.986, 29.21754, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.21754 -1.986)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (216, LEFT('lake', 150), -1.82665, 29.16366, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.16366 -1.82665)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (217, LEFT('lake', 150), -1.62165, 29.05015, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.05015 -1.62165)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (218, LEFT('lake', 150), -1.66293, 29.11517, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.11517 -1.66293)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (219, LEFT('lake', 150), -1.77663, 29.07236, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.07236 -1.77663)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (220, LEFT('lake', 150), -1.89995, 29.02737, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.02737 -1.89995)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (221, LEFT('lake', 150), -2.02628, 28.98716, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.98716 -2.02628)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (222, LEFT('lake', 150), -2.15668, 28.9613, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.9613 -2.15668)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (223, LEFT('lake', 150), -2.10969, 29.19157, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.19157 -2.10969)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (224, LEFT('lake', 150), -2.28516, 29.06324, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.06324 -2.28516)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (225, LEFT('lake', 150), -2.27515, 28.98867, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.98867 -2.27515)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (226, LEFT('lake', 150), -2.33841, 28.97638, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.97638 -2.33841)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (227, LEFT('lake', 150), -2.1906, 29.13592, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.13592 -2.1906)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (228, LEFT('lake', 150), -2.45281, 28.85536, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.85536 -2.45281)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (229, LEFT('lake', 150), -2.0474, 29.2864, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.2864 -2.0474)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (230, LEFT('lake', 150), -2.04628, 29.28771, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.28771 -2.04628)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (231, LEFT('lake', 150), -2.26987, 28.98767, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.98767 -2.26987)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (232, LEFT('lake', 150), -2.15595, 28.96165, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.96165 -2.15595)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (233, LEFT('lake', 150), -2.02266, 28.98914, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.98914 -2.02266)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (234, LEFT('lake', 150), -1.8997, 29.02858, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.02858 -1.8997)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (235, LEFT('lake', 150), -1.77547, 29.07288, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.07288 -1.77547)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (236, LEFT('lake', 150), -1.621, 29.05016, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.05016 -1.621)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (237, LEFT('lake', 150), -1.66344, 29.11607, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.11607 -1.66344)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (238, LEFT('lake', 150), -1.98625, 29.21717, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.21717 -1.98625)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (239, LEFT('lake', 150), -2.10765, 29.19188, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.19188 -2.10765)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (240, LEFT('lake', 150), -2.19157, 29.13655, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.13655 -2.19157)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (241, LEFT('lake', 150), -2.28597, 29.06193, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.06193 -2.28597)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (242, LEFT('lake', 150), -2.337, 28.97625, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.97625 -2.337)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (243, LEFT('lake', 150), -2.45295, 28.85455, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.85455 -2.45295)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (244, LEFT('lake', 150), -2.32522, 28.98028, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.98028 -2.32522)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (245, LEFT('lake', 150), -2.4501, 28.85644, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.85644 -2.4501)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (246, LEFT('lake', 150), -2.2749, 28.98892, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.98892 -2.2749)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (247, LEFT('lake', 150), -2.15633, 28.96137, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.96137 -2.15633)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (248, LEFT('lake', 150), -2.02548, 28.98626, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.98626 -2.02548)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (249, LEFT('lake', 150), -1.90019, 29.02915, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.02915 -1.90019)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (250, LEFT('lake', 150), -1.77536, 29.07214, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.07214 -1.77536)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (251, LEFT('lake', 150), -1.66301, 29.11631, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.11631 -1.66301)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (252, LEFT('lake', 150), -1.62087, 29.04961, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.04961 -1.62087)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (253, LEFT('lake', 150), -1.8235, 29.16261, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.16261 -1.8235)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (254, LEFT('lake', 150), -1.98671, 29.21716, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.21716 -1.98671)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (255, LEFT('lake', 150), -2.11002, 29.19194, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.19194 -2.11002)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (256, LEFT('lake', 150), -2.19096, 29.1365, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.1365 -2.19096)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (257, LEFT('lake', 150), -2.28486, 29.06255, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.06255 -2.28486)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (258, LEFT('lake', 150), -2.0487, 29.28611, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.28611 -2.0487)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (259, LEFT('lake', 150), -2.33952, 28.97633, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.97633 -2.33952)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (260, LEFT('lake', 150), -1.72504, 29.23745, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.23745 -1.72504)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (261, LEFT('river', 150), -2.08139, 29.37524, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.37524 -2.08139)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (262, LEFT('river', 150), -2.06672, 29.41089, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.41089 -2.06672)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (263, LEFT('river', 150), -2.03078, 29.39893, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.39893 -2.03078)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (264, LEFT('river', 150), -1.99127, 29.35508, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.35508 -1.99127)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (265, LEFT('river', 150), -2.11789, 29.3307, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.3307 -2.11789)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (266, LEFT('river', 150), -2.13102, 29.32533, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.32533 -2.13102)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (267, LEFT('river', 150), -2.16663, 29.29639, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.29639 -2.16663)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (268, LEFT('river', 150), -2.36229, 28.79562, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.79562 -2.36229)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (269, LEFT('river', 150), -2.38485, 28.78838, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.78838 -2.38485)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (270, LEFT('river', 150), -2.41381, 28.83433, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.83433 -2.41381)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (271, LEFT('river', 150), -2.43526, 28.8319, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.8319 -2.43526)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (272, LEFT('river', 150), -2.46981, 28.83672, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.83672 -2.46981)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (273, LEFT('river', 150), -2.362, 28.79569, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.79569 -2.362)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (274, LEFT('river', 150), -2.38485, 28.78844, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.78844 -2.38485)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (275, LEFT('river', 150), -2.41374, 28.83492, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.83492 -2.41374)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (276, LEFT('river', 150), -2.43273, 28.83449, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.83449 -2.43273)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (277, LEFT('river', 150), -2.47075, 28.83676, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.83676 -2.47075)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (278, LEFT('river', 150), -2.50511, 28.887, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.887 -2.50511)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (279, LEFT('river', 150), -2.08131, 29.37515, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.37515 -2.08131)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (280, LEFT('river', 150), -2.06677, 29.41117, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.41117 -2.06677)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (281, LEFT('river', 150), -2.03079, 29.399, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.399 -2.03079)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (282, LEFT('river', 150), -1.99169, 29.35693, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.35693 -1.99169)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (283, LEFT('river', 150), -2.1178, 29.3307, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.3307 -2.1178)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (284, LEFT('river', 150), -2.13098, 29.32534, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.32534 -2.13098)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (285, LEFT('river', 150), -2.16661, 29.29638, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.29638 -2.16661)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (286, LEFT('river', 150), -1.99193, 29.35685, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.35685 -1.99193)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (287, LEFT('river', 150), -2.03074, 29.39904, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.39904 -2.03074)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (288, LEFT('river', 150), -2.06695, 29.41148, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.41148 -2.06695)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (289, LEFT('river', 150), -2.11788, 29.33061, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.33061 -2.11788)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (290, LEFT('river', 150), -2.13154, 29.32513, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.32513 -2.13154)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (291, LEFT('river', 150), -2.16647, 29.29643, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.29643 -2.16647)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (292, LEFT('river', 150), -2.36234, 28.79552, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.79552 -2.36234)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (293, LEFT('river', 150), -2.38494, 28.78823, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.78823 -2.38494)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (294, LEFT('river', 150), -2.41409, 28.83485, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.83485 -2.41409)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (295, LEFT('river', 150), -2.43548, 28.83196, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.83196 -2.43548)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (296, LEFT('river', 150), -2.47008, 28.8369, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.8369 -2.47008)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (297, LEFT('river', 150), -2.50515, 28.8871, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.8871 -2.50515)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (298, LEFT('river', 150), -2.36236, 28.79547, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.79547 -2.36236)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (299, LEFT('river', 150), -2.38483, 28.78836, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.78836 -2.38483)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (300, LEFT('river', 150), -2.41389, 28.83471, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.83471 -2.41389)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (301, LEFT('river', 150), -2.41321, 28.8345, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.8345 -2.41321)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (302, LEFT('river', 150), -2.4702, 28.8366, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.8366 -2.4702)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (303, LEFT('river', 150), -2.50519, 28.88693, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.88693 -2.50519)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (304, LEFT('river', 150), -1.99064, 29.35685, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.35685 -1.99064)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (305, LEFT('river', 150), -2.0308, 29.39891, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.39891 -2.0308)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (306, LEFT('river', 150), -2.06685, 29.41125, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.41125 -2.06685)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (307, LEFT('river', 150), -2.11785, 29.3305, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.3305 -2.11785)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (308, LEFT('river', 150), 0.50577, 25.18699, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.18699 0.5057700000000001)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (309, LEFT('river', 150), 0.56267, 25.11986, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.11986 0.56267)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (310, LEFT('river', 150), 0.56807, 25.11718, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.11718 0.56807)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (311, LEFT('river', 150), 0.58211, 24.76085, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.76085 0.58211)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (312, LEFT('river', 150), 0.74571, 24.39691, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.39691 0.74571)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (313, LEFT('river', 150), 0.773, 24.27061, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.27061 0.773)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (314, LEFT('river', 150), 1.00566, 24.05911, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.05911 1.00566)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (315, LEFT('river', 150), 1.13995, 23.6502, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.6502 1.13995)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (316, LEFT('river', 150), 1.23217, 23.61593, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.61593 1.23217)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (317, LEFT('river', 150), 1.34218, 23.42641, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.42641 1.34218)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (318, LEFT('river', 150), 1.47807, 23.37913, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.37913 1.47807)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (319, LEFT('river', 150), 1.51654, 23.34539, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.34539 1.51654)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (320, LEFT('river', 150), 1.79804, 23.08739, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.08739 1.79804)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (321, LEFT('river', 150), 1.9939, 22.71825, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.71825 1.9939)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (322, LEFT('river', 150), 2.06356, 22.69775, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.69775 2.06356)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (323, LEFT('river', 150), 2.20585, 22.332, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.332 2.20585)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (324, LEFT('river', 150), 2.19821, 22.29619, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.29619 2.19821)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (325, LEFT('river', 150), 2.18563, 21.9008, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.9008 2.18563)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (326, LEFT('river', 150), 2.10547, 21.66455, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.66455 2.10547)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (327, LEFT('river', 150), 2.07789, 21.52044, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.52044 2.07789)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (328, LEFT('river', 150), 2.10085, 21.45398, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.45398 2.10085)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (329, LEFT('river', 150), 2.04344, 21.06155, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.06155 2.04344)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (330, LEFT('river', 150), 2.05091, 21.02265, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.02265 2.05091)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (331, LEFT('river', 150), 2.01699, 20.66444, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.66444 2.01699)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (332, LEFT('river', 150), 2.03023, 20.50076, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.50076 2.03023)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (333, LEFT('river', 150), 1.96535, 20.19742, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.19742 1.96535)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (334, LEFT('river', 150), 1.96957, 20.06373, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.06373 1.96957)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (335, LEFT('river', 150), 1.9103, 19.81723, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.81723 1.9103)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (336, LEFT('river', 150), 1.8546, 19.78305, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.78305 1.8546)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (337, LEFT('river', 150), 1.75099, 19.3594, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.3594 1.75099)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (338, LEFT('river', 150), 1.63675, 19.15969, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.15969 1.63675)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (339, LEFT('river', 150), 1.4898, 18.99207, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.99207 1.4898)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (340, LEFT('river', 150), 1.26153, 18.79267, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.79267 1.26153)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (341, LEFT('river', 150), 1.25127, 18.75011, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.75011 1.25127)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (342, LEFT('river', 150), 1.15953, 18.65123, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.65123 1.15953)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (343, LEFT('river', 150), 1.12503, 18.61036, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.61036 1.12503)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (344, LEFT('river', 150), 1.12826, 18.62077, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.62077 1.12826)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (345, LEFT('river', 150), 1.1284, 18.62576, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.62576 1.1284)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (346, LEFT('river', 150), 1.03281, 18.5287, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.5287 1.03281)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (347, LEFT('river', 150), 0.85421, 18.38732, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.38732 0.85421)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (348, LEFT('river', 150), 0.68418, 18.40149, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.40149 0.68418)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (349, LEFT('river', 150), 0.46323, 18.33142, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.33142 0.46323)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (350, LEFT('river', 150), 0.10889, 18.28058, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.28058 0.10889)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (351, LEFT('river', 150), 0.11243, 18.28072, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.28072 0.11243)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (352, LEFT('river', 150), 0.07078, 18.31695, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.31695 0.07078)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (353, LEFT('river', 150), -0.05497, 18.37942, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.37942 -0.05497)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (354, LEFT('river', 150), 0.04347, 18.22524, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.22524 0.04347)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (355, LEFT('river', 150), -0.29826, 17.96509, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.96509 -0.29826)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (356, LEFT('river', 150), -0.4897, 17.7022, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.7022 -0.4897)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (357, LEFT('river', 150), -0.61219, 17.66333, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.66333 -0.61219)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (358, LEFT('river', 150), -0.6007, 17.8052, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.8052 -0.6007)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (359, LEFT('river', 150), -0.89893, 17.39705, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.39705 -0.89893)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (360, LEFT('river', 150), -0.93356, 17.41706, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.41706 -0.9335599999999999)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (361, LEFT('river', 150), -1.13281, 16.99073, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.99073 -1.13281)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (362, LEFT('river', 150), -1.22286, 16.82016, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.82016 -1.22286)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (363, LEFT('river', 150), -1.42362, 16.70159, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.70159 -1.42362)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (364, LEFT('river', 150), -1.72012, 16.66458, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.66458 -1.72012)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (365, LEFT('river', 150), -1.88172, 16.56923, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.56923 -1.88172)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (366, LEFT('river', 150), -1.86932, 16.50047, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.50047 -1.86932)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (367, LEFT('river', 150), -2.12683, 16.30374, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.30374 -2.12683)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (368, LEFT('river', 150), -2.13287, 16.20167, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.20167 -2.13287)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (369, LEFT('river', 150), -2.57983, 16.22316, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.22316 -2.57983)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (370, LEFT('river', 150), -2.85295, 16.19966, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.19966 -2.85295)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (371, LEFT('river', 150), -2.94128, 16.15635, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.15635 -2.94128)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (372, LEFT('river', 150), -3.01573, 16.18627, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.18627 -3.01573)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (373, LEFT('river', 150), -3.17771, 16.19681, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.19681 -3.17771)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (374, LEFT('river', 150), -3.30154, 16.23543, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.23543 -3.30154)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (375, LEFT('river', 150), -3.42917, 16.15668, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.15668 -3.42917)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (376, LEFT('river', 150), -3.5627, 16.09921, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.09921 -3.5627)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (377, LEFT('river', 150), -3.81736, 15.9486, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.9486 -3.81736)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (378, LEFT('river', 150), -3.94913, 15.9083, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.9083 -3.94913)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (379, LEFT('river', 150), -4.01882, 15.61529, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.61529 -4.01882)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (380, LEFT('river', 150), -4.19277, 15.52579, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.52579 -4.19277)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (381, LEFT('river', 150), -4.24639, 15.55122, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.55122 -4.24639)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (382, LEFT('river', 150), -4.30655, 15.3504, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.3504 -4.30655)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (383, LEFT('river', 150), 0.50522, 25.18681, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.18681 0.50522)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (384, LEFT('river', 150), 0.5617, 25.12465, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.12465 0.5617)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (385, LEFT('river', 150), 0.57726, 25.12037, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.12037 0.57726)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (386, LEFT('river', 150), 0.58076, 24.76016, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.76016 0.5807600000000001)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (387, LEFT('river', 150), 0.62863, 24.66369, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.66369 0.62863)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (388, LEFT('river', 150), 0.73787, 24.56351, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.56351 0.73787)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (389, LEFT('river', 150), 0.75207, 24.38852, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.38852 0.75207)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (390, LEFT('river', 150), 0.76418, 24.26162, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.26162 0.76418)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (391, LEFT('river', 150), 1.00697, 24.07055, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.07055 1.00697)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (392, LEFT('river', 150), 1.07552, 23.9455, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.9455 1.07552)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (393, LEFT('river', 150), 1.1439, 23.64689, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.64689 1.1439)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (394, LEFT('river', 150), 1.23029, 23.61245, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.61245 1.23029)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (395, LEFT('river', 150), 1.34062, 23.42339, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.42339 1.34062)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (396, LEFT('river', 150), 1.47916, 23.37817, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.37817 1.47916)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (397, LEFT('river', 150), 1.51695, 23.34665, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.34665 1.51695)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (398, LEFT('river', 150), 1.8104, 23.06598, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.06598 1.8104)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (399, LEFT('river', 150), 1.99233, 22.70948, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.70948 1.99233)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (400, LEFT('river', 150), 2.06387, 22.69562, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.69562 2.06387)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (401, LEFT('river', 150), 2.1277, 22.59548, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.59548 2.1277)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (402, LEFT('river', 150), 2.19798, 22.45144, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.45144 2.19798)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (403, LEFT('river', 150), 2.20191, 22.3409, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.3409 2.20191)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (404, LEFT('river', 150), 2.21681, 21.98516, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.98516 2.21681)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (405, LEFT('river', 150), 2.18374, 21.89175, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.89175 2.18374)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (406, LEFT('river', 150), 2.17607, 21.66269, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.66269 2.17607)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (407, LEFT('river', 150), 2.10542, 21.48115, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.48115 2.10542)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (408, LEFT('river', 150), 2.07412, 21.14133, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.14133 2.07412)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (409, LEFT('river', 150), 2.04397, 21.08333, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.08333 2.04397)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (410, LEFT('river', 150), 2.0506, 21.02231, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (21.02231 2.0506)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (411, LEFT('river', 150), 1.96798, 20.6944, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.6944 1.96798)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (412, LEFT('river', 150), 1.97107, 20.66985, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.66985 1.97107)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (413, LEFT('river', 150), 1.9978, 20.57103, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.57103 1.9978)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (414, LEFT('river', 150), 2.01597, 20.41854, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.41854 2.01597)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (415, LEFT('river', 150), 2.00441, 20.37641, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.37641 2.00441)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (416, LEFT('river', 150), 1.96333, 20.19882, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.19882 1.96333)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (417, LEFT('river', 150), 1.97888, 20.12881, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.12881 1.97888)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (418, LEFT('river', 150), 1.97022, 20.06342, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.06342 1.97022)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (419, LEFT('river', 150), 1.90961, 19.81715, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.81715 1.90961)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (420, LEFT('river', 150), 1.85561, 19.78517, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.78517 1.85561)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (421, LEFT('river', 150), 1.81498, 19.47446, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.47446 1.81498)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (422, LEFT('river', 150), 1.7563, 19.36773, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.36773 1.7563)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (423, LEFT('river', 150), 1.51539, 19.01712, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.01712 1.51539)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (424, LEFT('river', 150), 1.48418, 18.92762, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.92762 1.48418)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (425, LEFT('river', 150), 1.22534, 18.66453, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.66453 1.22534)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (426, LEFT('river', 150), 1.03679, 18.54188, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.54188 1.03679)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (427, LEFT('river', 150), 0.92878, 18.45535, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.45535 0.92878)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (428, LEFT('river', 150), 0.87151, 18.3932, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.3932 0.87151)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (429, LEFT('river', 150), 0.68552, 18.40132, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.40132 0.68552)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (430, LEFT('river', 150), 0.46291, 18.32476, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.32476 0.46291)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (431, LEFT('river', 150), 0.37927, 18.33594, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.33594 0.37927)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (432, LEFT('river', 150), 0.10862, 18.29738, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.29738 0.10862)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (433, LEFT('river', 150), 0.07411, 18.31294, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.31294 0.07411)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (434, LEFT('river', 150), 0.08878, 18.29954, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.29954 0.08878)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (435, LEFT('river', 150), 0.03617, 18.21978, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.21978 0.03617)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (436, LEFT('river', 150), -0.13231, 18.03406, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.03406 -0.13231)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (437, LEFT('river', 150), -0.27966, 17.98013, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.98013 -0.27966)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (438, LEFT('river', 150), -0.35979, 17.7493, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.7493 -0.35979)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (439, LEFT('river', 150), 0.45521, 18.01536, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.01536 0.45521)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (440, LEFT('river', 150), 0.43545, 17.95775, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.95775 0.43545)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (441, LEFT('river', 150), 0.3213, 17.94802, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.94802 0.3213)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (442, LEFT('river', 150), -0.03344, 17.74838, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.74838 -0.03344)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (443, LEFT('river', 150), -0.50086, 17.70299, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.70299 -0.50086)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (444, LEFT('river', 150), -0.60979, 17.6667, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.6667 -0.6097900000000001)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (445, LEFT('river', 150), -0.60096, 17.80677, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.80677 -0.60096)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (446, LEFT('river', 150), -0.92104, 17.38049, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.38049 -0.92104)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (447, LEFT('river', 150), -0.93318, 17.41887, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.41887 -0.93318)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (448, LEFT('river', 150), -1.07204, 17.25941, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.25941 -1.07204)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (449, LEFT('river', 150), -1.11615, 16.98184, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.98184 -1.11615)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (450, LEFT('river', 150), -1.21323, 16.82852, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.82852 -1.21323)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (451, LEFT('river', 150), -1.44976, 16.70918, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.70918 -1.44976)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (452, LEFT('river', 150), -1.71856, 16.66493, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.66493 -1.71856)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (453, LEFT('river', 150), -1.83955, 16.55708, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.55708 -1.83955)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (454, LEFT('river', 150), -1.88037, 16.5707, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.5707 -1.88037)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (455, LEFT('river', 150), -2.12641, 16.30363, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.30363 -2.12641)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (456, LEFT('river', 150), -2.1363, 16.21045, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.21045 -2.1363)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (457, LEFT('river', 150), -2.58017, 16.22771, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.22771 -2.58017)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (458, LEFT('river', 150), -2.85292, 16.19969, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.19969 -2.85292)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (459, LEFT('river', 150), -3.03441, 16.18713, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.18713 -3.03441)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (460, LEFT('river', 150), -3.17704, 16.19888, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.19888 -3.17704)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (461, LEFT('river', 150), -3.30641, 16.24334, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.24334 -3.30641)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (462, LEFT('river', 150), -3.43544, 16.15209, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.15209 -3.43544)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (463, LEFT('river', 150), -3.56176, 16.09987, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.09987 -3.56176)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (464, LEFT('river', 150), -3.75764, 15.98894, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.98894 -3.75764)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (465, LEFT('river', 150), -3.82762, 15.94585, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.94585 -3.82762)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (466, LEFT('river', 150), -3.94968, 15.91093, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.91093 -3.94968)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (467, LEFT('river', 150), -3.94992, 15.92261, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.92261 -3.94992)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (468, LEFT('river', 150), -4.01975, 15.61323, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.61323 -4.01975)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (469, LEFT('river', 150), -4.24711, 15.54679, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.54679 -4.24711)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (470, LEFT('river', 150), -4.30579, 15.35666, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.35666 -4.30579)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (471, LEFT('river', 150), 0.50746, 24.17412, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.17412 0.50746)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (472, LEFT('river', 150), 0.49335, 24.16961, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.16961 0.49335)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (473, LEFT('river', 150), 0.5, 24.17639, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.17639 0.5)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (474, LEFT('river', 150), 0.49806, 24.17, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.17 0.49806)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (475, LEFT('river', 150), 0.49583, 24.17611, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.17611 0.49583)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (476, LEFT('river', 150), 0.49639, 24.17528, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.17528 0.49639)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (477, LEFT('river', 150), 0.49722, 24.1775, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.1775 0.49722)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (478, LEFT('river', 150), 0.76278, 24.59639, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.59639 0.76278)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (479, LEFT('river', 150), 0.7575, 24.59611, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.59611 0.7575)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (480, LEFT('river', 150), 0.77889, 24.60417, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.60417 0.77889)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (481, LEFT('river', 150), 0.76556, 24.59778, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.59778 0.76556)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (482, LEFT('river', 150), 0.7775, 24.60278, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.60278 0.7775)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (483, LEFT('river', 150), 0.78444, 24.60417, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.60417 0.78444)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (484, LEFT('river', 150), 0.74083, 24.56278, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.56278 0.74083)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (485, LEFT('river', 150), 0.73722, 24.56306, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.56306 0.73722)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (486, LEFT('river', 150), 0.73639, 24.56194, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.56194 0.73639)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (487, LEFT('river', 150), 0.72972, 24.55889, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.55889 0.72972)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (488, LEFT('river', 150), 0.7325, 24.56389, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.56389 0.7325)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (489, LEFT('river', 150), 0.72444, 24.56056, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.56056 0.72444)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (490, LEFT('river', 150), 0.71583, 24.5575, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.5575 0.71583)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (491, LEFT('river', 150), 0.49356, 24.16944, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.16944 0.49356)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (492, LEFT('river', 150), 0.49532, 24.17608, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.17608 0.49532)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (493, LEFT('river', 150), 0.51489, 24.17585, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.17585 0.51489)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (494, LEFT('river', 150), 0.77375, 24.59666, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.59666 0.77375)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (495, LEFT('river', 150), 0.76187, 24.59599, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.59599 0.76187)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (496, LEFT('river', 150), 0.77518, 24.59874, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.59874 0.77518)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (497, LEFT('river', 150), 0.71093, 24.56987, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.56987 0.71093)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (498, LEFT('river', 150), 0.7251, 24.56259, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.56259 0.7251)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (499, LEFT('river', 150), 0.77384, 24.59661, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.59661 0.77384)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (500, LEFT('river', 150), 0.77109, 24.59753, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.59753 0.7710900000000001)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (501, LEFT('river', 150), 0.77668, 24.59986, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.59986 0.77668)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (502, LEFT('river', 150), 0.49339, 24.1696, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.1696 0.49339)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (503, LEFT('river', 150), 0.4897, 24.17728, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.17728 0.4897)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (504, LEFT('river', 150), 0.49822, 24.1701, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.1701 0.49822)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (505, LEFT('river', 150), 0.51405, 24.17295, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.17295 0.51405)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (506, LEFT('river', 150), 0.79495, 24.28214, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.28214 0.79495)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (507, LEFT('river', 150), 0.76869, 24.26612, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.26612 0.76869)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (508, LEFT('river', 150), 0.78778, 24.29666, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.29666 0.78778)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (509, LEFT('river', 150), 0.7381, 24.22818, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.22818 0.7381)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (510, LEFT('river', 150), 0.74073, 24.2368, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.2368 0.74073)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (511, LEFT('river', 150), 0.77258, 24.31222, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.31222 0.77258)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (512, LEFT('river', 150), 0.77206, 24.31145, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.31145 0.77206)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (513, LEFT('river', 150), 0.7699, 24.31001, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.31001 0.7699)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (514, LEFT('river', 150), 0.7682, 24.30763, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.30763 0.7682)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (515, LEFT('river', 150), 0.7667, 24.30437, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.30437 0.7667)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (516, LEFT('river', 150), 0.76535, 24.30192, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.30192 0.76535)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (517, LEFT('river', 150), 0.76393, 24.2996, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.2996 0.76393)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (518, LEFT('river', 150), 0.76224, 24.29678, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.29678 0.76224)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (519, LEFT('river', 150), 0.76112, 24.2965, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.2965 0.76112)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (520, LEFT('river', 150), 0.76038, 24.29663, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.29663 0.7603799999999999)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (521, LEFT('river', 150), 0.77258, 24.3122, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.3122 0.77258)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (522, LEFT('river', 150), 0.76659, 24.30437, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.30437 0.76659)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (523, LEFT('river', 150), 0.76113, 24.2964, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.2964 0.76113)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (524, LEFT('river', 150), 0.76073, 24.29645, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.29645 0.76073)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (525, LEFT('river', 150), 0.73122, 24.43459, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.43459 0.73122)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (526, LEFT('river', 150), 0.64391, 24.66294, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.66294 0.64391)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (527, LEFT('river', 150), 0.57749, 24.90082, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.90082 0.5774899999999999)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (528, LEFT('river', 150), 0.56177, 25.12514, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.12514 0.56177)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (529, LEFT('river', 150), 0.57483, 25.12012, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.12012 0.57483)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (530, LEFT('river', 150), 0.50237, 25.19596, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.19596 0.50237)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (531, LEFT('river', 150), 0.49895, 25.20037, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.20037 0.49895)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (532, LEFT('river', 150), 0.49964, 25.19793, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.19793 0.49964)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (533, LEFT('river', 150), 0.4999, 25.19843, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.19843 0.4999)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (534, LEFT('river', 150), 0.49936, 25.19871, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.19871 0.49936)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (535, LEFT('river', 150), 0.49929, 25.1967, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.1967 0.49929)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (536, LEFT('river', 150), 0.50062, 25.19738, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.19738 0.50062)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (537, LEFT('river', 150), 0.54198, 25.18583, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.18583 0.54198)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (538, LEFT('river', 150), 0.54244, 25.18632, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.18632 0.54244)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (539, LEFT('river', 150), 0.54234, 25.18611, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.18611 0.54234)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (540, LEFT('river', 150), 0.54215, 25.18618, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.18618 0.54215)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (541, LEFT('river', 150), 0.54222, 25.18615, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.18615 0.54222)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (542, LEFT('river', 150), 0.54215, 25.18617, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.18617 0.54215)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (543, LEFT('river', 150), -3.17305, 28.18552, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.18552 -3.17305)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (544, LEFT('river', 150), -3.17425, 28.18598, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.18598 -3.17425)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (545, LEFT('river', 150), -3.26813, 28.12542, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.12542 -3.26813)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (546, LEFT('river', 150), -3.04593, 28.2161, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.2161 -3.04593)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (547, LEFT('river', 150), -3.31022, 28.086, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.086 -3.31022)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (548, LEFT('river', 150), -2.99275, 28.47267, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.47267 -2.99275)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (549, LEFT('river', 150), -2.88787, 28.57363, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.57363 -2.88787)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (550, LEFT('river', 150), -1.52117, 28.11447, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.11447 -1.52117)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (551, LEFT('river', 150), -1.47442, 28.09802, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.09802 -1.47442)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (552, LEFT('river', 150), -1.39422, 28.09373, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.09373 -1.39422)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (553, LEFT('river', 150), -1.43147, 28.07405, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.07405 -1.43147)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (554, LEFT('river', 150), -1.4233, 28.07005, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.07005 -1.4233)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (555, LEFT('river', 150), -1.32723, 27.95003, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.95003 -1.32723)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (556, LEFT('river', 150), -1.29023, 27.80885, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.80885 -1.29023)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (557, LEFT('river', 150), -1.28293, 27.80332, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.80332 -1.28293)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (558, LEFT('river', 150), 4.91439, 18.00844, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.00844 4.91439)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (559, LEFT('river', 150), 4.6655, 18.22128, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.22128 4.6655)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (560, LEFT('river', 150), 4.53083, 18.46867, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.46867 4.53083)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (561, LEFT('river', 150), 4.05069, 17.34492, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.34492 4.05069)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (562, LEFT('river', 150), 3.9445, 17.025, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.025 3.9445)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (563, LEFT('river', 150), 4.17358, 17.22372, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.22372 4.17358)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (564, LEFT('river', 150), 3.90408, 17.11038, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.11038 3.90408)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (565, LEFT('river', 150), 3.90394, 17.11073, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.11073 3.90394)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (566, LEFT('river', 150), 3.89716, 17.15729, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.15729 3.89716)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (567, LEFT('river', 150), 3.90082, 17.15848, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.15848 3.90082)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (568, LEFT('river', 150), 4.06681, 17.3209, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.3209 4.06681)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (569, LEFT('river', 150), 4.07166, 17.30829, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.30829 4.07166)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (570, LEFT('river', 150), 4.08135, 17.3074, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.3074 4.08135)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (571, LEFT('river', 150), 4.10503, 17.29411, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.29411 4.10503)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (572, LEFT('river', 150), 4.02745, 17.32564, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.32564 4.02745)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (573, LEFT('river', 150), 3.75467, 17.51074, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.51074 3.75467)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (574, LEFT('river', 150), 3.75407, 17.52856, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.52856 3.75407)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (575, LEFT('river', 150), 3.79562, 17.49983, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.49983 3.79562)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (576, LEFT('river', 150), 3.87487, 17.47599, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.47599 3.87487)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (577, LEFT('river', 150), 3.75596, 17.37455, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.37455 3.75596)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (578, LEFT('river', 150), 3.75558, 17.38182, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.38182 3.75558)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (579, LEFT('river', 150), 3.80638, 17.322, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.322 3.80638)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (580, LEFT('river', 150), 3.84314, 17.26092, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.26092 3.84314)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (581, LEFT('river', 150), 4.08147, 17.30735, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.30735 4.08147)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (582, LEFT('river', 150), 4.06685, 17.3209, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.3209 4.06685)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (583, LEFT('river', 150), 4.00858, 17.38897, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.38897 4.00858)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (584, LEFT('river', 150), 3.96712, 17.41333, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.41333 3.96712)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (585, LEFT('river', 150), 3.9285, 17.43455, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.43455 3.9285)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (586, LEFT('river', 150), 3.87355, 17.46859, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.46859 3.87355)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (587, LEFT('river', 150), 3.84159, 17.487, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.487 3.84159)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (588, LEFT('river', 150), 3.75726, 17.53485, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.53485 3.75726)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (589, LEFT('river', 150), 3.79557, 17.49878, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.49878 3.79557)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (590, LEFT('river', 150), 3.75453, 17.51075, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.51075 3.75453)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (591, LEFT('river', 150), 3.89735, 17.15737, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.15737 3.89735)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (592, LEFT('river', 150), 3.90075, 17.15847, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.15847 3.90075)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (593, LEFT('river', 150), 4.35, 18.56667, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.56667 4.35)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (594, LEFT('river', 150), 0.67127, 24.61258, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.61258 0.67127)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (595, LEFT('river', 150), 0.76861, 24.26611, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.26611 0.76861)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (596, LEFT('river', 150), 0.78522, 24.27687, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.27687 0.78522)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (597, LEFT('river', 150), 0.79461, 24.29373, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.29373 0.79461)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (598, LEFT('river', 150), 0.75107, 24.28226, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.28226 0.75107)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (599, LEFT('river', 150), 0.82639, 24.32908, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.32908 0.82639)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (600, LEFT('river', 150), 0.84339, 24.34464, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.34464 0.84339)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (601, LEFT('river', 150), 0.83128, 24.32931, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.32931 0.83128)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (602, LEFT('river', 150), 0.80925, 24.23403, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.23403 0.80925)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (603, LEFT('river', 150), 1.09653, 23.86629, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.86629 1.09653)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (604, LEFT('river', 150), 1.1892, 23.57981, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.57981 1.1892)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (605, LEFT('river', 150), 1.54824, 23.27398, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.27398 1.54824)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (606, LEFT('river', 150), 1.94114, 22.85998, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.85998 1.94114)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (607, LEFT('river', 150), 2.03829, 22.82548, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.82548 2.03829)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (608, LEFT('river', 150), 2.06369, 22.81901, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.81901 2.06369)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (609, LEFT('river', 150), 2.04136, 22.74762, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.74762 2.04136)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (610, LEFT('river', 150), 2.08921, 22.6544, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.6544 2.08921)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (611, LEFT('river', 150), 2.04847, 22.74363, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.74363 2.04847)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (612, LEFT('river', 150), 2.17192, 22.45778, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.45778 2.17192)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (613, LEFT('river', 150), 1.77514, 23.10255, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.10255 1.77514)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (614, LEFT('river', 150), 1.23367, 23.61885, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.61885 1.23367)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (615, LEFT('river', 150), 1.24753, 23.65052, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.65052 1.24753)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (616, LEFT('river', 150), 1.24816, 23.72787, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.72787 1.24816)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (617, LEFT('river', 150), 1.28785, 23.79998, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.79998 1.28785)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (618, LEFT('river', 150), 1.29425, 23.85729, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.85729 1.29425)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (619, LEFT('river', 150), 1.31383, 23.96778, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.96778 1.31383)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (620, LEFT('river', 150), 1.307, 23.96771, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.96771 1.307)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (621, LEFT('river', 150), 1.24669, 23.91302, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.91302 1.24669)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (622, LEFT('river', 150), 1.2487, 23.92577, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.92577 1.2487)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (623, LEFT('river', 150), 1.26915, 23.73422, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.73422 1.26915)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (624, LEFT('river', 150), 0.99451, 24.11224, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.11224 0.99451)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (625, LEFT('river', 150), 0.63518, 24.1838, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.1838 0.63518)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (626, LEFT('river', 150), 0.67421, 24.1899, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.1899 0.67421)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (627, LEFT('river', 150), 0.49002, 24.17682, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.17682 0.49002)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (628, LEFT('river', 150), 0.47537, 24.16486, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.16486 0.47537)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (629, LEFT('river', 150), 0.63324, 24.26401, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.26401 0.63324)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (630, LEFT('river', 150), 0.86665, 24.19778, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.19778 0.86665)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (631, LEFT('river', 150), 0.76711, 24.26552, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.26552 0.76711)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (632, LEFT('river', 150), 0.73781, 24.2277, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.2277 0.73781)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (633, LEFT('river', 150), 0.73664, 24.22844, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.22844 0.73664)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (634, LEFT('river', 150), 0.76242, 24.31136, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.31136 0.76242)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (635, LEFT('river', 150), 0.72949, 24.4341, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.4341 0.72949)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (636, LEFT('river', 150), 0.74145, 24.46087, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.46087 0.7414500000000001)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (637, LEFT('river', 150), 0.76203, 24.39204, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.39204 0.76203)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (638, LEFT('river', 150), 0.79777, 24.26696, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.26696 0.79777)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (639, LEFT('river', 150), 0.80411, 24.26254, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.26254 0.80411)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (640, LEFT('river', 150), 0.63607, 24.18458, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.18458 0.63607)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (641, LEFT('river', 150), 0.64327, 24.66379, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.66379 0.64327)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (642, LEFT('river', 150), 0.57712, 24.90246, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.90246 0.57712)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (643, LEFT('river', 150), 0.55955, 25.14219, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.14219 0.55955)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (644, LEFT('river', 150), 0.56995, 25.11757, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.11757 0.56995)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (645, LEFT('river', 150), 0.49988, 25.18066, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.18066 0.49988)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (646, LEFT('river', 150), -4.29592, 15.27612, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.27612 -4.29592)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (647, LEFT('river', 150), -5.95568, 12.70453, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (12.70453 -5.95568)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (648, LEFT('river', 150), -5.96425, 12.73255, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (12.73255 -5.96425)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (649, LEFT('river', 150), -1.72653, 29.00993, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.00993 -1.72653)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (650, LEFT('river', 150), -1.71146, 29.01452, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.01452 -1.71146)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (651, LEFT('river', 150), -1.67876, 29.01683, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.01683 -1.67876)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (652, LEFT('river', 150), -1.62221, 29.01493, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.01493 -1.62221)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (653, LEFT('river', 150), -1.57128, 29.04702, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.04702 -1.57128)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (654, LEFT('river', 150), -1.57424, 29.07227, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.07227 -1.57424)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (655, LEFT('river', 150), -1.02778, 29.00429, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.00429 -1.02778)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (656, LEFT('river', 150), -1.03277, 29.00428, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.00428 -1.03277)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (657, LEFT('river', 150), -1.23759, 29.4779, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.4779 -1.23759)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (658, LEFT('river', 150), -1.33366, 29.37209, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.37209 -1.33366)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (659, LEFT('river', 150), -1.27735, 29.38689, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.38689 -1.27735)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (660, LEFT('river', 150), -1.56294, 29.04749, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.04749 -1.56294)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (661, LEFT('river', 150), -1.56425, 29.03872, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.03872 -1.56425)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (662, LEFT('river', 150), -1.56966, 29.04603, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.04603 -1.56966)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (663, LEFT('river', 150), -2.36361, 28.79349, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.79349 -2.36361)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (664, LEFT('river', 150), -2.38463, 28.78865, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.78865 -2.38463)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (665, LEFT('river', 150), -2.414, 28.83461, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.83461 -2.414)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (666, LEFT('river', 150), -2.43544, 28.83179, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.83179 -2.43544)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (667, LEFT('river', 150), -2.47015, 28.83636, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.83636 -2.47015)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (668, LEFT('river', 150), -1.57441, 29.07211, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.07211 -1.57441)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (669, LEFT('river', 150), -1.57485, 29.07219, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.07219 -1.57485)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (670, LEFT('river', 150), -2.36236, 28.79555, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.79555 -2.36236)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (671, LEFT('river', 150), 5.21626, -3.71893, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.71893 5.21626)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (672, LEFT('river', 150), 5.22619, -3.7098, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.7098 5.22619)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (673, LEFT('river', 150), 5.23027, -3.69445, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.69445 5.23027)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (674, LEFT('river', 150), 5.23144, -3.67435, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.67435 5.23144)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (675, LEFT('river', 150), 5.25438, -3.66529, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.66529 5.25438)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (676, LEFT('river', 150), 5.25876, -3.64662, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.64662 5.25876)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (677, LEFT('river', 150), 5.26098, -3.61637, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.61637 5.26098)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (678, LEFT('river', 150), 5.34719, -3.20375, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20375 5.34719)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (679, LEFT('river', 150), 5.35647, -3.20066, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20066 5.35647)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (680, LEFT('river', 150), 5.36252, -3.2054, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.2054 5.36252)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (681, LEFT('river', 150), 5.36493, -3.2076, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.2076 5.36493)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (682, LEFT('river', 150), 5.37043, -3.20686, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20686 5.37043)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (683, LEFT('river', 150), 5.37708, -3.20892, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20892 5.37708)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (684, LEFT('river', 150), 5.12379, -2.94592, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.94592 5.12379)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (685, LEFT('river', 150), 5.12519, -2.94046, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.94046 5.12519)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (686, LEFT('river', 150), 5.12463, -2.93348, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.93348 5.12463)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (687, LEFT('river', 150), 5.1232, -2.93086, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.93086 5.1232)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (688, LEFT('river', 150), 5.12134, -2.92663, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.92663 5.12134)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (689, LEFT('river', 150), 5.12227, -2.92249, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.92249 5.12227)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (690, LEFT('river', 150), 5.21618, -3.71814, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.71814 5.21618)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (691, LEFT('river', 150), 5.22641, -3.70942, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.70942 5.22641)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (692, LEFT('river', 150), 5.22906, -3.69257, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.69257 5.22906)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (693, LEFT('river', 150), 5.23128, -3.6747, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.6747 5.23128)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (694, LEFT('river', 150), 5.25665, -3.66348, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.66348 5.25665)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (695, LEFT('river', 150), 5.25795, -3.64515, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.64515 5.25795)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (696, LEFT('river', 150), 5.24808, -3.63362, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.63362 5.24808)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (697, LEFT('river', 150), 5.26181, -3.61519, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.61519 5.26181)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (698, LEFT('river', 150), 5.35739, -3.2033, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.2033 5.35739)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (699, LEFT('river', 150), 5.35911, -3.20079, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20079 5.35911)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (700, LEFT('river', 150), 5.36267, -3.20658, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20658 5.36267)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (701, LEFT('river', 150), 5.36467, -3.20719, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20719 5.36467)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (702, LEFT('river', 150), 5.37278, -3.20993, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20993 5.37278)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (703, LEFT('river', 150), 5.38078, -3.21198, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.21198 5.38078)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (704, LEFT('river', 150), 5.38166, -3.22182, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.22182 5.38166)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (705, LEFT('river', 150), 5.38893, -3.22032, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.22032 5.38893)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (706, LEFT('river', 150), 5.12559, -2.9419, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.9419 5.12559)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (707, LEFT('river', 150), 5.12277, -2.93439, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.93439 5.12277)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (708, LEFT('river', 150), 5.12144, -2.92387, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.92387 5.12144)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (709, LEFT('river', 150), 5.12104, -2.9129, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.9129 5.12104)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (710, LEFT('river', 150), 5.1233, -2.90544, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.90544 5.1233)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (711, LEFT('river', 150), 5.12268, -2.89659, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.89659 5.12268)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (712, LEFT('river', 150), 5.12377, -2.89101, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.89101 5.12377)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (713, LEFT('river', 150), 5.12339, -2.88452, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.88452 5.12339)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (714, LEFT('river', 150), 5.21539, -3.71902, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.71902 5.21539)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (715, LEFT('river', 150), 5.22677, -3.70971, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.70971 5.22677)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (716, LEFT('river', 150), 5.22935, -3.693, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.693 5.22935)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (717, LEFT('river', 150), 5.23158, -3.67479, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.67479 5.23158)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (718, LEFT('river', 150), 5.2525, -3.66644, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.66644 5.2525)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (719, LEFT('river', 150), 5.25778, -3.6442, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.6442 5.25778)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (720, LEFT('river', 150), 5.24973, -3.62204, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.62204 5.24973)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (721, LEFT('river', 150), 5.26205, -3.6149, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.6149 5.26205)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (722, LEFT('river', 150), 5.34778, -3.20305, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20305 5.34778)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (723, LEFT('river', 150), 5.35638, -3.20075, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20075 5.35638)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (724, LEFT('river', 150), 5.36238, -3.2066, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.2066 5.36238)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (725, LEFT('river', 150), 5.36489, -3.20503, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20503 5.36489)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (726, LEFT('river', 150), 5.38092, -3.20979, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20979 5.38092)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (727, LEFT('river', 150), 5.38233, -3.22134, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.22134 5.38233)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (728, LEFT('river', 150), 5.38942, -3.22127, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.22127 5.38942)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (729, LEFT('river', 150), 5.38863, -3.22672, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.22672 5.38863)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (730, LEFT('river', 150), 5.12461, -2.94443, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.94443 5.12461)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (731, LEFT('river', 150), 5.12256, -2.93424, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.93424 5.12256)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (732, LEFT('river', 150), 5.12113, -2.92885, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.92885 5.12113)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (733, LEFT('river', 150), 5.12189, -2.91415, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.91415 5.12189)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (734, LEFT('river', 150), 5.12301, -2.90504, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.90504 5.12301)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (735, LEFT('river', 150), 5.12274, -2.89664, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.89664 5.12274)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (736, LEFT('river', 150), 5.1246, -2.89098, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.89098 5.1246)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (737, LEFT('river', 150), 5.12496, -2.88266, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.88266 5.12496)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (738, LEFT('river', 150), 5.21569, -3.71784, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.71784 5.21569)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (739, LEFT('river', 150), 5.2287, -3.70839, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.70839 5.2287)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (740, LEFT('river', 150), 5.2273, -3.68775, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.68775 5.2273)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (741, LEFT('river', 150), 5.24683, -3.66867, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.66867 5.24683)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (742, LEFT('river', 150), 5.25969, -3.65107, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.65107 5.25969)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (743, LEFT('river', 150), 5.25007, -3.63484, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.63484 5.25007)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (744, LEFT('river', 150), 5.25105, -3.62592, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.62592 5.25105)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (745, LEFT('river', 150), 5.26177, -3.61501, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.61501 5.26177)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (746, LEFT('river', 150), 5.34822, -3.20292, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20292 5.34822)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (747, LEFT('river', 150), 5.35681, -3.20066, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20066 5.35681)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (748, LEFT('river', 150), 5.36235, -3.20665, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20665 5.36235)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (749, LEFT('river', 150), 5.36575, -3.20519, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20519 5.36575)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (750, LEFT('river', 150), 5.38026, -3.20964, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.20964 5.38026)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (751, LEFT('river', 150), 5.37979, -3.22134, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.22134 5.37979)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (752, LEFT('river', 150), 5.38895, -3.22234, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.22234 5.38895)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (753, LEFT('river', 150), 5.38868, -3.22728, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-3.22728 5.38868)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (754, LEFT('river', 150), 5.12568, -2.94278, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.94278 5.12568)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (755, LEFT('river', 150), 5.12336, -2.93472, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.93472 5.12336)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (756, LEFT('river', 150), 5.1216, -2.92366, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-2.92366 5.1216)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (757, LEFT('river', 150), -0.59907, 10.311, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (10.311 -0.59907)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (758, LEFT('river', 150), -0.70607, 10.22485, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (10.22485 -0.70607)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (759, LEFT('river', 150), 13.56698, 2.00608, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (2.00608 13.56698)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (760, LEFT('river', 150), -11.12198, 24.19863, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.19863 -11.12198)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (761, LEFT('river', 150), -13.09435, 22.68761, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.68761 -13.09435)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (762, LEFT('river', 150), -14.3772, 23.23589, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.23589 -14.3772)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (763, LEFT('river', 150), -16.24215, 23.24111, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.24111 -16.24215)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (764, LEFT('river', 150), -17.46662, 24.247, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.247 -17.46662)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (765, LEFT('river', 150), -17.79845, 25.28052, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.28052 -17.79845)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (766, LEFT('river', 150), -17.88739, 25.84265, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.84265 -17.88739)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (767, LEFT('river', 150), -17.93098, 25.85963, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.85963 -17.93098)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (768, LEFT('river', 150), -16.03506, 28.85822, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.85822 -16.03506)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (769, LEFT('river', 150), -15.7244, 29.32284, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.32284 -15.7244)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (770, LEFT('river', 150), -15.62437, 30.41347, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.41347 -15.62437)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (771, LEFT('river', 150), -12.46425, 27.85076, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.85076 -12.46425)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (772, LEFT('river', 150), -12.645, 28.1647, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.1647 -12.645)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (773, LEFT('river', 150), -13.64231, 27.61623, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.61623 -13.64231)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (774, LEFT('river', 150), -14.56243, 26.45772, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.45772 -14.56243)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (775, LEFT('river', 150), -14.94511, 25.91404, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.91404 -14.94511)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (776, LEFT('river', 150), -15.76383, 26.03033, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.03033 -15.76383)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (777, LEFT('river', 150), -15.67564, 26.44536, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.44536 -15.67564)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (778, LEFT('river', 150), -15.74914, 27.82954, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.82954 -15.74914)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (779, LEFT('river', 150), -15.83655, 28.23771, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.23771 -15.83655)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (780, LEFT('river', 150), -15.94567, 28.87528, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.87528 -15.94567)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (781, LEFT('river', 150), -13.09776, 31.78599, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (31.78599 -13.09776)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (782, LEFT('river', 150), -14.30454, 30.55045, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.55045 -14.30454)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (783, LEFT('river', 150), -14.97456, 30.21181, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.21181 -14.97456)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (784, LEFT('river', 150), -15.60938, 30.4105, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.4105 -15.60938)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (785, LEFT('river', 150), -14.30752, 29.12416, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.12416 -14.30752)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (786, LEFT('river', 150), -14.78429, 29.62916, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.62916 -14.78429)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (787, LEFT('river', 150), -12.26056, 26.79241, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.79241 -12.26056)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (788, LEFT('river', 150), -12.99708, 26.53035, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.53035 -12.99708)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (789, LEFT('river', 150), -13.96352, 26.34692, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.34692 -13.96352)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (790, LEFT('river', 150), -11.88855, 25.25051, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.25051 -11.88855)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (791, LEFT('river', 150), -15.62074, 33.00953, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (33.00953 -15.62074)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (792, LEFT('river', 150), -16.13954, 33.54203, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (33.54203 -16.13954)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (793, LEFT('river', 150), -16.71482, 34.24946, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (34.24946 -16.71482)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (794, LEFT('river', 150), -17.45931, 35.05923, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (35.05923 -17.45931)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (795, LEFT('river', 150), -17.80579, 35.39935, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (35.39935 -17.80579)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (796, LEFT('river', 150), -18.36487, 36.05988, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.05988 -18.36487)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (797, LEFT('river', 150), -18.5486, 36.19319, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.19319 -18.5486)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (798, LEFT('river', 150), -17.66801, 35.33752, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (35.33752 -17.66801)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (799, LEFT('river', 150), -16.03056, 28.85812, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.85812 -16.03056)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (800, LEFT('river', 150), -15.63372, 30.40524, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.40524 -15.63372)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (801, LEFT('river', 150), -15.83654, 28.23769, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.23769 -15.83654)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (802, LEFT('river', 150), -15.9512, 28.86024, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.86024 -15.9512)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (803, LEFT('river', 150), -15.62103, 30.41623, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.41623 -15.62103)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (804, LEFT('river', 150), -13.10773, 22.68901, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.68901 -13.10773)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (805, LEFT('river', 150), -14.33721, 23.23592, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.23592 -14.33721)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (806, LEFT('river', 150), -16.24473, 23.23882, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.23882 -16.24473)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (807, LEFT('river', 150), -17.46661, 24.24698, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.24698 -17.46661)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (808, LEFT('river', 150), -17.79853, 25.28073, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.28073 -17.79853)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (809, LEFT('river', 150), -17.88741, 25.84259, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.84259 -17.88741)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (810, LEFT('river', 150), -17.93106, 25.85963, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.85963 -17.93106)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (811, LEFT('river', 150), -16.01624, 28.87979, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.87979 -16.01624)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (812, LEFT('river', 150), -15.63554, 30.40335, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.40335 -15.63554)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (813, LEFT('river', 150), -12.46425, 27.85079, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.85079 -12.46425)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (814, LEFT('river', 150), -12.64502, 28.16447, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.16447 -12.64502)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (815, LEFT('river', 150), -13.64227, 27.76163, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.76163 -13.64227)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (816, LEFT('river', 150), -14.56245, 26.45769, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.45769 -14.56245)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (817, LEFT('river', 150), -14.9449, 25.91303, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.91303 -14.9449)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (818, LEFT('river', 150), -15.76407, 26.03038, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.03038 -15.76407)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (819, LEFT('river', 150), -15.74653, 27.8296, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.8296 -15.74653)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (820, LEFT('river', 150), -15.83687, 28.32822, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.32822 -15.83687)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (821, LEFT('river', 150), -15.94616, 28.87197, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.87197 -15.94616)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (822, LEFT('river', 150), -10.252, 33.02209, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (33.02209 -10.252)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (823, LEFT('river', 150), -13.0979, 31.78602, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (31.78602 -13.0979)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (824, LEFT('river', 150), -15.00547, 30.21553, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.21553 -15.00547)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (825, LEFT('river', 150), -15.60396, 30.41032, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.41032 -15.60396)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (826, LEFT('river', 150), -13.93198, 29.13162, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.13162 -13.93198)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (827, LEFT('river', 150), -14.78434, 29.6292, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.6292 -14.78434)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (828, LEFT('river', 150), -12.26042, 26.79227, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.79227 -12.26042)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (829, LEFT('river', 150), -13.98387, 26.34687, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.34687 -13.98387)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (830, LEFT('river', 150), -14.03872, 23.629, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.629 -14.03872)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (831, LEFT('river', 150), -16.13964, 33.54084, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (33.54084 -16.13964)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (832, LEFT('river', 150), -17.45938, 35.05922, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (35.05922 -17.45938)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (833, LEFT('river', 150), -17.80587, 35.39949, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (35.39949 -17.80587)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (834, LEFT('river', 150), -18.57924, 36.24422, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.24422 -18.57924)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (835, LEFT('river', 150), -18.56729, 36.44534, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.44534 -18.56729)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (836, LEFT('river', 150), -17.45844, 35.33882, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (35.33882 -17.45844)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (837, LEFT('river', 150), -16.54353, 33.38056, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (33.38056 -16.54353)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (838, LEFT('river', 150), -10.10472, 30.91496, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.91496 -10.10472)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (839, LEFT('river', 150), -10.10837, 30.91707, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.91707 -10.10837)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (840, LEFT('river', 150), -10.1199, 30.91534, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.91534 -10.1199)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (841, LEFT('river', 150), -8.59647, 31.23948, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (31.23948 -8.59647)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (842, LEFT('river', 150), -11.73076, 31.49518, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (31.49518 -11.73076)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (843, LEFT('river', 150), -11.73056, 31.49466, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (31.49466 -11.73056)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (844, LEFT('river', 150), -10.75313, 32.00543, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (32.00543 -10.75313)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (845, LEFT('river', 150), -10.74828, 32.00336, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (32.00336 -10.74828)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (846, LEFT('river', 150), -13.15368, 30.70293, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.70293 -13.15368)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (847, LEFT('river', 150), -13.15412, 30.70336, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.70336 -13.15412)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (848, LEFT('river', 150), -13.15467, 30.70447, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.70447 -13.15467)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (849, LEFT('river', 150), -11.3503, 24.32862, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.32862 -11.3503)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (850, LEFT('river', 150), -13.09744, 22.68542, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.68542 -13.09744)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (851, LEFT('river', 150), -14.38381, 23.2362, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.2362 -14.38381)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (852, LEFT('river', 150), -15.20596, 22.92231, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.92231 -15.20596)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (853, LEFT('river', 150), -16.13003, 23.28826, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.28826 -16.13003)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (854, LEFT('river', 150), -17.46667, 24.24691, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.24691 -17.46667)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (855, LEFT('river', 150), -17.8874, 25.84263, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.84263 -17.8874)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (856, LEFT('river', 150), -16.50434, 28.79071, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.79071 -16.50434)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (857, LEFT('river', 150), -15.98502, 28.88075, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.88075 -15.98502)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (858, LEFT('river', 150), -15.62444, 30.41351, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.41351 -15.62444)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (859, LEFT('river', 150), -12.46428, 27.85069, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.85069 -12.46428)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (860, LEFT('river', 150), -14.56235, 26.45759, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.45759 -14.56235)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (861, LEFT('river', 150), -14.97784, 25.9926, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.9926 -14.97784)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (862, LEFT('river', 150), -15.76377, 26.03031, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.03031 -15.76377)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (863, LEFT('river', 150), -15.74789, 27.82828, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.82828 -15.74789)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (864, LEFT('river', 150), -15.83649, 28.23764, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.23764 -15.83649)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (865, LEFT('river', 150), -15.95124, 28.86022, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.86022 -15.95124)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (866, LEFT('river', 150), -15.94621, 28.87198, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.87198 -15.94621)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (867, LEFT('river', 150), -15.95138, 28.86036, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.86036 -15.95138)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (868, LEFT('river', 150), -19.11294, 47.76394, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.76394 -19.11294)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (869, LEFT('river', 150), -19.02003, 47.79169, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.79169 -19.02003)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (870, LEFT('river', 150), -18.41253, 47.88136, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.88136 -18.41253)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (871, LEFT('river', 150), -18.32397, 47.89008, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.89008 -18.32397)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (872, LEFT('river', 150), -18.36306, 47.50225, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.50225 -18.36306)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (873, LEFT('river', 150), -18.23786, 47.61014, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.61014 -18.23786)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (874, LEFT('river', 150), -18.69511, 47.49414, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.49414 -18.69511)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (875, LEFT('river', 150), -19.2945, 47.34111, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.34111 -19.2945)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (876, LEFT('river', 150), -19.00397, 47.12425, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.12425 -19.00397)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (877, LEFT('river', 150), -18.67669, 47.04456, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.04456 -18.67669)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (878, LEFT('river', 150), -18.48833, 47.25011, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.25011 -18.48833)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (879, LEFT('river', 150), -18.19653, 47.04228, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.04228 -18.19653)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (880, LEFT('river', 150), -18.16581, 46.95094, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.95094 -18.16581)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (881, LEFT('river', 150), -18.87325, 47.32506, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.32506 -18.87325)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (882, LEFT('river', 150), -18.30181, 47.31519, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.31519 -18.30181)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (883, LEFT('river', 150), -18.25919, 47.21611, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.21611 -18.25919)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (884, LEFT('river', 150), -18.13503, 47.47947, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.47947 -18.13503)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (885, LEFT('river', 150), -18.02519, 47.39497, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.39497 -18.02519)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (886, LEFT('river', 150), -18.0175, 47.34247, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.34247 -18.0175)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (887, LEFT('river', 150), -17.35539, 46.93022, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.93022 -17.35539)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (888, LEFT('river', 150), -17.02456, 46.75956, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.75956 -17.02456)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (889, LEFT('river', 150), -16.92306, 46.86272, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.86272 -16.92306)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (890, LEFT('river', 150), -17.03847, 46.683, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.683 -17.03847)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (891, LEFT('river', 150), -16.46117, 47.16814, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.16814 -16.46117)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (892, LEFT('river', 150), -16.93794, 46.94858, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.94858 -16.93794)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (893, LEFT('river', 150), -16.23314, 46.54669, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.54669 -16.23314)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (894, LEFT('river', 150), -16.47289, 46.71056, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.71056 -16.47289)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (895, LEFT('river', 150), -16.75447, 47.59894, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.59894 -16.75447)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (896, LEFT('river', 150), -17.18292, 46.83975, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.83975 -17.18292)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (897, LEFT('river', 150), -17.51453, 46.97556, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.97556 -17.51453)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (898, LEFT('river', 150), -17.68272, 46.98811, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.98811 -17.68272)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (899, LEFT('river', 150), -17.98297, 47.02744, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.02744 -17.98297)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (900, LEFT('river', 150), -18.09456, 47.27586, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.27586 -18.09456)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (901, LEFT('river', 150), -17.65269, 47.68769, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.68769 -17.65269)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (902, LEFT('river', 150), -18.52289, 47.54194, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.54194 -18.52289)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (903, LEFT('river', 150), -17.69253, 47.39969, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.39969 -17.69253)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (904, LEFT('river', 150), -17.68911, 47.92281, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.92281 -17.68911)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (905, LEFT('river', 150), -18.44769, 46.57569, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (46.57569 -18.44769)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (906, LEFT('river', 150), -18.93975, 48.416, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.416 -18.93975)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (907, LEFT('river', 150), -18.91189, 48.42258, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.42258 -18.91189)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (908, LEFT('river', 150), -18.96756, 48.73497, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.73497 -18.96756)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (909, LEFT('river', 150), -18.90317, 48.42775, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.42775 -18.90317)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (910, LEFT('river', 150), -18.96092, 48.85289, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.85289 -18.96092)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (911, LEFT('river', 150), -18.997, 48.94561, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.94561 -18.997)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (912, LEFT('river', 150), -18.82389, 49.07139, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (49.07139 -18.82389)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (913, LEFT('river', 150), -18.74039, 48.96578, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.96578 -18.74039)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (914, LEFT('river', 150), -18.73806, 48.98861, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.98861 -18.73806)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (915, LEFT('river', 150), -18.76739, 48.92569, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.92569 -18.76739)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (916, LEFT('river', 150), -18.76186, 48.8825, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.8825 -18.76186)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (917, LEFT('river', 150), -18.649, 48.98042, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.98042 -18.649)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (918, LEFT('river', 150), -18.64619, 48.97061, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.97061 -18.64619)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (919, LEFT('river', 150), -18.80636, 49.07303, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (49.07303 -18.80636)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (920, LEFT('river', 150), -18.46808, 48.99933, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.99933 -18.46808)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (921, LEFT('river', 150), -18.98364, 48.61189, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.61189 -18.98364)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (922, LEFT('river', 150), -18.95486, 47.88339, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.88339 -18.95486)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (923, LEFT('river', 150), -18.91153, 47.91822, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.91822 -18.91153)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (924, LEFT('river', 150), -18.21847, 48.25033, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.25033 -18.21847)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (925, LEFT('river', 150), -18.64811, 48.25039, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.25039 -18.64811)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (926, LEFT('river', 150), -18.86447, 48.06264, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.06264 -18.86447)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (927, LEFT('river', 150), -18.87656, 48.107, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.107 -18.87656)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (928, LEFT('river', 150), -18.25739, 49.26792, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (49.26792 -18.25739)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (929, LEFT('river', 150), -18.82389, 48.07139, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.07139 -18.82389)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (930, LEFT('river', 150), -18.76739, 49.02569, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (49.02569 -18.76739)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (931, LEFT('river', 150), -18.80636, 48.07303, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (48.07303 -18.80636)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (932, LEFT('river', 150), -17.68911, 47.29617, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.29617 -17.68911)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (933, LEFT('river', 150), -16.25106, 47.92281, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (47.92281 -16.25106)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (934, LEFT('river', 150), -4.20381, 39.41556, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.41556 -4.20381)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (935, LEFT('river', 150), -4.19456, 39.47153, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.47153 -4.19456)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (936, LEFT('river', 150), -4.15794, 39.41783, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.41783 -4.15794)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (937, LEFT('river', 150), -4.18106, 39.41922, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.41922 -4.18106)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (938, LEFT('river', 150), -4.27128, 39.40647, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.40647 -4.27128)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (939, LEFT('river', 150), -4.28328, 39.43042, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.43042 -4.28328)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (940, LEFT('river', 150), -4.28519, 39.43128, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.43128 -4.28519)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (941, LEFT('river', 150), -4.36483, 39.33964, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.33964 -4.36483)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (942, LEFT('river', 150), -4.35503, 39.43383, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.43383 -4.35503)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (943, LEFT('river', 150), -4.4215, 39.33958, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.33958 -4.4215)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (944, LEFT('river', 150), -0.37458, 36.88378, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.88378 -0.37458)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (945, LEFT('river', 150), -0.45417, 36.71606, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.71606 -0.45417)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (946, LEFT('river', 150), -0.48686, 36.70797, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.70797 -0.48686)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (947, LEFT('river', 150), -0.52431, 36.72153, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.72153 -0.5243100000000001)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (948, LEFT('river', 150), -0.16464, 38.18767, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.18767 -0.16464)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (949, LEFT('river', 150), -0.15447, 38.18083, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.18083 -0.15447)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (950, LEFT('river', 150), -0.06153, 37.66011, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.66011 -0.06153)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (951, LEFT('river', 150), -0.21422, 37.65711, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.65711 -0.21422)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (952, LEFT('river', 150), -0.28728, 37.66508, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.66508 -0.28728)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (953, LEFT('river', 150), -0.35417, 37.60775, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.60775 -0.35417)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (954, LEFT('river', 150), -0.39497, 37.62839, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.62839 -0.39497)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (955, LEFT('river', 150), -0.78744, 37.26889, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.26889 -0.78744)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (956, LEFT('river', 150), -0.87381, 37.5915, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.5915 -0.87381)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (957, LEFT('river', 150), -0.474, 37.91261, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.91261 -0.474)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (958, LEFT('river', 150), -0.07767, 38.41469, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.41469 -0.07767)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (959, LEFT('river', 150), -0.32031, 39.56169, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.56169 -0.32031)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (960, LEFT('river', 150), -0.81717, 39.83944, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.83944 -0.81717)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (961, LEFT('river', 150), -1.67731, 40.11953, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (40.11953 -1.67731)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (962, LEFT('river', 150), -1.87589, 40.14089, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (40.14089 -1.87589)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (963, LEFT('river', 150), -2.28886, 40.12664, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (40.12664 -2.28886)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (964, LEFT('river', 150), -2.40983, 40.35183, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (40.35183 -2.40983)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (965, LEFT('river', 150), -0.4572, 36.7026, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.7026 -0.4572)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (966, LEFT('river', 150), -0.4704, 36.7123, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.7123 -0.4704)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (967, LEFT('river', 150), -0.4866, 36.7076, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.7076 -0.4866)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (968, LEFT('river', 150), -0.5299, 36.7166, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.7166 -0.5299)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (969, LEFT('river', 150), -0.3873, 36.8168, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.8168 -0.3873)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (970, LEFT('river', 150), -0.3613, 36.6737, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.6737 -0.3613)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (971, LEFT('river', 150), -0.3746, 36.8837, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.8837 -0.3746)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (972, LEFT('river', 150), -0.4151, 36.9436, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.9436 -0.4151)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (973, LEFT('river', 150), -0.499, 36.9363, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.9363 -0.499)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (974, LEFT('river', 150), -0.8341, 37.6731, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.6731 -0.8341)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (975, LEFT('river', 150), -0.5671, 37.3226, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.3226 -0.5671)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (976, LEFT('river', 150), -0.5474, 37.3886, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.3886 -0.5474)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (977, LEFT('river', 150), -0.545, 37.449, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.449 -0.545)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (978, LEFT('river', 150), -0.3995, 37.4717, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.4717 -0.3995)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (979, LEFT('river', 150), -0.3843, 37.4588, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.4588 -0.3843)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (980, LEFT('river', 150), -0.3811, 37.4531, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.4531 -0.3811)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (981, LEFT('river', 150), -0.3659, 37.3106, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.3106 -0.3659)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (982, LEFT('river', 150), -2.4027, 40.3515, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (40.3515 -2.4027)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (983, LEFT('river', 150), -0.3988, 37.3086, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.3086 -0.3988)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (984, LEFT('river', 150), -0.5043, 37.3211, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.3211 -0.5043)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (985, LEFT('river', 150), -0.1543, 37.4385, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.4385 -0.1543)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (986, LEFT('river', 150), -0.2514, 37.6, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.6 -0.2514)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (987, LEFT('river', 150), -0.2401, 37.5985, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.5985 -0.2401)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (988, LEFT('river', 150), -1.0261, 37.2447, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.2447 -1.0261)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (989, LEFT('river', 150), -0.7141, 37.1806, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.1806 -0.7141)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (990, LEFT('river', 150), -0.4461, 37.7894, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.7894 -0.4461)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (991, LEFT('river', 150), -0.3089, 37.8735, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.8735 -0.3089)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (992, LEFT('river', 150), -0.344, 37.8708, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.8708 -0.344)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (993, LEFT('river', 150), -0.1508, 37.9721, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.9721 -0.1508)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (994, LEFT('river', 150), -0.1, 38.0088, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.0088 -0.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (995, LEFT('river', 150), 0.2687, 38.1321, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.1321 0.2687)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (996, LEFT('river', 150), -0.0693, 38.4187, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.4187 -0.0693)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (997, LEFT('river', 150), 0.0231, 38.0662, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.0662 0.0231)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (998, LEFT('river', 150), 0.2151, 38.1292, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.1292 0.2151)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (999, LEFT('river', 150), -0.7879, 37.2685, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.2685 -0.7879)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1000, LEFT('river', 150), -0.8739, 37.5913, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.5913 -0.8739)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1001, LEFT('river', 150), -0.4742, 37.9132, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.9132 -0.4742)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1002, LEFT('river', 150), -0.1516, 38.1968, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.1968 -0.1516)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1003, LEFT('river', 150), -0.0766, 38.4146, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.4146 -0.0766)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1004, LEFT('river', 150), -0.0546, 38.3108, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.3108 -0.0546)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1005, LEFT('river', 150), -0.1453, 39.3256, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.3256 -0.1453)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1006, LEFT('river', 150), -0.4636, 39.6366, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.6366 -0.4636)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1007, LEFT('river', 150), -0.3025, 39.5506, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.5506 -0.3025)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1008, LEFT('river', 150), -0.0939, 39.105, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.105 -0.0939)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1009, LEFT('river', 150), -0.7073, 39.8057, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.8057 -0.7073)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1010, LEFT('river', 150), -1.0996, 39.9379, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.9379 -1.0996)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1011, LEFT('river', 150), -2.2887, 40.1266, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (40.1266 -2.2887)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1012, LEFT('river', 150), -1.8511, 40.1153, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (40.1153 -1.8511)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1013, LEFT('river', 150), -1.4945, 40.0393, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (40.0393 -1.4945)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1014, LEFT('river', 150), -2.4098, 40.3518, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (40.3518 -2.4098)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1015, LEFT('river', 150), -0.46417, 39.63632, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.63632 -0.46417)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1016, LEFT('river', 150), -3.14425, 40.10839, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (40.10839 -3.14425)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1017, LEFT('river', 150), -2.26872, 40.11701, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (40.11701 -2.26872)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1018, LEFT('river', 150), -1.07758, 37.25253, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.25253 -1.07758)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1019, LEFT('river', 150), -1.23347, 37.46603, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.46603 -1.23347)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1020, LEFT('river', 150), -1.41558, 37.64694, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.64694 -1.41558)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1021, LEFT('river', 150), -1.61461, 37.78531, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.78531 -1.61461)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1022, LEFT('river', 150), -1.90597, 37.90669, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.90669 -1.90597)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1023, LEFT('river', 150), -2.20114, 38.05733, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.05733 -2.20114)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1024, LEFT('river', 150), -2.98419, 38.02314, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.02314 -2.98419)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1025, LEFT('river', 150), -3.01547, 38.02883, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.02883 -3.01547)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1026, LEFT('river', 150), -3.02564, 38.04075, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.04075 -3.02564)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1027, LEFT('river', 150), -3.04628, 38.10381, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.10381 -3.04628)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1028, LEFT('river', 150), -2.66967, 38.38206, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.38206 -2.66967)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1029, LEFT('river', 150), -2.99456, 38.46081, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.46081 -2.99456)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1030, LEFT('river', 150), -2.94247, 38.48897, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.48897 -2.94247)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1031, LEFT('river', 150), -3.04031, 38.69614, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.69614 -3.04031)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1032, LEFT('river', 150), -3.04639, 38.9055, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.9055 -3.04639)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1033, LEFT('river', 150), -3.07628, 39.16986, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.16986 -3.07628)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1034, LEFT('river', 150), -3.06889, 39.29439, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.29439 -3.06889)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1035, LEFT('river', 150), -3.10619, 39.55394, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.55394 -3.10619)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1036, LEFT('river', 150), -3.14292, 39.85181, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (39.85181 -3.14292)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1037, LEFT('river', 150), -1.56706, 37.54878, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.54878 -1.56706)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1038, LEFT('river', 150), -1.77636, 37.61669, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.61669 -1.77636)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1039, LEFT('river', 150), -1.77558, 37.72039, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.72039 -1.77558)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1040, LEFT('river', 150), -1.67083, 37.66153, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.66153 -1.67083)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1041, LEFT('river', 150), -3.3911, 38.5788, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (38.5788 -3.3911)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1042, LEFT('river', 150), -2.08517, 37.77072, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (37.77072 -2.08517)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1043, LEFT('river', 150), 3.16667, 11.85, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (11.85 3.16667)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1044, LEFT('river', 150), 3.28333, 11.78333, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (11.78333 3.28333)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1045, LEFT('river', 150), 3.43333, 11.28333, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (11.28333 3.43333)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1046, LEFT('river', 150), 3.31667, 11.48333, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (11.48333 3.31667)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1047, LEFT('river', 150), 3.9, 12.53333, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (12.53333 3.9)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1048, LEFT('river', 150), -1.87755, -55.56843, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.56843 -1.87755)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1049, LEFT('river', 150), -2.24947, -54.78872, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.78872 -2.24947)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1050, LEFT('river', 150), -2.42473, -54.46258, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.46258 -2.42473)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1051, LEFT('river', 150), -2.24685, -54.06152, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.06152 -2.24685)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1052, LEFT('river', 150), -1.933, -53.79318, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-53.79318 -1.933)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1053, LEFT('river', 150), -1.87192, -53.54055, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-53.54055 -1.87192)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1054, LEFT('river', 150), -1.75962, -53.09298, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-53.09298 -1.75962)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1055, LEFT('river', 150), -1.62452, -52.88482, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-52.88482 -1.62452)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1056, LEFT('river', 150), -1.58095, -52.54592, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-52.54592 -1.58095)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1057, LEFT('river', 150), -1.48687, -51.79165, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-51.79165 -1.48687)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1058, LEFT('river', 150), -1.33282, -51.8911, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-51.8911 -1.33282)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1059, LEFT('river', 150), -0.59963, -51.54387, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-51.54387 -0.59963)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1060, LEFT('river', 150), -0.11607, -51.23892, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-51.23892 -0.11607)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1061, LEFT('river', 150), -2.40183, -54.83582, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.83582 -2.40183)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1062, LEFT('river', 150), -2.54645, -55.04743, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.04743 -2.54645)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1063, LEFT('river', 150), -2.48987, -55.01252, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.01252 -2.48987)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1064, LEFT('river', 150), -1.81408, -52.22758, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-52.22758 -1.81408)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1065, LEFT('river', 150), -2.26118, -55.13673, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.13673 -2.26118)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1066, LEFT('river', 150), -2.26025, -55.76935, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.76935 -2.26025)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1067, LEFT('river', 150), -1.13933, -51.98155, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-51.98155 -1.13933)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1068, LEFT('river', 150), -0.28077, -51.48117, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-51.48117 -0.28077)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1069, LEFT('river', 150), -1.91348, -55.58462, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.58462 -1.91348)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1070, LEFT('river', 150), -2.22637, -55.27473, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.27473 -2.22637)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1071, LEFT('river', 150), -2.25862, -55.40277, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.40277 -2.25862)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1072, LEFT('river', 150), -2.23288, -55.47665, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.47665 -2.23288)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1073, LEFT('river', 150), -2.21038, -55.34187, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.34187 -2.21038)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1074, LEFT('river', 150), -2.2883, -55.35533, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.35533 -2.2883)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1075, LEFT('river', 150), -2.17063, -54.93262, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.93262 -2.17063)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1076, LEFT('river', 150), -3.30493, -60.1742, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.1742 -3.30493)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1077, LEFT('river', 150), -3.32687, -60.5523, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.5523 -3.32687)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1078, LEFT('river', 150), -3.07593, -60.26462, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.26462 -3.07593)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1079, LEFT('river', 150), -3.11915, -60.438, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.438 -3.11915)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1080, LEFT('river', 150), -3.1288, -60.92015, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.92015 -3.1288)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1081, LEFT('river', 150), -3.18195, -60.78375, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.78375 -3.18195)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1082, LEFT('river', 150), -3.31267, -60.81535, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.81535 -3.31267)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1083, LEFT('river', 150), -3.35165, -60.82795, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.82795 -3.35165)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1084, LEFT('river', 150), -3.29097, -60.74382, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.74382 -3.29097)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1085, LEFT('river', 150), -3.39663, -60.2873, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.2873 -3.39663)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1086, LEFT('river', 150), -3.38935, -60.31862, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.31862 -3.38935)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1087, LEFT('river', 150), -3.38397, -60.28595, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.28595 -3.38397)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1088, LEFT('river', 150), -3.39475, -60.31215, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.31215 -3.39475)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1089, LEFT('river', 150), -3.15952, -59.4169, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-59.4169 -3.15952)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1090, LEFT('river', 150), -3.16335, -58.43252, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.43252 -3.16335)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1091, LEFT('river', 150), -2.40555, -57.55097, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-57.55097 -2.40555)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1092, LEFT('river', 150), -2.53278, -57.01655, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-57.01655 -2.53278)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1093, LEFT('river', 150), -2.16545, -56.14787, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-56.14787 -2.16545)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1094, LEFT('river', 150), -1.91328, -55.55533, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.55533 -1.91328)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1095, LEFT('river', 150), -3.07015, -60.2621, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.2621 -3.07015)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1096, LEFT('river', 150), -3.40993, -58.78958, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.78958 -3.40993)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1097, LEFT('river', 150), -2.83812, -58.18635, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.18635 -2.83812)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1098, LEFT('river', 150), -3.37558, -60.26953, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.26953 -3.37558)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1099, LEFT('river', 150), -3.38663, -60.29113, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.29113 -3.38663)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1100, LEFT('river', 150), -2.79127, -58.10597, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.10597 -2.79127)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1101, LEFT('river', 150), -2.25062, -55.35125, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.35125 -2.25062)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1102, LEFT('river', 150), -2.19852, -55.28797, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.28797 -2.19852)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1103, LEFT('river', 150), -3.33108, -60.5434, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.5434 -3.33108)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1104, LEFT('river', 150), -3.11867, -59.55692, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-59.55692 -3.11867)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1105, LEFT('river', 150), -3.24233, -58.97553, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.97553 -3.24233)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1106, LEFT('river', 150), -3.17443, -58.40908, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.40908 -3.17443)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1107, LEFT('river', 150), -2.69203, -57.70525, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-57.70525 -2.69203)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1108, LEFT('river', 150), -2.54228, -57.02672, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-57.02672 -2.54228)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1109, LEFT('river', 150), -1.95085, -55.49037, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.49037 -1.95085)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1110, LEFT('river', 150), -3.07265, -60.26265, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.26265 -3.07265)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1111, LEFT('river', 150), -3.40897, -58.78522, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.78522 -3.40897)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1112, LEFT('river', 150), -2.8653, -58.32637, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.32637 -2.8653)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1113, LEFT('river', 150), -2.52622, -55.02915, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.02915 -2.52622)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1114, LEFT('river', 150), -3.18952, -60.7755, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.7755 -3.18952)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1115, LEFT('river', 150), -3.46698, -60.28877, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.28877 -3.46698)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1116, LEFT('river', 150), -3.36657, -60.21172, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.21172 -3.36657)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1117, LEFT('river', 150), -3.22977, -58.30652, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.30652 -3.22977)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1118, LEFT('river', 150), -2.24883, -55.07465, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.07465 -2.24883)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1119, LEFT('river', 150), -3.29843, -60.78005, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.78005 -3.29843)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1120, LEFT('river', 150), -3.29897, -60.82413, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.82413 -3.29897)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1121, LEFT('river', 150), -3.29255, -60.77902, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.77902 -3.29255)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1122, LEFT('river', 150), -3.29332, -60.77947, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.77947 -3.29332)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1123, LEFT('river', 150), -3.36273, -60.30365, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.30365 -3.36273)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1124, LEFT('river', 150), -3.36727, -60.24583, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.24583 -3.36727)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1125, LEFT('river', 150), -3.38888, -60.31662, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.31662 -3.38888)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1126, LEFT('river', 150), -3.37808, -60.2695, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.2695 -3.37808)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1127, LEFT('river', 150), -3.39952, -60.28323, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.28323 -3.39952)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1128, LEFT('river', 150), -3.24217, -58.32515, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.32515 -3.24217)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1129, LEFT('river', 150), -3.3523, -58.35418, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.35418 -3.3523)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1130, LEFT('river', 150), -2.94907, -58.25363, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.25363 -2.94907)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1131, LEFT('river', 150), -3.0316, -58.32438, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.32438 -3.0316)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1132, LEFT('river', 150), -2.98568, -58.257, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.257 -2.98568)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1133, LEFT('river', 150), -2.1262, -55.64383, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.64383 -2.1262)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1134, LEFT('river', 150), -3.32545, -60.55282, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.55282 -3.32545)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1135, LEFT('river', 150), -3.12527, -59.57057, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-59.57057 -3.12527)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1136, LEFT('river', 150), -3.311, -58.86205, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.86205 -3.311)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1137, LEFT('river', 150), -3.16143, -58.37775, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.37775 -3.16143)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1138, LEFT('river', 150), -2.5096, -57.29772, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-57.29772 -2.5096)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1139, LEFT('river', 150), -2.38317, -56.44372, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-56.44372 -2.38317)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1140, LEFT('river', 150), -1.94682, -55.49902, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.49902 -1.94682)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1141, LEFT('river', 150), -3.07617, -60.26347, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.26347 -3.07617)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1142, LEFT('river', 150), -2.85898, -58.31178, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.31178 -2.85898)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1143, LEFT('river', 150), -2.4578, -54.98833, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-54.98833 -2.4578)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1144, LEFT('river', 150), -3.21833, -60.7365, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.7365 -3.21833)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1145, LEFT('river', 150), -3.36773, -60.21345, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.21345 -3.36773)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1146, LEFT('river', 150), -3.23007, -58.3118, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.3118 -3.23007)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1147, LEFT('river', 150), -2.2614, -55.67158, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.67158 -2.2614)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1148, LEFT('river', 150), -3.30618, -60.85182, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.85182 -3.30618)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1149, LEFT('river', 150), -3.38377, -60.32327, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-60.32327 -3.38377)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1150, LEFT('river', 150), -3.35083, -58.44512, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.44512 -3.35083)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1151, LEFT('river', 150), -3.00887, -58.29262, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.29262 -3.00887)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1152, LEFT('river', 150), -2.92515, -58.26508, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-58.26508 -2.92515)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1153, LEFT('river', 150), -2.26472, -55.46837, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-55.46837 -2.26472)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1154, LEFT('river', 150), -3.40708, 17.32662, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.32662 -3.40708)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1155, LEFT('river', 150), -3.38783, 17.4071, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.4071 -3.38783)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1156, LEFT('river', 150), -3.25358, 17.37779, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.37779 -3.25358)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1157, LEFT('river', 150), -3.2333, 17.22909, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.22909 -3.2333)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1158, LEFT('river', 150), -3.1764, 17.32298, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.32298 -3.1764)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1159, LEFT('river', 150), -3.22042, 17.43124, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.43124 -3.22042)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1160, LEFT('river', 150), -3.26218, 17.46914, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.46914 -3.26218)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1161, LEFT('river', 150), -3.25787, 17.51245, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.51245 -3.25787)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1162, LEFT('river', 150), -3.27481, 17.53867, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.53867 -3.27481)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1163, LEFT('river', 150), -3.15759, 17.12306, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.12306 -3.15759)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1164, LEFT('river', 150), -3.13071, 17.15451, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.15451 -3.13071)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1165, LEFT('river', 150), -3.31024, 17.60087, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.60087 -3.31024)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1166, LEFT('river', 150), -3.37136, 17.76766, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.76766 -3.37136)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1167, LEFT('river', 150), -3.39553, 18.00808, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.00808 -3.39553)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1168, LEFT('river', 150), -3.39502, 18.07142, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.07142 -3.39502)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1169, LEFT('river', 150), -3.46538, 18.16674, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.16674 -3.46538)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1170, LEFT('river', 150), -3.38862, 18.24314, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.24314 -3.38862)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1171, LEFT('river', 150), -3.40261, 18.24947, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.24947 -3.40261)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1172, LEFT('river', 150), -3.52121, 18.36442, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.36442 -3.52121)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1173, LEFT('river', 150), -3.625, 18.6586, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.6586 -3.625)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1174, LEFT('river', 150), -3.71521, 18.92626, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.92626 -3.71521)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1175, LEFT('river', 150), -3.72659, 18.96668, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.96668 -3.72659)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1176, LEFT('river', 150), -3.85985, 19.2611, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.2611 -3.85985)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1177, LEFT('river', 150), -3.96084, 19.3966, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.3966 -3.96084)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1178, LEFT('river', 150), -4.03104, 19.54771, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.54771 -4.03104)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1179, LEFT('river', 150), -4.07059, 19.74795, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.74795 -4.07059)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1180, LEFT('river', 150), -4.11932, 19.77624, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.77624 -4.11932)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1181, LEFT('river', 150), -4.15057, 19.86921, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.86921 -4.15057)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1182, LEFT('river', 150), -4.20231, 19.9848, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.9848 -4.20231)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1183, LEFT('river', 150), -4.30081, 20.02896, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.02896 -4.30081)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1184, LEFT('river', 150), -4.2915, 20.12124, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.12124 -4.2915)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1185, LEFT('river', 150), -4.3944, 20.32806, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.32806 -4.3944)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1186, LEFT('river', 150), -4.36377, 20.57818, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.57818 -4.36377)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1187, LEFT('river', 150), -4.27528, 20.44151, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.44151 -4.27528)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1188, LEFT('river', 150), -4.30676, 20.3751, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.3751 -4.30676)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1189, LEFT('river', 150), -4.31778, 20.37558, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (20.37558 -4.31778)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1190, LEFT('river', 150), -4.18301, 19.87594, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (19.87594 -4.18301)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1191, LEFT('river', 150), -3.37062, 18.03562, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.03562 -3.37062)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1192, LEFT('river', 150), -2.99357, 17.05589, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.05589 -2.99357)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1193, LEFT('river', 150), -2.89283, 17.32695, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.32695 -2.89283)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1194, LEFT('river', 150), -2.83864, 17.49164, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.49164 -2.83864)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1195, LEFT('river', 150), -2.74453, 17.60495, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.60495 -2.74453)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1196, LEFT('river', 150), -2.71138, 17.70522, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.70522 -2.71138)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1197, LEFT('river', 150), -2.66661, 18.2354, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.2354 -2.66661)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1198, LEFT('river', 150), -2.76931, 18.20527, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.20527 -2.76931)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1199, LEFT('river', 150), -2.72521, 18.12953, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (18.12953 -2.72521)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1200, LEFT('river', 150), -2.76992, 17.89391, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (17.89391 -2.76992)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1201, LEFT('river', 150), -3.04832, 16.84085, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.84085 -3.04832)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1202, LEFT('river', 150), -3.0296, 16.77812, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.77812 -3.0296)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1203, LEFT('river', 150), -3.0562, 16.49571, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.49571 -3.0562)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1204, LEFT('river', 150), -3.16513, 16.21027, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.21027 -3.16513)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1205, LEFT('river', 150), -3.42039, 16.16509, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.16509 -3.42039)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1206, LEFT('river', 150), -3.5627, 16.09922, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (16.09922 -3.5627)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1207, LEFT('river', 150), -3.75714, 15.98902, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.98902 -3.75714)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1208, LEFT('river', 150), -3.82347, 15.9437, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.9437 -3.82347)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1209, LEFT('river', 150), -3.9529, 15.91458, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.91458 -3.9529)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1210, LEFT('river', 150), -4.02029, 15.61955, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.61955 -4.02029)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1211, LEFT('river', 150), -4.32432, 15.39172, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (15.39172 -4.32432)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1212, LEFT('river channel', 150), 50.4818, 5.591, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.591 50.4818)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1213, LEFT('river channel', 150), 50.386, 6.0104, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (6.0104 50.386)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1214, LEFT('river channel', 150), 50.3918, 5.932, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.932 50.3918)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1215, LEFT('river channel', 150), 50.7153, 5.7462, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.7462 50.7153)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1216, LEFT('river channel', 150), 50.4051, 4.5871, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.5871 50.4051)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1217, LEFT('river channel', 150), 50.1588, 5.06, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.06 50.1588)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1218, LEFT('river channel', 150), 50.3381, 4.9069, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.9069 50.3381)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1219, LEFT('river channel', 150), 50.0425, 4.2842, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.2842 50.0425)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1220, LEFT('river channel', 150), 50.3673, 4.3965, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.3965 50.3673)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1221, LEFT('river channel', 150), 50.1754, 4.4085, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.4085 50.1754)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1222, LEFT('river channel', 150), 50.0779, 4.5514, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.5514 50.0779)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1223, LEFT('river channel', 150), 50.7346, 5.3939, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.3939 50.7346)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1224, LEFT('river channel', 150), 50.7505, 5.9409, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.9409 50.7505)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1225, LEFT('river channel', 150), 50.2991, 4.1731, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.1731 50.2991)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1226, LEFT('river channel', 150), 50.5536, 5.8047, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.8047 50.5536)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1227, LEFT('river channel', 150), 50.4633, 5.2762, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.2762 50.4633)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1228, LEFT('river channel', 150), 50.5091, 5.2382, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.2382 50.5091)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1229, LEFT('river channel', 150), 50.2191, 4.9458, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.9458 50.2191)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1230, LEFT('river channel', 150), 49.9891, 5.3194, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.3194 49.9891)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1231, LEFT('river channel', 150), 50.1393, 5.1641, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.1641 50.1393)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1232, LEFT('river channel', 150), 49.972, 5.3911, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.3911 49.972)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1233, LEFT('river channel', 150), 50.4096, 5.7692, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.7692 50.4096)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1234, LEFT('river channel', 150), 50.1151, 5.2975, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.2975 50.1151)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1235, LEFT('river channel', 150), 50.6269, 5.0442, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.0442 50.6269)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1236, LEFT('river channel', 150), 50.551, 5.1841, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.1841 50.551)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1237, LEFT('river channel', 150), 50.2157, 4.8269, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.8269 50.2157)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1238, LEFT('river channel', 150), 50.4939, 5.0958, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.0958 50.4939)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1239, LEFT('river channel', 150), 50.7373, 5.6903, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.6903 50.7373)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1240, LEFT('river channel', 150), 50.5807, 5.4056, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.4056 50.5807)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1241, LEFT('river channel', 150), 50.6209, 5.5796, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.5796 50.6209)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1242, LEFT('river channel', 150), 50.398, 4.882, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.882 50.398)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1243, LEFT('river channel', 150), 50.4222, 5.5157, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.5157 50.4222)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1244, LEFT('river channel', 150), 50.4562, 5.5661, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.5661 50.4562)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1245, LEFT('river channel', 150), 50.2609, 5.4668, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.4668 50.2609)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1246, LEFT('river channel', 150), 50.6094, 5.6125, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.6125 50.6094)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1247, LEFT('river channel', 150), 50.1068, 5.6462, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.6462 50.1068)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1248, LEFT('river channel', 150), 50.1367, 5.7221, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.7221 50.1367)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1249, LEFT('river channel', 150), 49.8109, 5.1674, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.1674 49.8109)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1250, LEFT('river channel', 150), 50.3638, 5.8862, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.8862 50.3638)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1251, LEFT('river channel', 150), 50.3047, 4.1175, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.1175 50.3047)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1252, LEFT('river channel', 150), 50.4643, 4.8559, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.8559 50.4643)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1253, LEFT('river channel', 150), 50.4079, 4.3951, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.3951 50.4079)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1254, LEFT('river channel', 150), 50.4194, 4.5467, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.5467 50.4194)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1255, LEFT('river channel', 150), 50.4496, 4.7037, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.7037 50.4496)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1256, LEFT('river channel', 150), 50.4581, 5.0014, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.0014 50.4581)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1257, LEFT('river channel', 150), 49.7104, 5.3254, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.3254 49.7104)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1258, LEFT('river channel', 150), 49.8643, 4.8841, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.8841 49.8643)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1259, LEFT('river channel', 150), 50.1629, 5.1156, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.1156 50.1629)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1260, LEFT('river channel', 150), 50.6001, 5.6332, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.6332 50.6001)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1261, LEFT('river channel', 150), 50.0935, 4.691, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.691 50.0935)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1262, LEFT('river channel', 150), 50.3213, 4.9436, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.9436 50.3213)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1263, LEFT('river channel', 150), 50.3251, 5.0657, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.0657 50.3251)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1264, LEFT('river channel', 150), 50.3261, 5.0375, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.0375 50.3261)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1265, LEFT('river channel', 150), 50.3636, 4.847, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.847 50.3636)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1266, LEFT('river channel', 150), 50.0048, 4.4253, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.4253 50.0048)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1267, LEFT('river channel', 150), 50.412, 5.9534, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.9534 50.412)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1268, LEFT('river channel', 150), 50.6861, 5.2311, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.2311 50.6861)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1269, LEFT('river channel', 150), 49.9938, 5.1671, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.1671 49.9938)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1270, LEFT('river channel', 150), 49.918, 5.2861, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.2861 49.918)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1271, LEFT('river channel', 150), 50.1262, 5.185, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.185 50.1262)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1272, LEFT('river channel', 150), 50.1736, 5.0467, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.0467 50.1736)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1273, LEFT('river channel', 150), 50.1616, 5.261, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.261 50.1616)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1274, LEFT('river channel', 150), 50.5707, 5.1661, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.1661 50.5707)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1275, LEFT('river channel', 150), 50.3766, 5.5201, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.5201 50.3766)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1276, LEFT('river channel', 150), 49.9957, 5.0661, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.0661 49.9957)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1277, LEFT('river channel', 150), 50.5888, 5.4126, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.4126 50.5888)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1278, LEFT('river channel', 150), 49.7208, 5.5943, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.5943 49.7208)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1279, LEFT('river channel', 150), 50.0375, 4.5019, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (4.5019 50.0375)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1280, LEFT('river channel', 150), 49.8076, 5.1651, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.1651 49.8076)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1281, LEFT('river channel', 150), 49.5589, 5.5316, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.5316 49.5589)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1282, LEFT('river channel', 150), 50.3871, 5.9917, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.9917 50.3871)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1283, LEFT('river channel', 150), 50.532, 5.5677, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.5677 50.532)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1284, LEFT('river channel', 150), 50.7168, 5.3282, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.3282 50.7168)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1285, LEFT('river channel', 150), 50.5818, 5.5718, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.5718 50.5818)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1286, LEFT('river channel', 150), 50.6389, 5.5774, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (5.5774 50.6389)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1287, LEFT('stream', 150), 44.58206, -106.43789, cast(coalesce(nullif('1211.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.43789 44.58206)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1288, LEFT('stream', 150), 44.565126, -106.5258352, cast(coalesce(nullif('1235.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.5258352 44.565126)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1289, LEFT('stream', 150), 44.544573, -106.537443, cast(coalesce(nullif('1245.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.537443 44.544573)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1290, LEFT('stream', 150), 44.422526, -106.594035, cast(coalesce(nullif('1314.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.594035 44.422526)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1291, LEFT('stream', 150), 44.362499, -106.65422, cast(coalesce(nullif('1366.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.65422 44.362499)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1292, LEFT('stream', 150), 44.343529, -106.70578, cast(coalesce(nullif('1416.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.70578 44.343529)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1293, LEFT('stream', 150), 44.329758, -106.7234127, cast(coalesce(nullif('1453.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.7234127 44.329758)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1294, LEFT('stream', 150), 44.33092, -106.7925189, cast(coalesce(nullif('1632.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.7925189 44.33092)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1295, LEFT('stream', 150), 44.321944, -106.831667, cast(coalesce(nullif('1747.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.831667 44.321944)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1296, LEFT('stream', 150), 44.310162, -106.8607744, cast(coalesce(nullif('1976.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.8607744 44.310162)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1297, LEFT('stream', 150), 44.319532, -106.9137139, cast(coalesce(nullif('2127.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.9137139 44.319532)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1298, LEFT('stream', 150), 44.318982, -106.9425399, cast(coalesce(nullif('2206.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.9425399 44.318982)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1299, LEFT('stream', 150), 44.325646, -106.9857629, cast(coalesce(nullif('2398.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.9857629 44.325646)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1300, LEFT('stream', 150), 44.337557, -106.9999829, cast(coalesce(nullif('2573.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-106.9999829 44.337557)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1301, LEFT('stream', 150), 44.341382, -107.0059299, cast(coalesce(nullif('2616.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.0059299 44.341382)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1302, LEFT('stream', 150), 44.345047, -107.0206609, cast(coalesce(nullif('2642.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.0206609 44.345047)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1303, LEFT('stream', 150), 44.342792, -107.0420749, cast(coalesce(nullif('2716.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.0420749 44.342792)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1304, LEFT('stream', 150), 44.337781, -107.0521469, cast(coalesce(nullif('2760.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.0521469 44.337781)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1305, LEFT('stream', 150), 44.335752, -107.0607349, cast(coalesce(nullif('2781.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.0607349 44.335752)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1306, LEFT('stream', 150), 44.335667, -107.0859499, cast(coalesce(nullif('2818.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.0859499 44.335667)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1307, LEFT('stream', 150), 44.336047, -107.1002719, cast(coalesce(nullif('2842.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.1002719 44.336047)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1308, LEFT('stream', 150), 44.338731, -107.1002859, cast(coalesce(nullif('2844.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.1002859 44.338731)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1309, LEFT('stream', 150), 44.338152, -107.1073309, cast(coalesce(nullif('2870.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.1073309 44.338152)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1310, LEFT('stream', 150), 44.33658, -107.1253579, cast(coalesce(nullif('2900.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.1253579 44.33658)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1311, LEFT('stream', 150), 44.339159, -107.1364139, cast(coalesce(nullif('2929.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.1364139 44.339159)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1312, LEFT('stream', 150), 44.339439, -107.1361789, cast(coalesce(nullif('2929.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.1361789 44.339439)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1313, LEFT('stream', 150), 44.340182, -107.1518468, cast(coalesce(nullif('3035.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.1518468 44.340182)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1314, LEFT('stream', 150), 44.343069, -107.1603368, cast(coalesce(nullif('3133.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.1603368 44.343069)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1315, LEFT('stream', 150), 44.345339, -107.1716598, cast(coalesce(nullif('3261.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.1716598 44.345339)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1316, LEFT('stream', 150), 44.347443, -107.1787008, cast(coalesce(nullif('3311.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-107.1787008 44.347443)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1317, LEFT('river', 150), 26.58762, 101.69716, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (101.69716 26.58762)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1318, LEFT('river', 150), 26.645916, 101.84102, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (101.84102 26.645916)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1319, LEFT('river', 150), 28.6236, 104.146002, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (104.146002 28.6236)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1320, LEFT('river', 150), 28.762006, 104.631025, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (104.631025 28.762006)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1321, LEFT('river', 150), 29.59, 103.752057, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (103.752057 29.59)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1322, LEFT('river', 150), 29.605003, 103.771049, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (103.771049 29.605003)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1323, LEFT('river', 150), 28.884036, 105.429058, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (105.429058 28.884036)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1324, LEFT('river', 150), 30.010466, 106.35168, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (106.35168 30.010466)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1325, LEFT('river', 150), 29.620357, 106.592482, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (106.592482 29.620357)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1326, LEFT('river', 150), 29.322226, 107.752192, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (107.752192 29.322226)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1327, LEFT('river', 150), 30.810065, 108.392033, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (108.392033 30.810065)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1328, LEFT('river', 150), 30.634043, 111.338097, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (111.338097 30.634043)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1329, LEFT('river', 150), 28.191254, 112.936063, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (112.936063 28.191254)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1330, LEFT('river', 150), 31.186099, 112.544082, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (112.544082 31.186099)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1331, LEFT('river', 150), 30.561076, 114.271048, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (114.271048 30.561076)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1332, LEFT('river', 150), 28.674002, 115.859066, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (115.859066 28.674002)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1333, LEFT('river', 150), 30.773098, 117.632044, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (117.632044 30.773098)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1334, LEFT('stream', 150), 52.1, -75.85, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-75.84999999999999 52.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1335, LEFT('river', 150), 52.1, -75.85, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-75.84999999999999 52.1)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1336, LEFT('river, Zambezi mainstem', 150), -11.122, 24.1986, cast(coalesce(nullif('1223.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.1986 -11.122)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1337, LEFT('river, Zambezi mainstem', 150), -13.1077, 22.689, cast(coalesce(nullif('1043.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.689 -13.1077)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1338, LEFT('river, Zambezi mainstem', 150), -14.3372, 23.2359, cast(coalesce(nullif('1028.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.2359 -14.3372)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1339, LEFT('river, Zambezi mainstem', 150), -16.2447, 23.2388, cast(coalesce(nullif('1005.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.2388 -16.2447)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1340, LEFT('river, Zambezi mainstem', 150), -17.4666, 24.247, cast(coalesce(nullif('939.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.247 -17.4666)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1341, LEFT('river, Zambezi mainstem', 150), -17.7985, 25.2807, cast(coalesce(nullif('924.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.2807 -17.7985)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1342, LEFT('river, Zambezi mainstem', 150), -17.8874, 25.8426, cast(coalesce(nullif('889.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.8426 -17.8874)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1343, LEFT('river, Zambezi mainstem', 150), -17.9311, 25.8596, cast(coalesce(nullif('773.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.8596 -17.9311)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1344, LEFT('river, Zambezi mainstem', 150), -16.0162, 28.8798, cast(coalesce(nullif('371.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.8798 -16.0162)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1345, LEFT('river, Zambezi mainstem', 150), -15.6355, 30.4034, cast(coalesce(nullif('327.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.4034 -15.6355)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1346, LEFT('river, Zambezi mainstem', 150), -16.1396, 33.5408, cast(coalesce(nullif('124.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (33.5408 -16.1396)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1347, LEFT('river, Zambezi mainstem', 150), -17.4594, 35.0592, cast(coalesce(nullif('40.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (35.0592 -17.4594)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1348, LEFT('river, Zambezi mainstem', 150), -17.8059, 35.3995, cast(coalesce(nullif('25.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (35.3995 -17.8059)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1349, LEFT('river, Zambezi mainstem', 150), -18.5792, 36.2442, cast(coalesce(nullif('2.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.2442 -18.5792)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1350, LEFT('river, Zambezi mainstem', 150), -18.5673, 36.4453, cast(coalesce(nullif('0.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (36.4453 -18.5673)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1351, LEFT('river, tributary', 150), -12.4643, 27.8508, cast(coalesce(nullif('1258.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.8508 -12.4643)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1352, LEFT('river, tributary', 150), -12.645, 28.1645, cast(coalesce(nullif('1190.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.1645 -12.645)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1353, LEFT('river, tributary', 150), -13.6423, 27.7616, cast(coalesce(nullif('1129.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.7616 -13.6423)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1354, LEFT('river, tributary', 150), -14.5625, 26.4577, cast(coalesce(nullif('1100.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.4577 -14.5625)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1355, LEFT('river, tributary', 150), -14.9449, 25.913, cast(coalesce(nullif('1075.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.913 -14.9449)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1356, LEFT('river, tributary', 150), -15.7641, 26.0304, cast(coalesce(nullif('998.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.0304 -15.7641)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1357, LEFT('river, tributary', 150), -15.7465, 27.8296, cast(coalesce(nullif('982.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.8296 -15.7465)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1358, LEFT('river, tributary', 150), -15.8369, 28.3282, cast(coalesce(nullif('979.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.3282 -15.8369)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1359, LEFT('river, tributary', 150), -15.9462, 28.872, cast(coalesce(nullif('375.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.872 -15.9462)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1360, LEFT('river, tributary', 150), -11.8886, 25.2505, cast(coalesce(nullif('1317.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.2505 -11.8886)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1361, LEFT('river, tributary', 150), -13.0979, 31.786, cast(coalesce(nullif('529.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (31.786 -13.0979)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1362, LEFT('river, tributary', 150), -15.0055, 30.2155, cast(coalesce(nullif('369.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.2155 -15.0055)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1363, LEFT('river, tributary', 150), -15.604, 30.4103, cast(coalesce(nullif('327.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.4103 -15.604)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1364, LEFT('river, tributary', 150), -13.932, 29.1316, cast(coalesce(nullif('1064.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.1316 -13.932)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1365, LEFT('river, tributary', 150), -14.7943, 29.6292, cast(coalesce(nullif('440.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (29.6292 -14.7943)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1366, LEFT('river, tributary', 150), -12.2604, 26.7923, cast(coalesce(nullif('1271.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.7923 -12.2604)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1367, LEFT('river, tributary', 150), -13.9839, 26.3469, cast(coalesce(nullif('1121.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.3469 -13.9839)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1368, LEFT('river, tributary', 150), -17.4584, 35.3388, cast(coalesce(nullif('30.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (35.3388 -17.4584)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1369, LEFT('Reservoirs', 150), -17.279, 27.5348, cast(coalesce(nullif('488.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.5348 -17.279)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1370, LEFT('Reservoirs', 150), -16.5543, 28.6837, cast(coalesce(nullif('488.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.6837 -16.5543)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1371, LEFT('Reservoirs', 150), -15.5874, 32.3754, cast(coalesce(nullif('317.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (32.3754 -15.5874)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1372, LEFT('Reservoirs', 150), -15.6103, 26.0147, cast(coalesce(nullif('1030.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.0147 -15.6103)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1373, LEFT('Reservoirs', 150), -15.7602, 25.9888, cast(coalesce(nullif('1030.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.9888 -15.7602)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1374, LEFT('Reservoirs', 150), -15.8125, 25.9389, cast(coalesce(nullif('1030.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.9389 -15.8125)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1375, LEFT('river, tributary', 150), -14.0387, 23.629, cast(coalesce(nullif('1045.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.629 -14.0387)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1376, LEFT('river, tributary', 150), -10.252, 33.0221, cast(coalesce(nullif('778.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (33.0221 -10.252)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1377, LEFT('river, tributary', 150), -16.5435, 33.3806, cast(coalesce(nullif('169.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (33.3806 -16.5435)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1378, LEFT('Reservoirs', 150), -15.5567, 32.6337, cast(coalesce(nullif('317.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (32.6337 -15.5567)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1379, LEFT('river, Zambezi mainstem', 150), -11.3503, 24.3286, cast(coalesce(nullif('1442.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.3286 -11.3503)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1380, LEFT('river, Zambezi mainstem', 150), -13.0974, 22.6854, cast(coalesce(nullif('1043.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.6854 -13.0974)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1381, LEFT('river, Zambezi mainstem', 150), -14.3838, 23.2362, cast(coalesce(nullif('1028.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.2362 -14.3838)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1382, LEFT('river, Zambezi mainstem', 150), -15.206, 22.9223, cast(coalesce(nullif('1014.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (22.9223 -15.206)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1383, LEFT('river, Zambezi mainstem', 150), -16.13, 23.2883, cast(coalesce(nullif('1005.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (23.2883 -16.13)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1384, LEFT('river, Zambezi mainstem', 150), -17.4667, 24.2469, cast(coalesce(nullif('939.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (24.2469 -17.4667)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1385, LEFT('river, Zambezi mainstem', 150), -16.5043, 28.7907, cast(coalesce(nullif('400.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.7907 -16.5043)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1386, LEFT('river, Zambezi mainstem', 150), -15.985, 28.8808, cast(coalesce(nullif('371.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.8808 -15.985)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1387, LEFT('river, Zambezi mainstem', 150), -15.6244, 30.4135, cast(coalesce(nullif('327.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (30.4135 -15.6244)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1388, LEFT('river, tributary', 150), -12.4643, 27.8507, cast(coalesce(nullif('1258.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.8507 -12.4643)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1389, LEFT('river, tributary', 150), -14.5624, 26.4576, cast(coalesce(nullif('1100.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.4576 -14.5624)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1390, LEFT('river, tributary', 150), -14.9778, 25.9926, cast(coalesce(nullif('1075.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.9926 -14.9778)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1391, LEFT('river, tributary', 150), -15.7638, 26.0303, cast(coalesce(nullif('998.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (26.0303 -15.7638)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1392, LEFT('river, tributary', 150), -15.7479, 27.8283, cast(coalesce(nullif('982.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (27.8283 -15.7479)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1393, LEFT('river, tributary', 150), -15.8365, 28.2376, cast(coalesce(nullif('979.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.2376 -15.8365)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1394, LEFT('river, tributary', 150), -15.9512, 28.8602, cast(coalesce(nullif('375.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.8602 -15.9512)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1395, LEFT('Reservoirs', 150), -16.5755, 28.6887, cast(coalesce(nullif('488.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (28.6887 -16.5755)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1396, LEFT('Reservoirs', 150), -15.7741, 25.9692, cast(coalesce(nullif('1030.0', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (25.9692 -15.7741)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1397, LEFT('lake', 150), 30.54814, 114.3628, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (114.3628 30.54814)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1398, LEFT('lake', 150), 30.55982, 114.3869, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (114.3869 30.55982)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1399, LEFT('lake', 150), 30.57906, 114.4047, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (114.4047 30.57906)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1400, LEFT('small river', 150), 29.76552, -95.352, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-95.352 29.76552)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1401, LEFT('small river', 150), 29.76138, -95.3753, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-95.3753 29.76138)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1402, LEFT('small river', 150), 29.77189, -95.4824, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-95.4824 29.77189)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1403, LEFT('small river', 150), 29.74674, -95.5234, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-95.5234 29.74674)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1404, LEFT('small river', 150), 30.14514, -95.5047, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-95.5047 30.14514)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1405, LEFT('small river', 150), 30.09384, -95.7351, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-95.7351 30.09384)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1406, LEFT('small river', 150), 30.08686, -95.7632, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-95.7632 30.08686)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1407, LEFT('river', 150), 32.44, -97.766667, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-97.766667 32.44)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1408, LEFT('river', 150), 31.56166667, -97.12833333, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-97.12833333 31.56166667)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1409, LEFT('river', 150), 30.55833333, -96.425, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-96.425 30.55833333)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1410, LEFT('river', 150), 30.12833333, -96.18666667, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-96.18666666999999 30.12833333)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1411, LEFT('river', 150), 29.80833333, -96.095, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-96.095 29.80833333)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1412, LEFT('river', 150), 29.025, -95.46166667, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-95.46166667 29.025)'), 4326))
    
    
        INSERT INTO co2data_sitelocation (id, site_description, latitude, longitude, altitude, point) 
        values (1413, LEFT('river', 150), 28.87833333, -95.38, cast(coalesce(nullif('nan', 'nan'), '0') as float), ST_SetSRID(ST_GeomFromText('POINT (-95.38 28.87833333)'), 4326))
    


Another template to load the data into Samples now.


```python
insert_samples_string = """
    INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
    values ('{0}', '{1}', '{2}', cast(coalesce(nullif('{3}', 'nan'), '0') as float), {4})
"""
```


```python
clean_co2_samples.head(1)
print(len(clean_co2_samples))
```

    1378


Iterate through the dataframe to load all the co2 samples into the DB finally!!!


```python
for index, row in clean_co2_samples.iterrows():
        
        print(insert_samples_string.format(str(row["DateTime"]), str(row["SampleType"]), str(row["Unit"]), float(row["CO2"]), int(row["location_id"])))
        cur.execute(insert_samples_string.format(str(row["DateTime"]), str(row["SampleType"]), str(row["Unit"]), float(row["CO2"]), int(row["location_id"])))
        conn.commit()
```

    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2', 'uatm', cast(coalesce(nullif('140.5', 'nan'), '0') as float), 0)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050830', 'CO2', 'uatm', cast(coalesce(nullif('2662.2', 'nan'), '0') as float), 0)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2', 'uatm', cast(coalesce(nullif('140.5', 'nan'), '0') as float), 63)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050830', 'CO2', 'uatm', cast(coalesce(nullif('2662.2', 'nan'), '0') as float), 63)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2', 'uatm', cast(coalesce(nullif('860.3', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2', 'uatm', cast(coalesce(nullif('3228.9', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2', 'uatm', cast(coalesce(nullif('860.3', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2', 'uatm', cast(coalesce(nullif('3228.9', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2', 'uatm', cast(coalesce(nullif('860.3', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2', 'uatm', cast(coalesce(nullif('3228.9', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040705', 'CO2', 'uatm', cast(coalesce(nullif('414.0', 'nan'), '0') as float), 2)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040705', 'CO2', 'uatm', cast(coalesce(nullif('141.3', 'nan'), '0') as float), 3)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040714', 'CO2', 'uatm', cast(coalesce(nullif('5665.0', 'nan'), '0') as float), 4)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040717', 'CO2', 'uatm', cast(coalesce(nullif('425.0', 'nan'), '0') as float), 5)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040718', 'CO2', 'uatm', cast(coalesce(nullif('3958.0', 'nan'), '0') as float), 14)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2', 'uatm', cast(coalesce(nullif('3336.5', 'nan'), '0') as float), 14)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040718', 'CO2', 'uatm', cast(coalesce(nullif('3958.0', 'nan'), '0') as float), 6)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2', 'uatm', cast(coalesce(nullif('3336.5', 'nan'), '0') as float), 6)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040718', 'CO2', 'uatm', cast(coalesce(nullif('5343.0', 'nan'), '0') as float), 7)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040718', 'CO2', 'uatm', cast(coalesce(nullif('4836.0', 'nan'), '0') as float), 7)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040719', 'CO2', 'uatm', cast(coalesce(nullif('425.0', 'nan'), '0') as float), 8)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040719', 'CO2', 'uatm', cast(coalesce(nullif('6037.0', 'nan'), '0') as float), 9)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040720', 'CO2', 'uatm', cast(coalesce(nullif('7548.3', 'nan'), '0') as float), 10)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050716', 'CO2', 'uatm', cast(coalesce(nullif('9225.0', 'nan'), '0') as float), 10)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040720', 'CO2', 'uatm', cast(coalesce(nullif('7548.3', 'nan'), '0') as float), 48)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050716', 'CO2', 'uatm', cast(coalesce(nullif('9225.0', 'nan'), '0') as float), 48)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040722', 'CO2', 'uatm', cast(coalesce(nullif('4247.2', 'nan'), '0') as float), 11)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040810', 'CO2', 'uatm', cast(coalesce(nullif('936.1', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2', 'uatm', cast(coalesce(nullif('503.0', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2', 'uatm', cast(coalesce(nullif('394.3', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040816', 'CO2', 'uatm', cast(coalesce(nullif('506.9', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2', 'uatm', cast(coalesce(nullif('1515.2', 'nan'), '0') as float), 13)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040812', 'CO2', 'uatm', cast(coalesce(nullif('3922.5', 'nan'), '0') as float), 15)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040812', 'CO2', 'uatm', cast(coalesce(nullif('3922.5', 'nan'), '0') as float), 16)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040813', 'CO2', 'uatm', cast(coalesce(nullif('3711.0', 'nan'), '0') as float), 17)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040813', 'CO2', 'uatm', cast(coalesce(nullif('680.1', 'nan'), '0') as float), 18)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040814', 'CO2', 'uatm', cast(coalesce(nullif('565.1', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040814', 'CO2', 'uatm', cast(coalesce(nullif('682.5', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040815', 'CO2', 'uatm', cast(coalesce(nullif('767.2', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040815', 'CO2', 'uatm', cast(coalesce(nullif('813.0', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040815', 'CO2', 'uatm', cast(coalesce(nullif('619.2', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040817', 'CO2', 'uatm', cast(coalesce(nullif('3393.9', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040817', 'CO2', 'uatm', cast(coalesce(nullif('3168.9', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040818', 'CO2', 'uatm', cast(coalesce(nullif('4175.1', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040818', 'CO2', 'uatm', cast(coalesce(nullif('3928.9', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040818', 'CO2', 'uatm', cast(coalesce(nullif('3698.1', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2', 'uatm', cast(coalesce(nullif('616.1', 'nan'), '0') as float), 21)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040824', 'CO2', 'uatm', cast(coalesce(nullif('2524.6', 'nan'), '0') as float), 21)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2', 'uatm', cast(coalesce(nullif('6606.8', 'nan'), '0') as float), 22)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2', 'uatm', cast(coalesce(nullif('5937.3', 'nan'), '0') as float), 23)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040824', 'CO2', 'uatm', cast(coalesce(nullif('4282.7', 'nan'), '0') as float), 24)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050301', 'CO2', 'uatm', cast(coalesce(nullif('3185.0', 'nan'), '0') as float), 25)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2', 'uatm', cast(coalesce(nullif('5665.6', 'nan'), '0') as float), 28)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2', 'uatm', cast(coalesce(nullif('5757.2', 'nan'), '0') as float), 29)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2', 'uatm', cast(coalesce(nullif('3276.0', 'nan'), '0') as float), 30)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2', 'uatm', cast(coalesce(nullif('3344.8', 'nan'), '0') as float), 31)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2', 'uatm', cast(coalesce(nullif('2422.8', 'nan'), '0') as float), 32)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2', 'uatm', cast(coalesce(nullif('2476.7', 'nan'), '0') as float), 33)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2', 'uatm', cast(coalesce(nullif('3318.1', 'nan'), '0') as float), 34)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2', 'uatm', cast(coalesce(nullif('2807.2', 'nan'), '0') as float), 35)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2', 'uatm', cast(coalesce(nullif('3781.3', 'nan'), '0') as float), 36)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2', 'uatm', cast(coalesce(nullif('2374.0', 'nan'), '0') as float), 37)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2', 'uatm', cast(coalesce(nullif('2707.6', 'nan'), '0') as float), 38)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2', 'uatm', cast(coalesce(nullif('2904.7', 'nan'), '0') as float), 40)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2', 'uatm', cast(coalesce(nullif('4762.2', 'nan'), '0') as float), 41)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050312', 'CO2', 'uatm', cast(coalesce(nullif('1696.7', 'nan'), '0') as float), 42)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050312', 'CO2', 'uatm', cast(coalesce(nullif('7051.4', 'nan'), '0') as float), 43)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050713', 'CO2', 'uatm', cast(coalesce(nullif('4918.9', 'nan'), '0') as float), 45)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050715', 'CO2', 'uatm', cast(coalesce(nullif('10195.3', 'nan'), '0') as float), 46)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050715', 'CO2', 'uatm', cast(coalesce(nullif('10317.3', 'nan'), '0') as float), 47)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050719', 'CO2', 'uatm', cast(coalesce(nullif('2978.3', 'nan'), '0') as float), 49)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050719', 'CO2', 'uatm', cast(coalesce(nullif('2901.4', 'nan'), '0') as float), 50)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050721', 'CO2', 'uatm', cast(coalesce(nullif('5810.0', 'nan'), '0') as float), 51)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050725', 'CO2', 'uatm', cast(coalesce(nullif('11144.7', 'nan'), '0') as float), 52)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2', 'uatm', cast(coalesce(nullif('11144.7', 'nan'), '0') as float), 52)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050725', 'CO2', 'uatm', cast(coalesce(nullif('11144.7', 'nan'), '0') as float), 53)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2', 'uatm', cast(coalesce(nullif('11144.7', 'nan'), '0') as float), 53)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2', 'uatm', cast(coalesce(nullif('12523.4', 'nan'), '0') as float), 54)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050727', 'CO2', 'uatm', cast(coalesce(nullif('12615.8', 'nan'), '0') as float), 55)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050818', 'CO2', 'uatm', cast(coalesce(nullif('3946.7', 'nan'), '0') as float), 56)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050818', 'CO2', 'uatm', cast(coalesce(nullif('1462.4', 'nan'), '0') as float), 57)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050820', 'CO2', 'uatm', cast(coalesce(nullif('1923.7', 'nan'), '0') as float), 58)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050820', 'CO2', 'uatm', cast(coalesce(nullif('1719.8', 'nan'), '0') as float), 59)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050829', 'CO2', 'uatm', cast(coalesce(nullif('1374.9', 'nan'), '0') as float), 62)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050831', 'CO2', 'uatm', cast(coalesce(nullif('1375.6', 'nan'), '0') as float), 64)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050904', 'CO2', 'uatm', cast(coalesce(nullif('1110.4', 'nan'), '0') as float), 65)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061125', 'CO2', 'uatm', cast(coalesce(nullif('2416.052891', 'nan'), '0') as float), 67)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061127', 'CO2', 'uatm', cast(coalesce(nullif('3917.523126', 'nan'), '0') as float), 68)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2', 'uatm', cast(coalesce(nullif('3478.977943', 'nan'), '0') as float), 73)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2', 'uatm', cast(coalesce(nullif('6430.30547', 'nan'), '0') as float), 75)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2', 'uatm', cast(coalesce(nullif('3073.304174', 'nan'), '0') as float), 76)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2', 'uatm', cast(coalesce(nullif('2908.287255', 'nan'), '0') as float), 77)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2', 'uatm', cast(coalesce(nullif('3864.854859', 'nan'), '0') as float), 78)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2', 'uatm', cast(coalesce(nullif('2278.12582', 'nan'), '0') as float), 79)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2', 'uatm', cast(coalesce(nullif('3190.397483', 'nan'), '0') as float), 80)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2', 'uatm', cast(coalesce(nullif('2046.7', 'nan'), '0') as float), 82)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2', 'uatm', cast(coalesce(nullif('2590.7', 'nan'), '0') as float), 83)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061215', 'CO2', 'uatm', cast(coalesce(nullif('1086.419985', 'nan'), '0') as float), 84)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061215', 'CO2', 'uatm', cast(coalesce(nullif('1392.605626', 'nan'), '0') as float), 85)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2', 'uatm', cast(coalesce(nullif('2390.484515', 'nan'), '0') as float), 86)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2', 'uatm', cast(coalesce(nullif('1674.097649', 'nan'), '0') as float), 87)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2', 'uatm', cast(coalesce(nullif('2137.349087', 'nan'), '0') as float), 88)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2', 'uatm', cast(coalesce(nullif('3548.605616', 'nan'), '0') as float), 89)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070123', 'CO2', 'uatm', cast(coalesce(nullif('4451.167895', 'nan'), '0') as float), 90)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070123', 'CO2', 'uatm', cast(coalesce(nullif('3877.314264', 'nan'), '0') as float), 91)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41611', 'CO2', 'uatm', cast(coalesce(nullif('2424.0', 'nan'), '0') as float), 308)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41611', 'CO2', 'uatm', cast(coalesce(nullif('2349.0', 'nan'), '0') as float), 309)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41611', 'CO2', 'uatm', cast(coalesce(nullif('1697.0', 'nan'), '0') as float), 310)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41611', 'CO2', 'uatm', cast(coalesce(nullif('2262.0', 'nan'), '0') as float), 311)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41611', 'CO2', 'uatm', cast(coalesce(nullif('2371.0', 'nan'), '0') as float), 312)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41612', 'CO2', 'uatm', cast(coalesce(nullif('4478.0', 'nan'), '0') as float), 313)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41612', 'CO2', 'uatm', cast(coalesce(nullif('2455.0', 'nan'), '0') as float), 314)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41612', 'CO2', 'uatm', cast(coalesce(nullif('3008.0', 'nan'), '0') as float), 315)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41612', 'CO2', 'uatm', cast(coalesce(nullif('2831.0', 'nan'), '0') as float), 316)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41613', 'CO2', 'uatm', cast(coalesce(nullif('4697.0', 'nan'), '0') as float), 317)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41613', 'CO2', 'uatm', cast(coalesce(nullif('3522.0', 'nan'), '0') as float), 318)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41613', 'CO2', 'uatm', cast(coalesce(nullif('12232.0', 'nan'), '0') as float), 319)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41613', 'CO2', 'uatm', cast(coalesce(nullif('2928.0', 'nan'), '0') as float), 320)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41614', 'CO2', 'uatm', cast(coalesce(nullif('3720.0', 'nan'), '0') as float), 321)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41614', 'CO2', 'uatm', cast(coalesce(nullif('7735.0', 'nan'), '0') as float), 322)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41614', 'CO2', 'uatm', cast(coalesce(nullif('6088.0', 'nan'), '0') as float), 323)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41614', 'CO2', 'uatm', cast(coalesce(nullif('3857.0', 'nan'), '0') as float), 324)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41614', 'CO2', 'uatm', cast(coalesce(nullif('4304.0', 'nan'), '0') as float), 325)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615', 'CO2', 'uatm', cast(coalesce(nullif('8921.0', 'nan'), '0') as float), 326)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615', 'CO2', 'uatm', cast(coalesce(nullif('12662.0', 'nan'), '0') as float), 327)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615', 'CO2', 'uatm', cast(coalesce(nullif('4149.0', 'nan'), '0') as float), 328)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615', 'CO2', 'uatm', cast(coalesce(nullif('4176.0', 'nan'), '0') as float), 329)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615', 'CO2', 'uatm', cast(coalesce(nullif('9528.0', 'nan'), '0') as float), 330)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615', 'CO2', 'uatm', cast(coalesce(nullif('5437.0', 'nan'), '0') as float), 331)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41616', 'CO2', 'uatm', cast(coalesce(nullif('11464.0', 'nan'), '0') as float), 332)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41616', 'CO2', 'uatm', cast(coalesce(nullif('4168.0', 'nan'), '0') as float), 333)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41616', 'CO2', 'uatm', cast(coalesce(nullif('8147.0', 'nan'), '0') as float), 334)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41616', 'CO2', 'uatm', cast(coalesce(nullif('8929.0', 'nan'), '0') as float), 335)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41616', 'CO2', 'uatm', cast(coalesce(nullif('4476.0', 'nan'), '0') as float), 336)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41617', 'CO2', 'uatm', cast(coalesce(nullif('4460.0', 'nan'), '0') as float), 337)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41617', 'CO2', 'uatm', cast(coalesce(nullif('10067.0', 'nan'), '0') as float), 338)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41617', 'CO2', 'uatm', cast(coalesce(nullif('4496.0', 'nan'), '0') as float), 339)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41618', 'CO2', 'uatm', cast(coalesce(nullif('8532.0', 'nan'), '0') as float), 340)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41618', 'CO2', 'uatm', cast(coalesce(nullif('9382.0', 'nan'), '0') as float), 341)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41618', 'CO2', 'uatm', cast(coalesce(nullif('10770.0', 'nan'), '0') as float), 342)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41618', 'CO2', 'uatm', cast(coalesce(nullif('5648.0', 'nan'), '0') as float), 343)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41618', 'CO2', 'uatm', cast(coalesce(nullif('8137.0', 'nan'), '0') as float), 344)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41618', 'CO2', 'uatm', cast(coalesce(nullif('12382.0', 'nan'), '0') as float), 345)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41619', 'CO2', 'uatm', cast(coalesce(nullif('9755.0', 'nan'), '0') as float), 346)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41619', 'CO2', 'uatm', cast(coalesce(nullif('4891.0', 'nan'), '0') as float), 347)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41619', 'CO2', 'uatm', cast(coalesce(nullif('6643.0', 'nan'), '0') as float), 348)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41619', 'CO2', 'uatm', cast(coalesce(nullif('6084.0', 'nan'), '0') as float), 349)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41620', 'CO2', 'uatm', cast(coalesce(nullif('12059.0', 'nan'), '0') as float), 350)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41620', 'CO2', 'uatm', cast(coalesce(nullif('12996.0', 'nan'), '0') as float), 351)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41620', 'CO2', 'uatm', cast(coalesce(nullif('8686.0', 'nan'), '0') as float), 352)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41620', 'CO2', 'uatm', cast(coalesce(nullif('12642.0', 'nan'), '0') as float), 353)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41621', 'CO2', 'uatm', cast(coalesce(nullif('3975.0', 'nan'), '0') as float), 354)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41621', 'CO2', 'uatm', cast(coalesce(nullif('4735.0', 'nan'), '0') as float), 355)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41622', 'CO2', 'uatm', cast(coalesce(nullif('2504.0', 'nan'), '0') as float), 356)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41622', 'CO2', 'uatm', cast(coalesce(nullif('5256.0', 'nan'), '0') as float), 357)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41622', 'CO2', 'uatm', cast(coalesce(nullif('6933.0', 'nan'), '0') as float), 358)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41622', 'CO2', 'uatm', cast(coalesce(nullif('4706.0', 'nan'), '0') as float), 359)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41623', 'CO2', 'uatm', cast(coalesce(nullif('15571.0', 'nan'), '0') as float), 360)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41623', 'CO2', 'uatm', cast(coalesce(nullif('4875.0', 'nan'), '0') as float), 361)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41623', 'CO2', 'uatm', cast(coalesce(nullif('11142.0', 'nan'), '0') as float), 362)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41623', 'CO2', 'uatm', cast(coalesce(nullif('5263.0', 'nan'), '0') as float), 363)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41624', 'CO2', 'uatm', cast(coalesce(nullif('14703.0', 'nan'), '0') as float), 364)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41624', 'CO2', 'uatm', cast(coalesce(nullif('13705.0', 'nan'), '0') as float), 365)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41624', 'CO2', 'uatm', cast(coalesce(nullif('4844.0', 'nan'), '0') as float), 366)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41624', 'CO2', 'uatm', cast(coalesce(nullif('14299.0', 'nan'), '0') as float), 367)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41624', 'CO2', 'uatm', cast(coalesce(nullif('5713.0', 'nan'), '0') as float), 368)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41625', 'CO2', 'uatm', cast(coalesce(nullif('4840.0', 'nan'), '0') as float), 369)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41625', 'CO2', 'uatm', cast(coalesce(nullif('4430.0', 'nan'), '0') as float), 370)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41625', 'CO2', 'uatm', cast(coalesce(nullif('5923.0', 'nan'), '0') as float), 371)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41625', 'CO2', 'uatm', cast(coalesce(nullif('5813.0', 'nan'), '0') as float), 372)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41626', 'CO2', 'uatm', cast(coalesce(nullif('4669.0', 'nan'), '0') as float), 373)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41626', 'CO2', 'uatm', cast(coalesce(nullif('6880.0', 'nan'), '0') as float), 374)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41626', 'CO2', 'uatm', cast(coalesce(nullif('5963.0', 'nan'), '0') as float), 375)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41626', 'CO2', 'uatm', cast(coalesce(nullif('1582.0', 'nan'), '0') as float), 376)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41626', 'CO2', 'uatm', cast(coalesce(nullif('5868.0', 'nan'), '0') as float), 377)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41627', 'CO2', 'uatm', cast(coalesce(nullif('1903.0', 'nan'), '0') as float), 378)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41627', 'CO2', 'uatm', cast(coalesce(nullif('5826.0', 'nan'), '0') as float), 379)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41627', 'CO2', 'uatm', cast(coalesce(nullif('5635.0', 'nan'), '0') as float), 380)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41627', 'CO2', 'uatm', cast(coalesce(nullif('1974.0', 'nan'), '0') as float), 381)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41627', 'CO2', 'uatm', cast(coalesce(nullif('5343.0', 'nan'), '0') as float), 382)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41800', 'CO2', 'uatm', cast(coalesce(nullif('1670.0', 'nan'), '0') as float), 383)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41800', 'CO2', 'uatm', cast(coalesce(nullif('2563.0', 'nan'), '0') as float), 384)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41800', 'CO2', 'uatm', cast(coalesce(nullif('1439.0', 'nan'), '0') as float), 385)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41800', 'CO2', 'uatm', cast(coalesce(nullif('1699.0', 'nan'), '0') as float), 386)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41800', 'CO2', 'uatm', cast(coalesce(nullif('5268.0', 'nan'), '0') as float), 387)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41800', 'CO2', 'uatm', cast(coalesce(nullif('5859.0', 'nan'), '0') as float), 388)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41801', 'CO2', 'uatm', cast(coalesce(nullif('1807.0', 'nan'), '0') as float), 389)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41801', 'CO2', 'uatm', cast(coalesce(nullif('2286.0', 'nan'), '0') as float), 390)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41801', 'CO2', 'uatm', cast(coalesce(nullif('1767.0', 'nan'), '0') as float), 391)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41801', 'CO2', 'uatm', cast(coalesce(nullif('3475.0', 'nan'), '0') as float), 392)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41801', 'CO2', 'uatm', cast(coalesce(nullif('1710.0', 'nan'), '0') as float), 393)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41802', 'CO2', 'uatm', cast(coalesce(nullif('1754.0', 'nan'), '0') as float), 394)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41802', 'CO2', 'uatm', cast(coalesce(nullif('3591.0', 'nan'), '0') as float), 395)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41802', 'CO2', 'uatm', cast(coalesce(nullif('1791.0', 'nan'), '0') as float), 396)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41802', 'CO2', 'uatm', cast(coalesce(nullif('10670.0', 'nan'), '0') as float), 397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41802', 'CO2', 'uatm', cast(coalesce(nullif('1567.0', 'nan'), '0') as float), 398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41803', 'CO2', 'uatm', cast(coalesce(nullif('1514.0', 'nan'), '0') as float), 399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41803', 'CO2', 'uatm', cast(coalesce(nullif('6444.0', 'nan'), '0') as float), 400)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41803', 'CO2', 'uatm', cast(coalesce(nullif('8035.0', 'nan'), '0') as float), 401)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41803', 'CO2', 'uatm', cast(coalesce(nullif('3346.0', 'nan'), '0') as float), 402)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41804', 'CO2', 'uatm', cast(coalesce(nullif('1571.0', 'nan'), '0') as float), 403)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41804', 'CO2', 'uatm', cast(coalesce(nullif('9432.0', 'nan'), '0') as float), 404)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41804', 'CO2', 'uatm', cast(coalesce(nullif('1629.0', 'nan'), '0') as float), 405)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41804', 'CO2', 'uatm', cast(coalesce(nullif('11211.0', 'nan'), '0') as float), 406)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41805', 'CO2', 'uatm', cast(coalesce(nullif('1390.0', 'nan'), '0') as float), 407)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41805', 'CO2', 'uatm', cast(coalesce(nullif('9282.0', 'nan'), '0') as float), 408)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41805', 'CO2', 'uatm', cast(coalesce(nullif('1229.0', 'nan'), '0') as float), 409)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41805', 'CO2', 'uatm', cast(coalesce(nullif('11133.0', 'nan'), '0') as float), 410)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41806', 'CO2', 'uatm', cast(coalesce(nullif('12304.0', 'nan'), '0') as float), 411)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41806', 'CO2', 'uatm', cast(coalesce(nullif('15375.0', 'nan'), '0') as float), 412)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41806', 'CO2', 'uatm', cast(coalesce(nullif('1360.0', 'nan'), '0') as float), 413)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41806', 'CO2', 'uatm', cast(coalesce(nullif('15278.0', 'nan'), '0') as float), 414)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41806', 'CO2', 'uatm', cast(coalesce(nullif('10189.0', 'nan'), '0') as float), 415)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41806', 'CO2', 'uatm', cast(coalesce(nullif('1424.0', 'nan'), '0') as float), 416)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41806', 'CO2', 'uatm', cast(coalesce(nullif('15905.0', 'nan'), '0') as float), 417)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41807', 'CO2', 'uatm', cast(coalesce(nullif('9813.0', 'nan'), '0') as float), 418)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41807', 'CO2', 'uatm', cast(coalesce(nullif('9787.0', 'nan'), '0') as float), 419)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41807', 'CO2', 'uatm', cast(coalesce(nullif('1395.0', 'nan'), '0') as float), 420)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41807', 'CO2', 'uatm', cast(coalesce(nullif('15692.0', 'nan'), '0') as float), 421)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41807', 'CO2', 'uatm', cast(coalesce(nullif('1772.0', 'nan'), '0') as float), 422)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41808', 'CO2', 'uatm', cast(coalesce(nullif('1278.0', 'nan'), '0') as float), 423)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41808', 'CO2', 'uatm', cast(coalesce(nullif('15788.0', 'nan'), '0') as float), 424)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41808', 'CO2', 'uatm', cast(coalesce(nullif('1364.0', 'nan'), '0') as float), 425)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41808', 'CO2', 'uatm', cast(coalesce(nullif('16785.0', 'nan'), '0') as float), 426)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41808', 'CO2', 'uatm', cast(coalesce(nullif('9749.0', 'nan'), '0') as float), 427)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41809', 'CO2', 'uatm', cast(coalesce(nullif('1335.0', 'nan'), '0') as float), 428)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41809', 'CO2', 'uatm', cast(coalesce(nullif('4638.0', 'nan'), '0') as float), 429)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41809', 'CO2', 'uatm', cast(coalesce(nullif('1317.0', 'nan'), '0') as float), 430)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41809', 'CO2', 'uatm', cast(coalesce(nullif('16764.0', 'nan'), '0') as float), 431)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41809', 'CO2', 'uatm', cast(coalesce(nullif('11760.0', 'nan'), '0') as float), 432)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41810', 'CO2', 'uatm', cast(coalesce(nullif('6326.0', 'nan'), '0') as float), 433)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41810', 'CO2', 'uatm', cast(coalesce(nullif('11188.0', 'nan'), '0') as float), 434)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41811', 'CO2', 'uatm', cast(coalesce(nullif('1320.0', 'nan'), '0') as float), 435)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41811', 'CO2', 'uatm', cast(coalesce(nullif('16942.0', 'nan'), '0') as float), 436)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41811', 'CO2', 'uatm', cast(coalesce(nullif('1499.0', 'nan'), '0') as float), 437)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41811', 'CO2', 'uatm', cast(coalesce(nullif('13955.0', 'nan'), '0') as float), 438)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41813', 'CO2', 'uatm', cast(coalesce(nullif('8726.0', 'nan'), '0') as float), 439)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41813', 'CO2', 'uatm', cast(coalesce(nullif('1856.0', 'nan'), '0') as float), 440)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41813', 'CO2', 'uatm', cast(coalesce(nullif('15002.0', 'nan'), '0') as float), 441)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41813', 'CO2', 'uatm', cast(coalesce(nullif('1555.0', 'nan'), '0') as float), 442)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41814', 'CO2', 'uatm', cast(coalesce(nullif('2510.0', 'nan'), '0') as float), 443)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41814', 'CO2', 'uatm', cast(coalesce(nullif('1517.0', 'nan'), '0') as float), 444)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41814', 'CO2', 'uatm', cast(coalesce(nullif('2949.0', 'nan'), '0') as float), 445)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41815', 'CO2', 'uatm', cast(coalesce(nullif('2303.0', 'nan'), '0') as float), 446)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41815', 'CO2', 'uatm', cast(coalesce(nullif('10176.0', 'nan'), '0') as float), 447)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41815', 'CO2', 'uatm', cast(coalesce(nullif('8415.0', 'nan'), '0') as float), 448)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41815', 'CO2', 'uatm', cast(coalesce(nullif('1883.0', 'nan'), '0') as float), 449)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41815', 'CO2', 'uatm', cast(coalesce(nullif('5892.0', 'nan'), '0') as float), 450)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41816', 'CO2', 'uatm', cast(coalesce(nullif('1998.0', 'nan'), '0') as float), 451)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41816', 'CO2', 'uatm', cast(coalesce(nullif('16287.0', 'nan'), '0') as float), 452)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41816', 'CO2', 'uatm', cast(coalesce(nullif('2529.0', 'nan'), '0') as float), 453)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41816', 'CO2', 'uatm', cast(coalesce(nullif('14551.0', 'nan'), '0') as float), 454)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41816', 'CO2', 'uatm', cast(coalesce(nullif('7643.0', 'nan'), '0') as float), 455)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41817', 'CO2', 'uatm', cast(coalesce(nullif('2206.0', 'nan'), '0') as float), 456)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41817', 'CO2', 'uatm', cast(coalesce(nullif('1970.0', 'nan'), '0') as float), 457)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41817', 'CO2', 'uatm', cast(coalesce(nullif('2096.0', 'nan'), '0') as float), 458)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41818', 'CO2', 'uatm', cast(coalesce(nullif('2415.0', 'nan'), '0') as float), 459)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41818', 'CO2', 'uatm', cast(coalesce(nullif('2142.0', 'nan'), '0') as float), 460)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41818', 'CO2', 'uatm', cast(coalesce(nullif('1838.0', 'nan'), '0') as float), 461)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41818', 'CO2', 'uatm', cast(coalesce(nullif('3459.0', 'nan'), '0') as float), 462)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41818', 'CO2', 'uatm', cast(coalesce(nullif('1087.0', 'nan'), '0') as float), 463)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41819', 'CO2', 'uatm', cast(coalesce(nullif('2483.0', 'nan'), '0') as float), 464)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41819', 'CO2', 'uatm', cast(coalesce(nullif('3442.0', 'nan'), '0') as float), 465)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41819', 'CO2', 'uatm', cast(coalesce(nullif('1726.0', 'nan'), '0') as float), 466)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41819', 'CO2', 'uatm', cast(coalesce(nullif('1929.0', 'nan'), '0') as float), 467)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41819', 'CO2', 'uatm', cast(coalesce(nullif('3420.0', 'nan'), '0') as float), 468)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41820', 'CO2', 'uatm', cast(coalesce(nullif('1193.0', 'nan'), '0') as float), 469)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41820', 'CO2', 'uatm', cast(coalesce(nullif('2896.0', 'nan'), '0') as float), 470)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41711', 'CO2', 'uatm', cast(coalesce(nullif('1945.0', 'nan'), '0') as float), 471)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41711', 'CO2', 'uatm', cast(coalesce(nullif('1465.0', 'nan'), '0') as float), 472)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41711', 'CO2', 'uatm', cast(coalesce(nullif('1834.0', 'nan'), '0') as float), 473)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41711', 'CO2', 'uatm', cast(coalesce(nullif('3143.0', 'nan'), '0') as float), 474)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41712', 'CO2', 'uatm', cast(coalesce(nullif('2153.0', 'nan'), '0') as float), 475)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41712', 'CO2', 'uatm', cast(coalesce(nullif('2123.0', 'nan'), '0') as float), 476)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41712', 'CO2', 'uatm', cast(coalesce(nullif('2326.0', 'nan'), '0') as float), 477)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41715', 'CO2', 'uatm', cast(coalesce(nullif('5093.0', 'nan'), '0') as float), 478)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41715', 'CO2', 'uatm', cast(coalesce(nullif('2688.0', 'nan'), '0') as float), 479)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41715', 'CO2', 'uatm', cast(coalesce(nullif('5327.0', 'nan'), '0') as float), 480)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41716', 'CO2', 'uatm', cast(coalesce(nullif('5005.0', 'nan'), '0') as float), 481)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41716', 'CO2', 'uatm', cast(coalesce(nullif('4992.0', 'nan'), '0') as float), 482)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41716', 'CO2', 'uatm', cast(coalesce(nullif('5672.0', 'nan'), '0') as float), 483)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41718', 'CO2', 'uatm', cast(coalesce(nullif('3533.0', 'nan'), '0') as float), 484)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41718', 'CO2', 'uatm', cast(coalesce(nullif('3565.0', 'nan'), '0') as float), 485)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41718', 'CO2', 'uatm', cast(coalesce(nullif('2008.0', 'nan'), '0') as float), 486)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41718', 'CO2', 'uatm', cast(coalesce(nullif('1604.0', 'nan'), '0') as float), 487)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41719', 'CO2', 'uatm', cast(coalesce(nullif('1700.0', 'nan'), '0') as float), 488)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41719', 'CO2', 'uatm', cast(coalesce(nullif('1472.0', 'nan'), '0') as float), 489)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41719', 'CO2', 'uatm', cast(coalesce(nullif('1599.0', 'nan'), '0') as float), 490)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41534', 'CO2', 'uatm', cast(coalesce(nullif('2502.0', 'nan'), '0') as float), 491)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41539', 'CO2', 'uatm', cast(coalesce(nullif('6132.0', 'nan'), '0') as float), 494)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41540', 'CO2', 'uatm', cast(coalesce(nullif('6702.0', 'nan'), '0') as float), 495)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41541', 'CO2', 'uatm', cast(coalesce(nullif('7308.0', 'nan'), '0') as float), 496)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41542', 'CO2', 'uatm', cast(coalesce(nullif('1217.0', 'nan'), '0') as float), 497)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41543', 'CO2', 'uatm', cast(coalesce(nullif('1693.0', 'nan'), '0') as float), 498)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41233', 'CO2', 'uatm', cast(coalesce(nullif('6300.0', 'nan'), '0') as float), 499)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41234', 'CO2', 'uatm', cast(coalesce(nullif('7252.0', 'nan'), '0') as float), 500)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41234', 'CO2', 'uatm', cast(coalesce(nullif('6605.0', 'nan'), '0') as float), 501)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41237', 'CO2', 'uatm', cast(coalesce(nullif('4481.0', 'nan'), '0') as float), 502)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41237', 'CO2', 'uatm', cast(coalesce(nullif('7770.0', 'nan'), '0') as float), 503)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41238', 'CO2', 'uatm', cast(coalesce(nullif('5264.0', 'nan'), '0') as float), 504)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41238', 'CO2', 'uatm', cast(coalesce(nullif('4237.0', 'nan'), '0') as float), 505)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41240', 'CO2', 'uatm', cast(coalesce(nullif('2016.0', 'nan'), '0') as float), 506)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41240', 'CO2', 'uatm', cast(coalesce(nullif('3971.0', 'nan'), '0') as float), 507)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41241', 'CO2', 'uatm', cast(coalesce(nullif('12509.0', 'nan'), '0') as float), 508)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41244', 'CO2', 'uatm', cast(coalesce(nullif('8170.0', 'nan'), '0') as float), 509)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41244', 'CO2', 'uatm', cast(coalesce(nullif('4625.0', 'nan'), '0') as float), 510)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41245', 'CO2', 'uatm', cast(coalesce(nullif('2655.0', 'nan'), '0') as float), 511)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41245', 'CO2', 'uatm', cast(coalesce(nullif('2539.0', 'nan'), '0') as float), 512)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41245', 'CO2', 'uatm', cast(coalesce(nullif('2384.0', 'nan'), '0') as float), 513)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41245', 'CO2', 'uatm', cast(coalesce(nullif('2394.0', 'nan'), '0') as float), 514)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41245', 'CO2', 'uatm', cast(coalesce(nullif('2453.0', 'nan'), '0') as float), 515)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41245', 'CO2', 'uatm', cast(coalesce(nullif('2462.0', 'nan'), '0') as float), 516)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41245', 'CO2', 'uatm', cast(coalesce(nullif('2559.0', 'nan'), '0') as float), 517)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41245', 'CO2', 'uatm', cast(coalesce(nullif('2606.0', 'nan'), '0') as float), 518)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41245', 'CO2', 'uatm', cast(coalesce(nullif('2677.0', 'nan'), '0') as float), 519)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41245', 'CO2', 'uatm', cast(coalesce(nullif('2752.0', 'nan'), '0') as float), 520)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41246', 'CO2', 'uatm', cast(coalesce(nullif('2750.0', 'nan'), '0') as float), 521)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41246', 'CO2', 'uatm', cast(coalesce(nullif('2521.0', 'nan'), '0') as float), 522)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41247', 'CO2', 'uatm', cast(coalesce(nullif('2670.0', 'nan'), '0') as float), 523)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41247', 'CO2', 'uatm', cast(coalesce(nullif('3237.0', 'nan'), '0') as float), 524)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41248', 'CO2', 'uatm', cast(coalesce(nullif('7422.0', 'nan'), '0') as float), 525)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41248', 'CO2', 'uatm', cast(coalesce(nullif('2415.0', 'nan'), '0') as float), 526)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41249', 'CO2', 'uatm', cast(coalesce(nullif('2430.0', 'nan'), '0') as float), 527)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41250', 'CO2', 'uatm', cast(coalesce(nullif('2373.0', 'nan'), '0') as float), 528)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41250', 'CO2', 'uatm', cast(coalesce(nullif('1720.0', 'nan'), '0') as float), 529)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41251', 'CO2', 'uatm', cast(coalesce(nullif('2748.0', 'nan'), '0') as float), 530)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40944', 'CO2', 'uatm', cast(coalesce(nullif('1056.0', 'nan'), '0') as float), 760)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41287', 'CO2', 'uatm', cast(coalesce(nullif('2005.0', 'nan'), '0') as float), 760)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40946', 'CO2', 'uatm', cast(coalesce(nullif('2444.0', 'nan'), '0') as float), 761)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40947', 'CO2', 'uatm', cast(coalesce(nullif('1968.0', 'nan'), '0') as float), 762)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40949', 'CO2', 'uatm', cast(coalesce(nullif('7650.0', 'nan'), '0') as float), 763)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40950', 'CO2', 'uatm', cast(coalesce(nullif('1890.0', 'nan'), '0') as float), 764)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40950', 'CO2', 'uatm', cast(coalesce(nullif('6307.0', 'nan'), '0') as float), 765)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40951', 'CO2', 'uatm', cast(coalesce(nullif('2500.0', 'nan'), '0') as float), 766)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40953', 'CO2', 'uatm', cast(coalesce(nullif('642.0', 'nan'), '0') as float), 767)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40958', 'CO2', 'uatm', cast(coalesce(nullif('2008.0', 'nan'), '0') as float), 768)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40960', 'CO2', 'uatm', cast(coalesce(nullif('1228.0', 'nan'), '0') as float), 769)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40963', 'CO2', 'uatm', cast(coalesce(nullif('888.0', 'nan'), '0') as float), 770)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40991', 'CO2', 'uatm', cast(coalesce(nullif('3945.0', 'nan'), '0') as float), 771)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40992', 'CO2', 'uatm', cast(coalesce(nullif('2806.0', 'nan'), '0') as float), 772)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40992', 'CO2', 'uatm', cast(coalesce(nullif('1830.0', 'nan'), '0') as float), 773)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40994', 'CO2', 'uatm', cast(coalesce(nullif('3972.0', 'nan'), '0') as float), 774)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40995', 'CO2', 'uatm', cast(coalesce(nullif('1858.0', 'nan'), '0') as float), 775)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40996', 'CO2', 'uatm', cast(coalesce(nullif('904.0', 'nan'), '0') as float), 776)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40998', 'CO2', 'uatm', cast(coalesce(nullif('1620.0', 'nan'), '0') as float), 777)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40999', 'CO2', 'uatm', cast(coalesce(nullif('9985.0', 'nan'), '0') as float), 778)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41000', 'CO2', 'uatm', cast(coalesce(nullif('9769.0', 'nan'), '0') as float), 779)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41001', 'CO2', 'uatm', cast(coalesce(nullif('1357.0', 'nan'), '0') as float), 780)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41007', 'CO2', 'uatm', cast(coalesce(nullif('1305.0', 'nan'), '0') as float), 781)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41008', 'CO2', 'uatm', cast(coalesce(nullif('1227.0', 'nan'), '0') as float), 782)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40962', 'CO2', 'uatm', cast(coalesce(nullif('1469.0', 'nan'), '0') as float), 783)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41009', 'CO2', 'uatm', cast(coalesce(nullif('1201.0', 'nan'), '0') as float), 784)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41004', 'CO2', 'uatm', cast(coalesce(nullif('2952.0', 'nan'), '0') as float), 785)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41010', 'CO2', 'uatm', cast(coalesce(nullif('1523.0', 'nan'), '0') as float), 786)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40990', 'CO2', 'uatm', cast(coalesce(nullif('2621.0', 'nan'), '0') as float), 787)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40993', 'CO2', 'uatm', cast(coalesce(nullif('4465.0', 'nan'), '0') as float), 788)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40994', 'CO2', 'uatm', cast(coalesce(nullif('2460.0', 'nan'), '0') as float), 789)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41286', 'CO2', 'uatm', cast(coalesce(nullif('1234.0', 'nan'), '0') as float), 790)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41015', 'CO2', 'uatm', cast(coalesce(nullif('1802.0', 'nan'), '0') as float), 791)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41018', 'CO2', 'uatm', cast(coalesce(nullif('814.0', 'nan'), '0') as float), 792)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41019', 'CO2', 'uatm', cast(coalesce(nullif('559.0', 'nan'), '0') as float), 793)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41022', 'CO2', 'uatm', cast(coalesce(nullif('1204.0', 'nan'), '0') as float), 794)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41021', 'CO2', 'uatm', cast(coalesce(nullif('8181.0', 'nan'), '0') as float), 795)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41023', 'CO2', 'uatm', cast(coalesce(nullif('1789.0', 'nan'), '0') as float), 796)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41026', 'CO2', 'uatm', cast(coalesce(nullif('1612.0', 'nan'), '0') as float), 797)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41021', 'CO2', 'uatm', cast(coalesce(nullif('12698.0', 'nan'), '0') as float), 798)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41001', 'CO2', 'uatm', cast(coalesce(nullif('1793.0', 'nan'), '0') as float), 799)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41299', 'CO2', 'uatm', cast(coalesce(nullif('2207.0', 'nan'), '0') as float), 799)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41322', 'CO2', 'uatm', cast(coalesce(nullif('2122.0', 'nan'), '0') as float), 799)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41350', 'CO2', 'uatm', cast(coalesce(nullif('2348.0', 'nan'), '0') as float), 799)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41574', 'CO2', 'uatm', cast(coalesce(nullif('1602.0', 'nan'), '0') as float), 799)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41585', 'CO2', 'uatm', cast(coalesce(nullif('1611.0', 'nan'), '0') as float), 799)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41600', 'CO2', 'uatm', cast(coalesce(nullif('1644.0', 'nan'), '0') as float), 799)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41009', 'CO2', 'uatm', cast(coalesce(nullif('735.0', 'nan'), '0') as float), 800)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40961', 'CO2', 'uatm', cast(coalesce(nullif('9057.0', 'nan'), '0') as float), 801)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40959', 'CO2', 'uatm', cast(coalesce(nullif('1305.0', 'nan'), '0') as float), 802)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40963', 'CO2', 'uatm', cast(coalesce(nullif('1233.0', 'nan'), '0') as float), 803)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41288', 'CO2', 'uatm', cast(coalesce(nullif('2576.0', 'nan'), '0') as float), 804)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41290', 'CO2', 'uatm', cast(coalesce(nullif('2560.0', 'nan'), '0') as float), 805)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41291', 'CO2', 'uatm', cast(coalesce(nullif('10351.0', 'nan'), '0') as float), 806)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41292', 'CO2', 'uatm', cast(coalesce(nullif('1555.0', 'nan'), '0') as float), 807)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41293', 'CO2', 'uatm', cast(coalesce(nullif('4979.0', 'nan'), '0') as float), 808)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41295', 'CO2', 'uatm', cast(coalesce(nullif('1718.0', 'nan'), '0') as float), 809)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41295', 'CO2', 'uatm', cast(coalesce(nullif('663.0', 'nan'), '0') as float), 810)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41299', 'CO2', 'uatm', cast(coalesce(nullif('2207.0', 'nan'), '0') as float), 811)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41303', 'CO2', 'uatm', cast(coalesce(nullif('1447.0', 'nan'), '0') as float), 812)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41313', 'CO2', 'uatm', cast(coalesce(nullif('4346.0', 'nan'), '0') as float), 813)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41312', 'CO2', 'uatm', cast(coalesce(nullif('3093.0', 'nan'), '0') as float), 814)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41308', 'CO2', 'uatm', cast(coalesce(nullif('3407.0', 'nan'), '0') as float), 815)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41315', 'CO2', 'uatm', cast(coalesce(nullif('4136.0', 'nan'), '0') as float), 816)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41316', 'CO2', 'uatm', cast(coalesce(nullif('2300.0', 'nan'), '0') as float), 817)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41318', 'CO2', 'uatm', cast(coalesce(nullif('1237.0', 'nan'), '0') as float), 818)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41320', 'CO2', 'uatm', cast(coalesce(nullif('11747.0', 'nan'), '0') as float), 819)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41321', 'CO2', 'uatm', cast(coalesce(nullif('10915.0', 'nan'), '0') as float), 820)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41322', 'CO2', 'uatm', cast(coalesce(nullif('1552.0', 'nan'), '0') as float), 821)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41344', 'CO2', 'uatm', cast(coalesce(nullif('1410.0', 'nan'), '0') as float), 822)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41301', 'CO2', 'uatm', cast(coalesce(nullif('1855.0', 'nan'), '0') as float), 823)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41302', 'CO2', 'uatm', cast(coalesce(nullif('1432.0', 'nan'), '0') as float), 824)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41303', 'CO2', 'uatm', cast(coalesce(nullif('1317.0', 'nan'), '0') as float), 825)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41307', 'CO2', 'uatm', cast(coalesce(nullif('2493.0', 'nan'), '0') as float), 826)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41304', 'CO2', 'uatm', cast(coalesce(nullif('2154.0', 'nan'), '0') as float), 827)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41314', 'CO2', 'uatm', cast(coalesce(nullif('3284.0', 'nan'), '0') as float), 828)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41315', 'CO2', 'uatm', cast(coalesce(nullif('2855.0', 'nan'), '0') as float), 829)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41289', 'CO2', 'uatm', cast(coalesce(nullif('2470.0', 'nan'), '0') as float), 830)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41327', 'CO2', 'uatm', cast(coalesce(nullif('1272.0', 'nan'), '0') as float), 831)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41329', 'CO2', 'uatm', cast(coalesce(nullif('3615.0', 'nan'), '0') as float), 832)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41330', 'CO2', 'uatm', cast(coalesce(nullif('12199.0', 'nan'), '0') as float), 833)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41335', 'CO2', 'uatm', cast(coalesce(nullif('4291.0', 'nan'), '0') as float), 834)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41334', 'CO2', 'uatm', cast(coalesce(nullif('4521.0', 'nan'), '0') as float), 835)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41331', 'CO2', 'uatm', cast(coalesce(nullif('14004.0', 'nan'), '0') as float), 836)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41339', 'CO2', 'uatm', cast(coalesce(nullif('955.0', 'nan'), '0') as float), 837)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41345', 'CO2', 'uatm', cast(coalesce(nullif('1584.0', 'nan'), '0') as float), 838)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41345', 'CO2', 'uatm', cast(coalesce(nullif('878.0', 'nan'), '0') as float), 839)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41345', 'CO2', 'uatm', cast(coalesce(nullif('750.0', 'nan'), '0') as float), 840)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41346', 'CO2', 'uatm', cast(coalesce(nullif('890.0', 'nan'), '0') as float), 841)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41346', 'CO2', 'uatm', cast(coalesce(nullif('780.0', 'nan'), '0') as float), 841)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41347', 'CO2', 'uatm', cast(coalesce(nullif('708.0', 'nan'), '0') as float), 842)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41347', 'CO2', 'uatm', cast(coalesce(nullif('618.0', 'nan'), '0') as float), 843)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41347', 'CO2', 'uatm', cast(coalesce(nullif('1544.0', 'nan'), '0') as float), 844)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41347', 'CO2', 'uatm', cast(coalesce(nullif('524.0', 'nan'), '0') as float), 845)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41348', 'CO2', 'uatm', cast(coalesce(nullif('2979.0', 'nan'), '0') as float), 846)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41348', 'CO2', 'uatm', cast(coalesce(nullif('1907.0', 'nan'), '0') as float), 847)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41348', 'CO2', 'uatm', cast(coalesce(nullif('542.0', 'nan'), '0') as float), 848)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41566', 'CO2', 'uatm', cast(coalesce(nullif('2555.0', 'nan'), '0') as float), 849)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41567', 'CO2', 'uatm', cast(coalesce(nullif('617.0', 'nan'), '0') as float), 850)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41568', 'CO2', 'uatm', cast(coalesce(nullif('681.0', 'nan'), '0') as float), 851)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41569', 'CO2', 'uatm', cast(coalesce(nullif('816.0', 'nan'), '0') as float), 853)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41571', 'CO2', 'uatm', cast(coalesce(nullif('300.0', 'nan'), '0') as float), 854)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41572', 'CO2', 'uatm', cast(coalesce(nullif('707.0', 'nan'), '0') as float), 855)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41576', 'CO2', 'uatm', cast(coalesce(nullif('2600.0', 'nan'), '0') as float), 856)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41574', 'CO2', 'uatm', cast(coalesce(nullif('1602.0', 'nan'), '0') as float), 857)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41588', 'CO2', 'uatm', cast(coalesce(nullif('462.0', 'nan'), '0') as float), 858)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41592', 'CO2', 'uatm', cast(coalesce(nullif('2529.0', 'nan'), '0') as float), 859)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41593', 'CO2', 'uatm', cast(coalesce(nullif('331.0', 'nan'), '0') as float), 860)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41594', 'CO2', 'uatm', cast(coalesce(nullif('1705.0', 'nan'), '0') as float), 861)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41595', 'CO2', 'uatm', cast(coalesce(nullif('1022.0', 'nan'), '0') as float), 862)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41598', 'CO2', 'uatm', cast(coalesce(nullif('6049.0', 'nan'), '0') as float), 863)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41599', 'CO2', 'uatm', cast(coalesce(nullif('6647.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41600', 'CO2', 'uatm', cast(coalesce(nullif('1657.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41600', 'CO2', 'uatm', cast(coalesce(nullif('1644.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41600', 'CO2', 'uatm', cast(coalesce(nullif('1516.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41600', 'CO2', 'uatm', cast(coalesce(nullif('1397.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41600', 'CO2', 'uatm', cast(coalesce(nullif('1339.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41600', 'CO2', 'uatm', cast(coalesce(nullif('1288.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41600', 'CO2', 'uatm', cast(coalesce(nullif('1190.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41601', 'CO2', 'uatm', cast(coalesce(nullif('1177.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41601', 'CO2', 'uatm', cast(coalesce(nullif('1247.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41601', 'CO2', 'uatm', cast(coalesce(nullif('1307.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41601', 'CO2', 'uatm', cast(coalesce(nullif('1433.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41601', 'CO2', 'uatm', cast(coalesce(nullif('1418.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41601', 'CO2', 'uatm', cast(coalesce(nullif('1414.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41601', 'CO2', 'uatm', cast(coalesce(nullif('1378.0', 'nan'), '0') as float), 864)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41602', 'CO2', 'uatm', cast(coalesce(nullif('1099.0', 'nan'), '0') as float), 865)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41299', 'CO2', 'uatm', cast(coalesce(nullif('1602.0', 'nan'), '0') as float), 866)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41350', 'CO2', 'uatm', cast(coalesce(nullif('1591.0', 'nan'), '0') as float), 867)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41575', 'CO2', 'uatm', cast(coalesce(nullif('1135.0', 'nan'), '0') as float), 867)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41586', 'CO2', 'uatm', cast(coalesce(nullif('1172.0', 'nan'), '0') as float), 867)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41602', 'CO2', 'uatm', cast(coalesce(nullif('1099.0', 'nan'), '0') as float), 867)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40944', 'CO2', 'uatm', cast(coalesce(nullif('2274.0', 'nan'), '0') as float), 868)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40943', 'CO2', 'uatm', cast(coalesce(nullif('3190.0', 'nan'), '0') as float), 869)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40947', 'CO2', 'uatm', cast(coalesce(nullif('2583.0', 'nan'), '0') as float), 870)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40942', 'CO2', 'uatm', cast(coalesce(nullif('2259.0', 'nan'), '0') as float), 874)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40946', 'CO2', 'uatm', cast(coalesce(nullif('892.0', 'nan'), '0') as float), 875)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40948', 'CO2', 'uatm', cast(coalesce(nullif('1140.0', 'nan'), '0') as float), 876)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40969', 'CO2', 'uatm', cast(coalesce(nullif('1316.0', 'nan'), '0') as float), 878)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40956', 'CO2', 'uatm', cast(coalesce(nullif('2185.0', 'nan'), '0') as float), 879)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40948', 'CO2', 'uatm', cast(coalesce(nullif('1910.0', 'nan'), '0') as float), 881)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40955', 'CO2', 'uatm', cast(coalesce(nullif('1996.0', 'nan'), '0') as float), 882)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40955', 'CO2', 'uatm', cast(coalesce(nullif('2805.0', 'nan'), '0') as float), 883)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40958', 'CO2', 'uatm', cast(coalesce(nullif('1285.0', 'nan'), '0') as float), 885)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40960', 'CO2', 'uatm', cast(coalesce(nullif('589.0', 'nan'), '0') as float), 887)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40961', 'CO2', 'uatm', cast(coalesce(nullif('508.0', 'nan'), '0') as float), 888)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40961', 'CO2', 'uatm', cast(coalesce(nullif('1471.0', 'nan'), '0') as float), 889)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40964', 'CO2', 'uatm', cast(coalesce(nullif('1813.0', 'nan'), '0') as float), 891)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40963', 'CO2', 'uatm', cast(coalesce(nullif('2669.0', 'nan'), '0') as float), 892)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40962', 'CO2', 'uatm', cast(coalesce(nullif('508.0', 'nan'), '0') as float), 893)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40960', 'CO2', 'uatm', cast(coalesce(nullif('1022.0', 'nan'), '0') as float), 897)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40959', 'CO2', 'uatm', cast(coalesce(nullif('878.0', 'nan'), '0') as float), 899)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40957', 'CO2', 'uatm', cast(coalesce(nullif('3847.0', 'nan'), '0') as float), 900)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40939', 'CO2', 'uatm', cast(coalesce(nullif('836.0', 'nan'), '0') as float), 901)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40939', 'CO2', 'uatm', cast(coalesce(nullif('1743.0', 'nan'), '0') as float), 902)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40931', 'CO2', 'uatm', cast(coalesce(nullif('1225.0', 'nan'), '0') as float), 908)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40929', 'CO2', 'uatm', cast(coalesce(nullif('2062.0', 'nan'), '0') as float), 909)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40932', 'CO2', 'uatm', cast(coalesce(nullif('2255.0', 'nan'), '0') as float), 910)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40933', 'CO2', 'uatm', cast(coalesce(nullif('1365.0', 'nan'), '0') as float), 913)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40933', 'CO2', 'uatm', cast(coalesce(nullif('1710.0', 'nan'), '0') as float), 914)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40936', 'CO2', 'uatm', cast(coalesce(nullif('922.0', 'nan'), '0') as float), 917)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40936', 'CO2', 'uatm', cast(coalesce(nullif('819.0', 'nan'), '0') as float), 918)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40934', 'CO2', 'uatm', cast(coalesce(nullif('775.0', 'nan'), '0') as float), 920)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40931', 'CO2', 'uatm', cast(coalesce(nullif('1257.0', 'nan'), '0') as float), 921)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40937', 'CO2', 'uatm', cast(coalesce(nullif('3821.0', 'nan'), '0') as float), 930)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40935', 'CO2', 'uatm', cast(coalesce(nullif('3077.0', 'nan'), '0') as float), 931)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40940', 'CO2', 'uatm', cast(coalesce(nullif('545.0', 'nan'), '0') as float), 932)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40963', 'CO2', 'uatm', cast(coalesce(nullif('1685.0', 'nan'), '0') as float), 933)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41155', 'CO2', 'uatm', cast(coalesce(nullif('9497.0', 'nan'), '0') as float), 934)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41155', 'CO2', 'uatm', cast(coalesce(nullif('6705.0', 'nan'), '0') as float), 935)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41156', 'CO2', 'uatm', cast(coalesce(nullif('1739.0', 'nan'), '0') as float), 937)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41157', 'CO2', 'uatm', cast(coalesce(nullif('1366.0', 'nan'), '0') as float), 938)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41158', 'CO2', 'uatm', cast(coalesce(nullif('730.0', 'nan'), '0') as float), 939)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41158', 'CO2', 'uatm', cast(coalesce(nullif('546.0', 'nan'), '0') as float), 940)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41159', 'CO2', 'uatm', cast(coalesce(nullif('1747.0', 'nan'), '0') as float), 941)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41160', 'CO2', 'uatm', cast(coalesce(nullif('1699.0', 'nan'), '0') as float), 942)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41161', 'CO2', 'uatm', cast(coalesce(nullif('728.0', 'nan'), '0') as float), 943)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41195', 'CO2', 'uatm', cast(coalesce(nullif('433.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41196', 'CO2', 'uatm', cast(coalesce(nullif('923.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41197', 'CO2', 'uatm', cast(coalesce(nullif('1570.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41198', 'CO2', 'uatm', cast(coalesce(nullif('1487.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41199', 'CO2', 'uatm', cast(coalesce(nullif('1714.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41200', 'CO2', 'uatm', cast(coalesce(nullif('1230.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41201', 'CO2', 'uatm', cast(coalesce(nullif('934.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41202', 'CO2', 'uatm', cast(coalesce(nullif('1069.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41203', 'CO2', 'uatm', cast(coalesce(nullif('811.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41204', 'CO2', 'uatm', cast(coalesce(nullif('733.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41205', 'CO2', 'uatm', cast(coalesce(nullif('695.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41206', 'CO2', 'uatm', cast(coalesce(nullif('764.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41207', 'CO2', 'uatm', cast(coalesce(nullif('797.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41208', 'CO2', 'uatm', cast(coalesce(nullif('727.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41209', 'CO2', 'uatm', cast(coalesce(nullif('684.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41210', 'CO2', 'uatm', cast(coalesce(nullif('1043.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41211', 'CO2', 'uatm', cast(coalesce(nullif('790.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41212', 'CO2', 'uatm', cast(coalesce(nullif('753.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41213', 'CO2', 'uatm', cast(coalesce(nullif('681.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41214', 'CO2', 'uatm', cast(coalesce(nullif('764.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41215', 'CO2', 'uatm', cast(coalesce(nullif('672.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41216', 'CO2', 'uatm', cast(coalesce(nullif('678.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41217', 'CO2', 'uatm', cast(coalesce(nullif('638.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41218', 'CO2', 'uatm', cast(coalesce(nullif('1131.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41219', 'CO2', 'uatm', cast(coalesce(nullif('2099.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41220', 'CO2', 'uatm', cast(coalesce(nullif('2129.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41221', 'CO2', 'uatm', cast(coalesce(nullif('1571.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41222', 'CO2', 'uatm', cast(coalesce(nullif('1201.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41223', 'CO2', 'uatm', cast(coalesce(nullif('1254.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41224', 'CO2', 'uatm', cast(coalesce(nullif('2118.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41225', 'CO2', 'uatm', cast(coalesce(nullif('1683.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41226', 'CO2', 'uatm', cast(coalesce(nullif('1279.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41227', 'CO2', 'uatm', cast(coalesce(nullif('1033.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41228', 'CO2', 'uatm', cast(coalesce(nullif('904.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41229', 'CO2', 'uatm', cast(coalesce(nullif('876.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41230', 'CO2', 'uatm', cast(coalesce(nullif('797.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41231', 'CO2', 'uatm', cast(coalesce(nullif('1169.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41396', 'CO2', 'uatm', cast(coalesce(nullif('975.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41397', 'CO2', 'uatm', cast(coalesce(nullif('904.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41398', 'CO2', 'uatm', cast(coalesce(nullif('852.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41399', 'CO2', 'uatm', cast(coalesce(nullif('873.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41400', 'CO2', 'uatm', cast(coalesce(nullif('857.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41401', 'CO2', 'uatm', cast(coalesce(nullif('901.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41402', 'CO2', 'uatm', cast(coalesce(nullif('829.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41403', 'CO2', 'uatm', cast(coalesce(nullif('900.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41404', 'CO2', 'uatm', cast(coalesce(nullif('883.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41405', 'CO2', 'uatm', cast(coalesce(nullif('828.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41406', 'CO2', 'uatm', cast(coalesce(nullif('815.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41407', 'CO2', 'uatm', cast(coalesce(nullif('802.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41408', 'CO2', 'uatm', cast(coalesce(nullif('784.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41409', 'CO2', 'uatm', cast(coalesce(nullif('809.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41410', 'CO2', 'uatm', cast(coalesce(nullif('807.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41411', 'CO2', 'uatm', cast(coalesce(nullif('865.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41412', 'CO2', 'uatm', cast(coalesce(nullif('804.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41413', 'CO2', 'uatm', cast(coalesce(nullif('858.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41414', 'CO2', 'uatm', cast(coalesce(nullif('860.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41415', 'CO2', 'uatm', cast(coalesce(nullif('890.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41416', 'CO2', 'uatm', cast(coalesce(nullif('964.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41417', 'CO2', 'uatm', cast(coalesce(nullif('837.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41418', 'CO2', 'uatm', cast(coalesce(nullif('860.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41419', 'CO2', 'uatm', cast(coalesce(nullif('798.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41420', 'CO2', 'uatm', cast(coalesce(nullif('834.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41421', 'CO2', 'uatm', cast(coalesce(nullif('812.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41422', 'CO2', 'uatm', cast(coalesce(nullif('923.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41423', 'CO2', 'uatm', cast(coalesce(nullif('866.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41424', 'CO2', 'uatm', cast(coalesce(nullif('829.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41425', 'CO2', 'uatm', cast(coalesce(nullif('836.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41426', 'CO2', 'uatm', cast(coalesce(nullif('779.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41427', 'CO2', 'uatm', cast(coalesce(nullif('798.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41428', 'CO2', 'uatm', cast(coalesce(nullif('799.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41731', 'CO2', 'uatm', cast(coalesce(nullif('844.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41732', 'CO2', 'uatm', cast(coalesce(nullif('770.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41733', 'CO2', 'uatm', cast(coalesce(nullif('847.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41734', 'CO2', 'uatm', cast(coalesce(nullif('739.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41735', 'CO2', 'uatm', cast(coalesce(nullif('697.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41736', 'CO2', 'uatm', cast(coalesce(nullif('801.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41737', 'CO2', 'uatm', cast(coalesce(nullif('806.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41738', 'CO2', 'uatm', cast(coalesce(nullif('1065.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41739', 'CO2', 'uatm', cast(coalesce(nullif('949.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41740', 'CO2', 'uatm', cast(coalesce(nullif('2442.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41741', 'CO2', 'uatm', cast(coalesce(nullif('1611.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41742', 'CO2', 'uatm', cast(coalesce(nullif('1214.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41743', 'CO2', 'uatm', cast(coalesce(nullif('1064.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41744', 'CO2', 'uatm', cast(coalesce(nullif('1001.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41745', 'CO2', 'uatm', cast(coalesce(nullif('1320.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41746', 'CO2', 'uatm', cast(coalesce(nullif('1130.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41747', 'CO2', 'uatm', cast(coalesce(nullif('1701.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41748', 'CO2', 'uatm', cast(coalesce(nullif('2088.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41749', 'CO2', 'uatm', cast(coalesce(nullif('1861.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41750', 'CO2', 'uatm', cast(coalesce(nullif('1495.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41751', 'CO2', 'uatm', cast(coalesce(nullif('1201.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41752', 'CO2', 'uatm', cast(coalesce(nullif('1114.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41753', 'CO2', 'uatm', cast(coalesce(nullif('1189.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41754', 'CO2', 'uatm', cast(coalesce(nullif('1048.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41755', 'CO2', 'uatm', cast(coalesce(nullif('977.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41756', 'CO2', 'uatm', cast(coalesce(nullif('1085.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41757', 'CO2', 'uatm', cast(coalesce(nullif('879.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41758', 'CO2', 'uatm', cast(coalesce(nullif('1020.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41759', 'CO2', 'uatm', cast(coalesce(nullif('1090.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41760', 'CO2', 'uatm', cast(coalesce(nullif('1019.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41761', 'CO2', 'uatm', cast(coalesce(nullif('1029.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41762', 'CO2', 'uatm', cast(coalesce(nullif('985.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41763', 'CO2', 'uatm', cast(coalesce(nullif('915.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41764', 'CO2', 'uatm', cast(coalesce(nullif('935.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41765', 'CO2', 'uatm', cast(coalesce(nullif('1014.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41766', 'CO2', 'uatm', cast(coalesce(nullif('960.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41767', 'CO2', 'uatm', cast(coalesce(nullif('923.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41768', 'CO2', 'uatm', cast(coalesce(nullif('948.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41769', 'CO2', 'uatm', cast(coalesce(nullif('889.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41770', 'CO2', 'uatm', cast(coalesce(nullif('910.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41771', 'CO2', 'uatm', cast(coalesce(nullif('1069.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41772', 'CO2', 'uatm', cast(coalesce(nullif('1071.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41773', 'CO2', 'uatm', cast(coalesce(nullif('1435.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41774', 'CO2', 'uatm', cast(coalesce(nullif('963.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41775', 'CO2', 'uatm', cast(coalesce(nullif('924.0', 'nan'), '0') as float), 1015)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40856', 'CO2', 'uatm', cast(coalesce(nullif('2070.0', 'nan'), '0') as float), 1016)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41200', 'CO2', 'uatm', cast(coalesce(nullif('1447.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41201', 'CO2', 'uatm', cast(coalesce(nullif('1736.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41202', 'CO2', 'uatm', cast(coalesce(nullif('1877.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41204', 'CO2', 'uatm', cast(coalesce(nullif('2410.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41205', 'CO2', 'uatm', cast(coalesce(nullif('1999.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41206', 'CO2', 'uatm', cast(coalesce(nullif('1675.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41207', 'CO2', 'uatm', cast(coalesce(nullif('1753.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41208', 'CO2', 'uatm', cast(coalesce(nullif('1385.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41209', 'CO2', 'uatm', cast(coalesce(nullif('1023.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41210', 'CO2', 'uatm', cast(coalesce(nullif('994.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41211', 'CO2', 'uatm', cast(coalesce(nullif('1257.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41212', 'CO2', 'uatm', cast(coalesce(nullif('1047.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41213', 'CO2', 'uatm', cast(coalesce(nullif('1261.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41214', 'CO2', 'uatm', cast(coalesce(nullif('1274.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41215', 'CO2', 'uatm', cast(coalesce(nullif('1000.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41216', 'CO2', 'uatm', cast(coalesce(nullif('1193.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41217', 'CO2', 'uatm', cast(coalesce(nullif('1360.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41218', 'CO2', 'uatm', cast(coalesce(nullif('1205.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41219', 'CO2', 'uatm', cast(coalesce(nullif('1280.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41220', 'CO2', 'uatm', cast(coalesce(nullif('1352.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41221', 'CO2', 'uatm', cast(coalesce(nullif('1121.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41222', 'CO2', 'uatm', cast(coalesce(nullif('1928.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41223', 'CO2', 'uatm', cast(coalesce(nullif('2626.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41224', 'CO2', 'uatm', cast(coalesce(nullif('3269.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41225', 'CO2', 'uatm', cast(coalesce(nullif('3276.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41226', 'CO2', 'uatm', cast(coalesce(nullif('2984.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41227', 'CO2', 'uatm', cast(coalesce(nullif('2724.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41229', 'CO2', 'uatm', cast(coalesce(nullif('3800.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41230', 'CO2', 'uatm', cast(coalesce(nullif('2458.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41231', 'CO2', 'uatm', cast(coalesce(nullif('2937.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41232', 'CO2', 'uatm', cast(coalesce(nullif('2326.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41233', 'CO2', 'uatm', cast(coalesce(nullif('2204.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41234', 'CO2', 'uatm', cast(coalesce(nullif('1861.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41235', 'CO2', 'uatm', cast(coalesce(nullif('2067.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41236', 'CO2', 'uatm', cast(coalesce(nullif('2546.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41396', 'CO2', 'uatm', cast(coalesce(nullif('6016.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41397', 'CO2', 'uatm', cast(coalesce(nullif('6014.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41398', 'CO2', 'uatm', cast(coalesce(nullif('4609.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41399', 'CO2', 'uatm', cast(coalesce(nullif('5275.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41400', 'CO2', 'uatm', cast(coalesce(nullif('5071.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41401', 'CO2', 'uatm', cast(coalesce(nullif('4864.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41402', 'CO2', 'uatm', cast(coalesce(nullif('3544.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41403', 'CO2', 'uatm', cast(coalesce(nullif('4187.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41404', 'CO2', 'uatm', cast(coalesce(nullif('3881.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41405', 'CO2', 'uatm', cast(coalesce(nullif('3637.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41406', 'CO2', 'uatm', cast(coalesce(nullif('4369.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41407', 'CO2', 'uatm', cast(coalesce(nullif('4115.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41408', 'CO2', 'uatm', cast(coalesce(nullif('3748.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41409', 'CO2', 'uatm', cast(coalesce(nullif('3985.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41410', 'CO2', 'uatm', cast(coalesce(nullif('4035.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41411', 'CO2', 'uatm', cast(coalesce(nullif('3829.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41412', 'CO2', 'uatm', cast(coalesce(nullif('3810.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41413', 'CO2', 'uatm', cast(coalesce(nullif('4249.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41414', 'CO2', 'uatm', cast(coalesce(nullif('3476.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41415', 'CO2', 'uatm', cast(coalesce(nullif('3282.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41416', 'CO2', 'uatm', cast(coalesce(nullif('3471.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41417', 'CO2', 'uatm', cast(coalesce(nullif('3550.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41418', 'CO2', 'uatm', cast(coalesce(nullif('3406.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41419', 'CO2', 'uatm', cast(coalesce(nullif('3285.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41420', 'CO2', 'uatm', cast(coalesce(nullif('3083.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41421', 'CO2', 'uatm', cast(coalesce(nullif('3098.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41422', 'CO2', 'uatm', cast(coalesce(nullif('2918.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41423', 'CO2', 'uatm', cast(coalesce(nullif('2788.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41424', 'CO2', 'uatm', cast(coalesce(nullif('2410.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41425', 'CO2', 'uatm', cast(coalesce(nullif('2431.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41426', 'CO2', 'uatm', cast(coalesce(nullif('2501.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41427', 'CO2', 'uatm', cast(coalesce(nullif('1949.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41428', 'CO2', 'uatm', cast(coalesce(nullif('1526.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41429', 'CO2', 'uatm', cast(coalesce(nullif('1665.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41430', 'CO2', 'uatm', cast(coalesce(nullif('1647.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41431', 'CO2', 'uatm', cast(coalesce(nullif('1606.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41432', 'CO2', 'uatm', cast(coalesce(nullif('1327.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41433', 'CO2', 'uatm', cast(coalesce(nullif('1261.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41434', 'CO2', 'uatm', cast(coalesce(nullif('1104.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41435', 'CO2', 'uatm', cast(coalesce(nullif('1084.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41436', 'CO2', 'uatm', cast(coalesce(nullif('1024.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41437', 'CO2', 'uatm', cast(coalesce(nullif('937.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41438', 'CO2', 'uatm', cast(coalesce(nullif('1024.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41439', 'CO2', 'uatm', cast(coalesce(nullif('1072.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41440', 'CO2', 'uatm', cast(coalesce(nullif('1081.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41441', 'CO2', 'uatm', cast(coalesce(nullif('1054.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41442', 'CO2', 'uatm', cast(coalesce(nullif('969.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41443', 'CO2', 'uatm', cast(coalesce(nullif('907.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41444', 'CO2', 'uatm', cast(coalesce(nullif('880.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41445', 'CO2', 'uatm', cast(coalesce(nullif('917.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41446', 'CO2', 'uatm', cast(coalesce(nullif('845.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41447', 'CO2', 'uatm', cast(coalesce(nullif('904.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41735', 'CO2', 'uatm', cast(coalesce(nullif('1063.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41736', 'CO2', 'uatm', cast(coalesce(nullif('1052.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41737', 'CO2', 'uatm', cast(coalesce(nullif('1004.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41738', 'CO2', 'uatm', cast(coalesce(nullif('1030.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41739', 'CO2', 'uatm', cast(coalesce(nullif('949.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41740', 'CO2', 'uatm', cast(coalesce(nullif('865.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41741', 'CO2', 'uatm', cast(coalesce(nullif('944.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41742', 'CO2', 'uatm', cast(coalesce(nullif('1301.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41743', 'CO2', 'uatm', cast(coalesce(nullif('1577.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41744', 'CO2', 'uatm', cast(coalesce(nullif('1735.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41745', 'CO2', 'uatm', cast(coalesce(nullif('1796.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41746', 'CO2', 'uatm', cast(coalesce(nullif('2097.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41747', 'CO2', 'uatm', cast(coalesce(nullif('1785.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41748', 'CO2', 'uatm', cast(coalesce(nullif('1532.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41749', 'CO2', 'uatm', cast(coalesce(nullif('1293.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41750', 'CO2', 'uatm', cast(coalesce(nullif('1222.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41751', 'CO2', 'uatm', cast(coalesce(nullif('1767.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41752', 'CO2', 'uatm', cast(coalesce(nullif('2576.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41753', 'CO2', 'uatm', cast(coalesce(nullif('2840.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41754', 'CO2', 'uatm', cast(coalesce(nullif('2309.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41755', 'CO2', 'uatm', cast(coalesce(nullif('1839.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41756', 'CO2', 'uatm', cast(coalesce(nullif('1717.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41757', 'CO2', 'uatm', cast(coalesce(nullif('1421.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41758', 'CO2', 'uatm', cast(coalesce(nullif('1317.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41759', 'CO2', 'uatm', cast(coalesce(nullif('1241.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41760', 'CO2', 'uatm', cast(coalesce(nullif('1240.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41761', 'CO2', 'uatm', cast(coalesce(nullif('1231.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41762', 'CO2', 'uatm', cast(coalesce(nullif('1190.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41763', 'CO2', 'uatm', cast(coalesce(nullif('1169.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41764', 'CO2', 'uatm', cast(coalesce(nullif('1109.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41765', 'CO2', 'uatm', cast(coalesce(nullif('1082.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41766', 'CO2', 'uatm', cast(coalesce(nullif('1117.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41767', 'CO2', 'uatm', cast(coalesce(nullif('1119.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41768', 'CO2', 'uatm', cast(coalesce(nullif('1049.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41769', 'CO2', 'uatm', cast(coalesce(nullif('1056.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41770', 'CO2', 'uatm', cast(coalesce(nullif('1082.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41771', 'CO2', 'uatm', cast(coalesce(nullif('1089.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41772', 'CO2', 'uatm', cast(coalesce(nullif('1001.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41773', 'CO2', 'uatm', cast(coalesce(nullif('1136.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41774', 'CO2', 'uatm', cast(coalesce(nullif('1030.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41775', 'CO2', 'uatm', cast(coalesce(nullif('1008.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41776', 'CO2', 'uatm', cast(coalesce(nullif('1031.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41777', 'CO2', 'uatm', cast(coalesce(nullif('988.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41778', 'CO2', 'uatm', cast(coalesce(nullif('903.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41779', 'CO2', 'uatm', cast(coalesce(nullif('836.0', 'nan'), '0') as float), 1017)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40848', 'CO2', 'uatm', cast(coalesce(nullif('5596.0', 'nan'), '0') as float), 1018)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41024', 'CO2', 'uatm', cast(coalesce(nullif('2134.0', 'nan'), '0') as float), 1018)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40848', 'CO2', 'uatm', cast(coalesce(nullif('6329.0', 'nan'), '0') as float), 1019)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40850', 'CO2', 'uatm', cast(coalesce(nullif('1831.0', 'nan'), '0') as float), 1020)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41023', 'CO2', 'uatm', cast(coalesce(nullif('1559.0', 'nan'), '0') as float), 1020)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40852', 'CO2', 'uatm', cast(coalesce(nullif('1499.0', 'nan'), '0') as float), 1021)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41026', 'CO2', 'uatm', cast(coalesce(nullif('1626.0', 'nan'), '0') as float), 1021)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40867', 'CO2', 'uatm', cast(coalesce(nullif('1616.0', 'nan'), '0') as float), 1022)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41025', 'CO2', 'uatm', cast(coalesce(nullif('1790.0', 'nan'), '0') as float), 1022)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40866', 'CO2', 'uatm', cast(coalesce(nullif('1109.0', 'nan'), '0') as float), 1023)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41020', 'CO2', 'uatm', cast(coalesce(nullif('1660.0', 'nan'), '0') as float), 1023)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40862', 'CO2', 'uatm', cast(coalesce(nullif('9075.0', 'nan'), '0') as float), 1024)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41017', 'CO2', 'uatm', cast(coalesce(nullif('10311.0', 'nan'), '0') as float), 1024)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40868', 'CO2', 'uatm', cast(coalesce(nullif('9590.0', 'nan'), '0') as float), 1024)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40868', 'CO2', 'uatm', cast(coalesce(nullif('10405.0', 'nan'), '0') as float), 1024)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40868', 'CO2', 'uatm', cast(coalesce(nullif('9456.0', 'nan'), '0') as float), 1024)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40868', 'CO2', 'uatm', cast(coalesce(nullif('9636.0', 'nan'), '0') as float), 1024)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40862', 'CO2', 'uatm', cast(coalesce(nullif('2775.0', 'nan'), '0') as float), 1025)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41017', 'CO2', 'uatm', cast(coalesce(nullif('2694.0', 'nan'), '0') as float), 1025)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40863', 'CO2', 'uatm', cast(coalesce(nullif('1364.0', 'nan'), '0') as float), 1026)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41019', 'CO2', 'uatm', cast(coalesce(nullif('916.0', 'nan'), '0') as float), 1026)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40863', 'CO2', 'uatm', cast(coalesce(nullif('1031.0', 'nan'), '0') as float), 1027)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41019', 'CO2', 'uatm', cast(coalesce(nullif('1775.0', 'nan'), '0') as float), 1027)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41018', 'CO2', 'uatm', cast(coalesce(nullif('1207.0', 'nan'), '0') as float), 1028)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40861', 'CO2', 'uatm', cast(coalesce(nullif('1523.0', 'nan'), '0') as float), 1029)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41027', 'CO2', 'uatm', cast(coalesce(nullif('1336.0', 'nan'), '0') as float), 1029)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40864', 'CO2', 'uatm', cast(coalesce(nullif('1277.0', 'nan'), '0') as float), 1030)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41018', 'CO2', 'uatm', cast(coalesce(nullif('1031.0', 'nan'), '0') as float), 1030)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40859', 'CO2', 'uatm', cast(coalesce(nullif('1390.0', 'nan'), '0') as float), 1031)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41028', 'CO2', 'uatm', cast(coalesce(nullif('964.0', 'nan'), '0') as float), 1031)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40859', 'CO2', 'uatm', cast(coalesce(nullif('1196.0', 'nan'), '0') as float), 1032)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40860', 'CO2', 'uatm', cast(coalesce(nullif('1331.0', 'nan'), '0') as float), 1033)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40858', 'CO2', 'uatm', cast(coalesce(nullif('1414.0', 'nan'), '0') as float), 1034)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40857', 'CO2', 'uatm', cast(coalesce(nullif('2218.0', 'nan'), '0') as float), 1036)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40850', 'CO2', 'uatm', cast(coalesce(nullif('1148.0', 'nan'), '0') as float), 1037)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41023', 'CO2', 'uatm', cast(coalesce(nullif('896.0', 'nan'), '0') as float), 1037)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40851', 'CO2', 'uatm', cast(coalesce(nullif('884.0', 'nan'), '0') as float), 1038)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41022', 'CO2', 'uatm', cast(coalesce(nullif('1558.0', 'nan'), '0') as float), 1038)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40851', 'CO2', 'uatm', cast(coalesce(nullif('1193.0', 'nan'), '0') as float), 1039)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40852', 'CO2', 'uatm', cast(coalesce(nullif('1018.0', 'nan'), '0') as float), 1040)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40861', 'CO2', 'uatm', cast(coalesce(nullif('608.0', 'nan'), '0') as float), 1041)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40866', 'CO2', 'uatm', cast(coalesce(nullif('2354.0', 'nan'), '0') as float), 1042)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41020', 'CO2', 'uatm', cast(coalesce(nullif('1286.0', 'nan'), '0') as float), 1042)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39112', 'CO2', 'uatm', cast(coalesce(nullif('2950.0', 'nan'), '0') as float), 1048)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39114', 'CO2', 'uatm', cast(coalesce(nullif('3180.0', 'nan'), '0') as float), 1049)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39116', 'CO2', 'uatm', cast(coalesce(nullif('2880.0', 'nan'), '0') as float), 1050)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39116', 'CO2', 'uatm', cast(coalesce(nullif('2750.0', 'nan'), '0') as float), 1051)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39117', 'CO2', 'uatm', cast(coalesce(nullif('2870.0', 'nan'), '0') as float), 1052)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39117', 'CO2', 'uatm', cast(coalesce(nullif('2770.0', 'nan'), '0') as float), 1053)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39118', 'CO2', 'uatm', cast(coalesce(nullif('2630.0', 'nan'), '0') as float), 1054)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39118', 'CO2', 'uatm', cast(coalesce(nullif('2290.0', 'nan'), '0') as float), 1055)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39118', 'CO2', 'uatm', cast(coalesce(nullif('2300.0', 'nan'), '0') as float), 1056)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39119', 'CO2', 'uatm', cast(coalesce(nullif('1600.0', 'nan'), '0') as float), 1057)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39120', 'CO2', 'uatm', cast(coalesce(nullif('2500.0', 'nan'), '0') as float), 1058)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39121', 'CO2', 'uatm', cast(coalesce(nullif('2300.0', 'nan'), '0') as float), 1059)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39122', 'CO2', 'uatm', cast(coalesce(nullif('2280.0', 'nan'), '0') as float), 1060)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39115', 'CO2', 'uatm', cast(coalesce(nullif('70.0', 'nan'), '0') as float), 1061)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39115', 'CO2', 'uatm', cast(coalesce(nullif('70.0', 'nan'), '0') as float), 1062)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39115', 'CO2', 'uatm', cast(coalesce(nullif('520.0', 'nan'), '0') as float), 1063)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39119', 'CO2', 'uatm', cast(coalesce(nullif('1070.0', 'nan'), '0') as float), 1064)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39113', 'CO2', 'uatm', cast(coalesce(nullif('2850.0', 'nan'), '0') as float), 1065)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39114', 'CO2', 'uatm', cast(coalesce(nullif('7440.0', 'nan'), '0') as float), 1066)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39120', 'CO2', 'uatm', cast(coalesce(nullif('2700.0', 'nan'), '0') as float), 1067)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39121', 'CO2', 'uatm', cast(coalesce(nullif('6770.0', 'nan'), '0') as float), 1068)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39112', 'CO2', 'uatm', cast(coalesce(nullif('150.0', 'nan'), '0') as float), 1069)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39113', 'CO2', 'uatm', cast(coalesce(nullif('600.0', 'nan'), '0') as float), 1070)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39113', 'CO2', 'uatm', cast(coalesce(nullif('650.0', 'nan'), '0') as float), 1071)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39113', 'CO2', 'uatm', cast(coalesce(nullif('500.0', 'nan'), '0') as float), 1072)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39114', 'CO2', 'uatm', cast(coalesce(nullif('810.0', 'nan'), '0') as float), 1073)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39114', 'CO2', 'uatm', cast(coalesce(nullif('600.0', 'nan'), '0') as float), 1074)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39117', 'CO2', 'uatm', cast(coalesce(nullif('230.0', 'nan'), '0') as float), 1075)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39580', 'CO2', 'uatm', cast(coalesce(nullif('5850.0', 'nan'), '0') as float), 1076)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39582', 'CO2', 'uatm', cast(coalesce(nullif('5780.0', 'nan'), '0') as float), 1077)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39580', 'CO2', 'uatm', cast(coalesce(nullif('4600.0', 'nan'), '0') as float), 1078)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39579', 'CO2', 'uatm', cast(coalesce(nullif('10100.0', 'nan'), '0') as float), 1079)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39581', 'CO2', 'uatm', cast(coalesce(nullif('8400.0', 'nan'), '0') as float), 1080)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39581', 'CO2', 'uatm', cast(coalesce(nullif('5900.0', 'nan'), '0') as float), 1081)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39582', 'CO2', 'uatm', cast(coalesce(nullif('7200.0', 'nan'), '0') as float), 1082)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39582', 'CO2', 'uatm', cast(coalesce(nullif('5550.0', 'nan'), '0') as float), 1083)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39582', 'CO2', 'uatm', cast(coalesce(nullif('2630.0', 'nan'), '0') as float), 1084)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39583', 'CO2', 'uatm', cast(coalesce(nullif('6020.0', 'nan'), '0') as float), 1085)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39583', 'CO2', 'uatm', cast(coalesce(nullif('4260.0', 'nan'), '0') as float), 1086)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39583', 'CO2', 'uatm', cast(coalesce(nullif('4400.0', 'nan'), '0') as float), 1087)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('7387.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('7607.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('7013.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('7609.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('7305.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('7466.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('7538.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('7048.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('7104.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('7144.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('6973.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('6962.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('5214.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('4740.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('4674.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('3954.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('3932.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('4355.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('4350.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('5005.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('5345.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('5606.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39584', 'CO2', 'uatm', cast(coalesce(nullif('5519.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39585', 'CO2', 'uatm', cast(coalesce(nullif('5772.0', 'nan'), '0') as float), 1088)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39730', 'CO2', 'uatm', cast(coalesce(nullif('2780.0', 'nan'), '0') as float), 1089)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39731', 'CO2', 'uatm', cast(coalesce(nullif('2500.0', 'nan'), '0') as float), 1090)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39732', 'CO2', 'uatm', cast(coalesce(nullif('3090.0', 'nan'), '0') as float), 1091)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39732', 'CO2', 'uatm', cast(coalesce(nullif('2950.0', 'nan'), '0') as float), 1092)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39733', 'CO2', 'uatm', cast(coalesce(nullif('3050.0', 'nan'), '0') as float), 1093)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39733', 'CO2', 'uatm', cast(coalesce(nullif('2860.0', 'nan'), '0') as float), 1094)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39729', 'CO2', 'uatm', cast(coalesce(nullif('2700.0', 'nan'), '0') as float), 1095)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39730', 'CO2', 'uatm', cast(coalesce(nullif('1300.0', 'nan'), '0') as float), 1096)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39732', 'CO2', 'uatm', cast(coalesce(nullif('2030.0', 'nan'), '0') as float), 1097)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39728', 'CO2', 'uatm', cast(coalesce(nullif('70.0', 'nan'), '0') as float), 1098)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39728', 'CO2', 'uatm', cast(coalesce(nullif('90.0', 'nan'), '0') as float), 1099)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39732', 'CO2', 'uatm', cast(coalesce(nullif('750.0', 'nan'), '0') as float), 1100)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39734', 'CO2', 'uatm', cast(coalesce(nullif('1000.0', 'nan'), '0') as float), 1101)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40103', 'CO2', 'uatm', cast(coalesce(nullif('330.0', 'nan'), '0') as float), 1101)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40429', 'CO2', 'uatm', cast(coalesce(nullif('39.0', 'nan'), '0') as float), 1101)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('39734', 'CO2', 'uatm', cast(coalesce(nullif('160.0', 'nan'), '0') as float), 1102)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40103', 'CO2', 'uatm', cast(coalesce(nullif('298.0', 'nan'), '0') as float), 1102)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40429', 'CO2', 'uatm', cast(coalesce(nullif('46.0', 'nan'), '0') as float), 1102)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40091', 'CO2', 'uatm', cast(coalesce(nullif('4830.0', 'nan'), '0') as float), 1103)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40095', 'CO2', 'uatm', cast(coalesce(nullif('4548.0', 'nan'), '0') as float), 1104)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40095', 'CO2', 'uatm', cast(coalesce(nullif('4486.0', 'nan'), '0') as float), 1105)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40096', 'CO2', 'uatm', cast(coalesce(nullif('4127.0', 'nan'), '0') as float), 1106)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40100', 'CO2', 'uatm', cast(coalesce(nullif('3975.0', 'nan'), '0') as float), 1107)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40100', 'CO2', 'uatm', cast(coalesce(nullif('4051.0', 'nan'), '0') as float), 1108)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40102', 'CO2', 'uatm', cast(coalesce(nullif('3620.0', 'nan'), '0') as float), 1109)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40089', 'CO2', 'uatm', cast(coalesce(nullif('3800.0', 'nan'), '0') as float), 1110)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40095', 'CO2', 'uatm', cast(coalesce(nullif('1858.0', 'nan'), '0') as float), 1111)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40098', 'CO2', 'uatm', cast(coalesce(nullif('1950.0', 'nan'), '0') as float), 1112)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40106', 'CO2', 'uatm', cast(coalesce(nullif('750.0', 'nan'), '0') as float), 1113)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40091', 'CO2', 'uatm', cast(coalesce(nullif('11720.0', 'nan'), '0') as float), 1114)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40092', 'CO2', 'uatm', cast(coalesce(nullif('2446.0', 'nan'), '0') as float), 1115)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40094', 'CO2', 'uatm', cast(coalesce(nullif('11355.0', 'nan'), '0') as float), 1116)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40097', 'CO2', 'uatm', cast(coalesce(nullif('3476.0', 'nan'), '0') as float), 1117)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40105', 'CO2', 'uatm', cast(coalesce(nullif('1991.0', 'nan'), '0') as float), 1118)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40090', 'CO2', 'uatm', cast(coalesce(nullif('1010.0', 'nan'), '0') as float), 1119)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40090', 'CO2', 'uatm', cast(coalesce(nullif('7900.0', 'nan'), '0') as float), 1120)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40091', 'CO2', 'uatm', cast(coalesce(nullif('8880.0', 'nan'), '0') as float), 1121)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40091', 'CO2', 'uatm', cast(coalesce(nullif('3000.0', 'nan'), '0') as float), 1122)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40092', 'CO2', 'uatm', cast(coalesce(nullif('3490.0', 'nan'), '0') as float), 1123)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40092', 'CO2', 'uatm', cast(coalesce(nullif('1980.0', 'nan'), '0') as float), 1124)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40093', 'CO2', 'uatm', cast(coalesce(nullif('1490.0', 'nan'), '0') as float), 1125)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40093', 'CO2', 'uatm', cast(coalesce(nullif('480.0', 'nan'), '0') as float), 1125)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40093', 'CO2', 'uatm', cast(coalesce(nullif('325.0', 'nan'), '0') as float), 1125)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40094', 'CO2', 'uatm', cast(coalesce(nullif('1740.0', 'nan'), '0') as float), 1125)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40093', 'CO2', 'uatm', cast(coalesce(nullif('1260.0', 'nan'), '0') as float), 1126)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40093', 'CO2', 'uatm', cast(coalesce(nullif('376.0', 'nan'), '0') as float), 1127)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40096', 'CO2', 'uatm', cast(coalesce(nullif('4660.0', 'nan'), '0') as float), 1128)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40097', 'CO2', 'uatm', cast(coalesce(nullif('820.0', 'nan'), '0') as float), 1129)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40098', 'CO2', 'uatm', cast(coalesce(nullif('655.0', 'nan'), '0') as float), 1130)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40099', 'CO2', 'uatm', cast(coalesce(nullif('330.0', 'nan'), '0') as float), 1131)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40099', 'CO2', 'uatm', cast(coalesce(nullif('102.0', 'nan'), '0') as float), 1132)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40104', 'CO2', 'uatm', cast(coalesce(nullif('245.0', 'nan'), '0') as float), 1133)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40417', 'CO2', 'uatm', cast(coalesce(nullif('4330.0', 'nan'), '0') as float), 1134)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40422', 'CO2', 'uatm', cast(coalesce(nullif('4380.0', 'nan'), '0') as float), 1135)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40422', 'CO2', 'uatm', cast(coalesce(nullif('4580.0', 'nan'), '0') as float), 1136)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40424', 'CO2', 'uatm', cast(coalesce(nullif('4542.0', 'nan'), '0') as float), 1137)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40427', 'CO2', 'uatm', cast(coalesce(nullif('4779.0', 'nan'), '0') as float), 1138)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40428', 'CO2', 'uatm', cast(coalesce(nullif('4557.0', 'nan'), '0') as float), 1139)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40429', 'CO2', 'uatm', cast(coalesce(nullif('4060.0', 'nan'), '0') as float), 1140)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40415', 'CO2', 'uatm', cast(coalesce(nullif('5300.0', 'nan'), '0') as float), 1141)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40425', 'CO2', 'uatm', cast(coalesce(nullif('3276.0', 'nan'), '0') as float), 1142)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40433', 'CO2', 'uatm', cast(coalesce(nullif('733.0', 'nan'), '0') as float), 1143)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40417', 'CO2', 'uatm', cast(coalesce(nullif('7680.0', 'nan'), '0') as float), 1144)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40420', 'CO2', 'uatm', cast(coalesce(nullif('10120.0', 'nan'), '0') as float), 1145)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40423', 'CO2', 'uatm', cast(coalesce(nullif('4269.0', 'nan'), '0') as float), 1146)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40425', 'CO2', 'uatm', cast(coalesce(nullif('5439.0', 'nan'), '0') as float), 1147)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40416', 'CO2', 'uatm', cast(coalesce(nullif('8990.0', 'nan'), '0') as float), 1148)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40419', 'CO2', 'uatm', cast(coalesce(nullif('1659.0', 'nan'), '0') as float), 1149)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40423', 'CO2', 'uatm', cast(coalesce(nullif('253.0', 'nan'), '0') as float), 1150)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40425', 'CO2', 'uatm', cast(coalesce(nullif('107.0', 'nan'), '0') as float), 1151)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40426', 'CO2', 'uatm', cast(coalesce(nullif('131.0', 'nan'), '0') as float), 1152)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('40430', 'CO2', 'uatm', cast(coalesce(nullif('110.0', 'nan'), '0') as float), 1153)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42110', 'CO2', 'uatm', cast(coalesce(nullif('3418.0', 'nan'), '0') as float), 1154)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42110', 'CO2', 'uatm', cast(coalesce(nullif('1896.0', 'nan'), '0') as float), 1155)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42110', 'CO2', 'uatm', cast(coalesce(nullif('2713.0', 'nan'), '0') as float), 1156)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42111', 'CO2', 'uatm', cast(coalesce(nullif('3125.0', 'nan'), '0') as float), 1157)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42111', 'CO2', 'uatm', cast(coalesce(nullif('14089.0', 'nan'), '0') as float), 1158)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42111', 'CO2', 'uatm', cast(coalesce(nullif('21249.0', 'nan'), '0') as float), 1159)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42114', 'CO2', 'uatm', cast(coalesce(nullif('3467.0', 'nan'), '0') as float), 1160)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42114', 'CO2', 'uatm', cast(coalesce(nullif('11508.0', 'nan'), '0') as float), 1161)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42114', 'CO2', 'uatm', cast(coalesce(nullif('8921.0', 'nan'), '0') as float), 1162)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42115', 'CO2', 'uatm', cast(coalesce(nullif('9403.0', 'nan'), '0') as float), 1163)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42115', 'CO2', 'uatm', cast(coalesce(nullif('3262.0', 'nan'), '0') as float), 1164)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42116', 'CO2', 'uatm', cast(coalesce(nullif('12144.0', 'nan'), '0') as float), 1165)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42117', 'CO2', 'uatm', cast(coalesce(nullif('3630.0', 'nan'), '0') as float), 1166)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42117', 'CO2', 'uatm', cast(coalesce(nullif('12511.0', 'nan'), '0') as float), 1167)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42117', 'CO2', 'uatm', cast(coalesce(nullif('3670.0', 'nan'), '0') as float), 1168)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42118', 'CO2', 'uatm', cast(coalesce(nullif('14004.0', 'nan'), '0') as float), 1169)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42118', 'CO2', 'uatm', cast(coalesce(nullif('9544.0', 'nan'), '0') as float), 1170)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42118', 'CO2', 'uatm', cast(coalesce(nullif('9182.0', 'nan'), '0') as float), 1171)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42118', 'CO2', 'uatm', cast(coalesce(nullif('5434.0', 'nan'), '0') as float), 1172)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42119', 'CO2', 'uatm', cast(coalesce(nullif('4058.0', 'nan'), '0') as float), 1173)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42119', 'CO2', 'uatm', cast(coalesce(nullif('9540.0', 'nan'), '0') as float), 1174)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42119', 'CO2', 'uatm', cast(coalesce(nullif('3633.0', 'nan'), '0') as float), 1175)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42120', 'CO2', 'uatm', cast(coalesce(nullif('3010.0', 'nan'), '0') as float), 1176)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42120', 'CO2', 'uatm', cast(coalesce(nullif('3336.0', 'nan'), '0') as float), 1177)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42120', 'CO2', 'uatm', cast(coalesce(nullif('3133.0', 'nan'), '0') as float), 1178)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42120', 'CO2', 'uatm', cast(coalesce(nullif('11609.0', 'nan'), '0') as float), 1179)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42121', 'CO2', 'uatm', cast(coalesce(nullif('10024.0', 'nan'), '0') as float), 1180)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42121', 'CO2', 'uatm', cast(coalesce(nullif('2685.0', 'nan'), '0') as float), 1181)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42121', 'CO2', 'uatm', cast(coalesce(nullif('9608.0', 'nan'), '0') as float), 1182)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42121', 'CO2', 'uatm', cast(coalesce(nullif('1330.0', 'nan'), '0') as float), 1183)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42121', 'CO2', 'uatm', cast(coalesce(nullif('2772.0', 'nan'), '0') as float), 1184)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42121', 'CO2', 'uatm', cast(coalesce(nullif('2549.0', 'nan'), '0') as float), 1185)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42122', 'CO2', 'uatm', cast(coalesce(nullif('1973.0', 'nan'), '0') as float), 1186)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42122', 'CO2', 'uatm', cast(coalesce(nullif('6105.0', 'nan'), '0') as float), 1187)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42122', 'CO2', 'uatm', cast(coalesce(nullif('2371.0', 'nan'), '0') as float), 1188)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42122', 'CO2', 'uatm', cast(coalesce(nullif('3873.0', 'nan'), '0') as float), 1189)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42122', 'CO2', 'uatm', cast(coalesce(nullif('5095.0', 'nan'), '0') as float), 1190)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42124', 'CO2', 'uatm', cast(coalesce(nullif('11317.0', 'nan'), '0') as float), 1191)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42125', 'CO2', 'uatm', cast(coalesce(nullif('7499.0', 'nan'), '0') as float), 1192)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42126', 'CO2', 'uatm', cast(coalesce(nullif('6847.0', 'nan'), '0') as float), 1193)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42126', 'CO2', 'uatm', cast(coalesce(nullif('22899.0', 'nan'), '0') as float), 1194)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42126', 'CO2', 'uatm', cast(coalesce(nullif('7107.0', 'nan'), '0') as float), 1195)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42126', 'CO2', 'uatm', cast(coalesce(nullif('12835.0', 'nan'), '0') as float), 1196)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42127', 'CO2', 'uatm', cast(coalesce(nullif('3143.0', 'nan'), '0') as float), 1197)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42127', 'CO2', 'uatm', cast(coalesce(nullif('6739.0', 'nan'), '0') as float), 1198)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42127', 'CO2', 'uatm', cast(coalesce(nullif('15258.0', 'nan'), '0') as float), 1199)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42127', 'CO2', 'uatm', cast(coalesce(nullif('4618.0', 'nan'), '0') as float), 1200)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42129', 'CO2', 'uatm', cast(coalesce(nullif('5721.0', 'nan'), '0') as float), 1201)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42129', 'CO2', 'uatm', cast(coalesce(nullif('7027.0', 'nan'), '0') as float), 1202)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42129', 'CO2', 'uatm', cast(coalesce(nullif('3465.0', 'nan'), '0') as float), 1203)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42129', 'CO2', 'uatm', cast(coalesce(nullif('4036.0', 'nan'), '0') as float), 1204)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42129', 'CO2', 'uatm', cast(coalesce(nullif('3422.0', 'nan'), '0') as float), 1205)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42130', 'CO2', 'uatm', cast(coalesce(nullif('1554.0', 'nan'), '0') as float), 1206)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42130', 'CO2', 'uatm', cast(coalesce(nullif('3185.0', 'nan'), '0') as float), 1207)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42130', 'CO2', 'uatm', cast(coalesce(nullif('3445.0', 'nan'), '0') as float), 1208)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42130', 'CO2', 'uatm', cast(coalesce(nullif('2138.0', 'nan'), '0') as float), 1209)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42130', 'CO2', 'uatm', cast(coalesce(nullif('3401.0', 'nan'), '0') as float), 1210)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42130', 'CO2', 'uatm', cast(coalesce(nullif('3044.0', 'nan'), '0') as float), 1211)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('29/07/2013 13:45', 'CO2', 'uatm', cast(coalesce(nullif('520.0', 'nan'), '0') as float), 1212)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('19/03/2014 10:30', 'CO2', 'uatm', cast(coalesce(nullif('34.0', 'nan'), '0') as float), 1212)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('13/02/2015 11:20', 'CO2', 'uatm', cast(coalesce(nullif('522.0', 'nan'), '0') as float), 1212)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('18/07/2013 11:30', 'CO2', 'uatm', cast(coalesce(nullif('544.0', 'nan'), '0') as float), 1214)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20/03/2014 11:30', 'CO2', 'uatm', cast(coalesce(nullif('4643.0', 'nan'), '0') as float), 1214)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42340.4826388888', 'CO2', 'uatm', cast(coalesce(nullif('773.0', 'nan'), '0') as float), 1214)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('30/07/2013 13:50', 'CO2', 'uatm', cast(coalesce(nullif('1680.0', 'nan'), '0') as float), 1216)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('24/03/2014 13:15', 'CO2', 'uatm', cast(coalesce(nullif('942.0', 'nan'), '0') as float), 1216)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('26/02/2015 11:00', 'CO2', 'uatm', cast(coalesce(nullif('875.0', 'nan'), '0') as float), 1216)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('24/07/2013 12:05', 'CO2', 'uatm', cast(coalesce(nullif('6513.0', 'nan'), '0') as float), 1217)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41946.5625', 'CO2', 'uatm', cast(coalesce(nullif('2665.0', 'nan'), '0') as float), 1217)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42280.5104166666', 'CO2', 'uatm', cast(coalesce(nullif('2680.0', 'nan'), '0') as float), 1217)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('22/07/2013 12:00', 'CO2', 'uatm', cast(coalesce(nullif('1335.0', 'nan'), '0') as float), 1218)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41762.4895833333', 'CO2', 'uatm', cast(coalesce(nullif('728.0', 'nan'), '0') as float), 1218)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('25/02/2015 10:40', 'CO2', 'uatm', cast(coalesce(nullif('910.0', 'nan'), '0') as float), 1218)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('30/07/2013 11:35', 'CO2', 'uatm', cast(coalesce(nullif('2008.0', 'nan'), '0') as float), 1220)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('24/03/2014 11:10', 'CO2', 'uatm', cast(coalesce(nullif('1049.0', 'nan'), '0') as float), 1220)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42038.5', 'CO2', 'uatm', cast(coalesce(nullif('1182.0', 'nan'), '0') as float), 1220)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('16/07/2013 10:55', 'CO2', 'uatm', cast(coalesce(nullif('3599.0', 'nan'), '0') as float), 1221)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41976.4375', 'CO2', 'uatm', cast(coalesce(nullif('2185.0', 'nan'), '0') as float), 1221)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42341.4305555555', 'CO2', 'uatm', cast(coalesce(nullif('1878.0', 'nan'), '0') as float), 1221)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('16/07/2013 13:50', 'CO2', 'uatm', cast(coalesce(nullif('1608.0', 'nan'), '0') as float), 1222)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41976.5243055555', 'CO2', 'uatm', cast(coalesce(nullif('872.0', 'nan'), '0') as float), 1222)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42311.5173611111', 'CO2', 'uatm', cast(coalesce(nullif('1105.0', 'nan'), '0') as float), 1222)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615.5798611111', 'CO2', 'uatm', cast(coalesce(nullif('10033.0', 'nan'), '0') as float), 1223)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20/02/2014 11:00', 'CO2', 'uatm', cast(coalesce(nullif('8151.0', 'nan'), '0') as float), 1223)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42096.53125', 'CO2', 'uatm', cast(coalesce(nullif('6815.0', 'nan'), '0') as float), 1223)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615.4583333333', 'CO2', 'uatm', cast(coalesce(nullif('2573.0', 'nan'), '0') as float), 1224)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('18/02/2014 14:30', 'CO2', 'uatm', cast(coalesce(nullif('1453.0', 'nan'), '0') as float), 1224)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('19/02/2015 11:00', 'CO2', 'uatm', cast(coalesce(nullif('1759.0', 'nan'), '0') as float), 1224)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('30/07/2013 10:45', 'CO2', 'uatm', cast(coalesce(nullif('3048.0', 'nan'), '0') as float), 1225)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41732.5416666666', 'CO2', 'uatm', cast(coalesce(nullif('1554.0', 'nan'), '0') as float), 1225)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42038.4652777777', 'CO2', 'uatm', cast(coalesce(nullif('1722.0', 'nan'), '0') as float), 1225)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('17/07/2013 09:45', 'CO2', 'uatm', cast(coalesce(nullif('2734.0', 'nan'), '0') as float), 1226)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('18/02/2014 10:15', 'CO2', 'uatm', cast(coalesce(nullif('930.0', 'nan'), '0') as float), 1226)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20/02/2015 09:30', 'CO2', 'uatm', cast(coalesce(nullif('1121.0', 'nan'), '0') as float), 1226)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('19/07/2013 10:30', 'CO2', 'uatm', cast(coalesce(nullif('1465.0', 'nan'), '0') as float), 1228)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('28/02/2014 13:15', 'CO2', 'uatm', cast(coalesce(nullif('683.0', 'nan'), '0') as float), 1228)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('23/02/2015 11:20', 'CO2', 'uatm', cast(coalesce(nullif('734.0', 'nan'), '0') as float), 1228)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('24/07/2013 10:30', 'CO2', 'uatm', cast(coalesce(nullif('1689.0', 'nan'), '0') as float), 1229)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41976.6354166666', 'CO2', 'uatm', cast(coalesce(nullif('113.0', 'nan'), '0') as float), 1229)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42280.4513888888', 'CO2', 'uatm', cast(coalesce(nullif('724.0', 'nan'), '0') as float), 1229)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('23/07/2013 10:00', 'CO2', 'uatm', cast(coalesce(nullif('1946.0', 'nan'), '0') as float), 1231)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41946.53125', 'CO2', 'uatm', cast(coalesce(nullif('728.0', 'nan'), '0') as float), 1231)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42280.5347222222', 'CO2', 'uatm', cast(coalesce(nullif('1143.0', 'nan'), '0') as float), 1231)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('31/07/2013 09:45', 'CO2', 'uatm', cast(coalesce(nullif('2768.0', 'nan'), '0') as float), 1232)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('27/03/2014 13:00', 'CO2', 'uatm', cast(coalesce(nullif('1712.0', 'nan'), '0') as float), 1232)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42127.5208333333', 'CO2', 'uatm', cast(coalesce(nullif('3149.0', 'nan'), '0') as float), 1232)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('18/07/2013 12:30', 'CO2', 'uatm', cast(coalesce(nullif('524.0', 'nan'), '0') as float), 1233)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20/03/2014 12:35', 'CO2', 'uatm', cast(coalesce(nullif('339.0', 'nan'), '0') as float), 1233)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42340.5243055555', 'CO2', 'uatm', cast(coalesce(nullif('526.0', 'nan'), '0') as float), 1233)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('23/07/2013 11:30', 'CO2', 'uatm', cast(coalesce(nullif('1256.0', 'nan'), '0') as float), 1234)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41946.4652777777', 'CO2', 'uatm', cast(coalesce(nullif('563.0', 'nan'), '0') as float), 1234)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42280.5902777777', 'CO2', 'uatm', cast(coalesce(nullif('566.0', 'nan'), '0') as float), 1234)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('19/07/2013 11:20', 'CO2', 'uatm', cast(coalesce(nullif('2806.0', 'nan'), '0') as float), 1236)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20/02/2014 13:00', 'CO2', 'uatm', cast(coalesce(nullif('1581.0', 'nan'), '0') as float), 1236)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('23/02/2015 10:30', 'CO2', 'uatm', cast(coalesce(nullif('1827.0', 'nan'), '0') as float), 1236)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('16/07/2013 16:00', 'CO2', 'uatm', cast(coalesce(nullif('1432.0', 'nan'), '0') as float), 1237)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41976.6041666666', 'CO2', 'uatm', cast(coalesce(nullif('1119.0', 'nan'), '0') as float), 1237)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42280.4097222222', 'CO2', 'uatm', cast(coalesce(nullif('923.0', 'nan'), '0') as float), 1237)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615.3958333333', 'CO2', 'uatm', cast(coalesce(nullif('3230.0', 'nan'), '0') as float), 1239)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('18/02/2014 13:30', 'CO2', 'uatm', cast(coalesce(nullif('1125.0', 'nan'), '0') as float), 1239)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('19/02/2015 12:35', 'CO2', 'uatm', cast(coalesce(nullif('1165.0', 'nan'), '0') as float), 1239)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('19/07/2013 09:30', 'CO2', 'uatm', cast(coalesce(nullif('2010.0', 'nan'), '0') as float), 1240)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('28/02/2014 11:00', 'CO2', 'uatm', cast(coalesce(nullif('799.0', 'nan'), '0') as float), 1240)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42126.5347222222', 'CO2', 'uatm', cast(coalesce(nullif('1066.0', 'nan'), '0') as float), 1240)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615.6458333333', 'CO2', 'uatm', cast(coalesce(nullif('2457.0', 'nan'), '0') as float), 1241)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('18/02/2014 12:15', 'CO2', 'uatm', cast(coalesce(nullif('1095.0', 'nan'), '0') as float), 1241)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42065.5243055555', 'CO2', 'uatm', cast(coalesce(nullif('1165.0', 'nan'), '0') as float), 1241)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('22/07/2013 14:00', 'CO2', 'uatm', cast(coalesce(nullif('1715.0', 'nan'), '0') as float), 1242)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41762.5833333333', 'CO2', 'uatm', cast(coalesce(nullif('887.0', 'nan'), '0') as float), 1242)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('25/02/2015 13:30', 'CO2', 'uatm', cast(coalesce(nullif('858.0', 'nan'), '0') as float), 1242)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('15/07/2013 14:00', 'CO2', 'uatm', cast(coalesce(nullif('1889.0', 'nan'), '0') as float), 1243)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('19/03/2014 12:00', 'CO2', 'uatm', cast(coalesce(nullif('946.0', 'nan'), '0') as float), 1243)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('13/02/2015 10:15', 'CO2', 'uatm', cast(coalesce(nullif('946.0', 'nan'), '0') as float), 1243)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('15/07/2013 14:55', 'CO2', 'uatm', cast(coalesce(nullif('176.0', 'nan'), '0') as float), 1244)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('19/03/2014 11:15', 'CO2', 'uatm', cast(coalesce(nullif('66.0', 'nan'), '0') as float), 1244)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('13/02/2015 10:50', 'CO2', 'uatm', cast(coalesce(nullif('709.0', 'nan'), '0') as float), 1244)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('15/07/2013 10:00', 'CO2', 'uatm', cast(coalesce(nullif('467.0', 'nan'), '0') as float), 1247)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('27/03/2014 13:45', 'CO2', 'uatm', cast(coalesce(nullif('280.0', 'nan'), '0') as float), 1247)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42066.4270833333', 'CO2', 'uatm', cast(coalesce(nullif('561.0', 'nan'), '0') as float), 1247)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('15/07/2013 11:07', 'CO2', 'uatm', cast(coalesce(nullif('448.0', 'nan'), '0') as float), 1248)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('27/03/2014 14:30', 'CO2', 'uatm', cast(coalesce(nullif('590.0', 'nan'), '0') as float), 1248)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42066.5069444444', 'CO2', 'uatm', cast(coalesce(nullif('497.0', 'nan'), '0') as float), 1248)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('31/07/2013 13:15', 'CO2', 'uatm', cast(coalesce(nullif('920.0', 'nan'), '0') as float), 1249)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('21/03/2014 11:20', 'CO2', 'uatm', cast(coalesce(nullif('547.0', 'nan'), '0') as float), 1249)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42127.4479166666', 'CO2', 'uatm', cast(coalesce(nullif('464.0', 'nan'), '0') as float), 1249)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('30/07/2013 09:50', 'CO2', 'uatm', cast(coalesce(nullif('7529.0', 'nan'), '0') as float), 1251)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41732.5', 'CO2', 'uatm', cast(coalesce(nullif('2162.0', 'nan'), '0') as float), 1251)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42038.4375', 'CO2', 'uatm', cast(coalesce(nullif('1814.0', 'nan'), '0') as float), 1251)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('30/07/2013 12:30', 'CO2', 'uatm', cast(coalesce(nullif('4020.0', 'nan'), '0') as float), 1253)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('24/03/2014 12:30', 'CO2', 'uatm', cast(coalesce(nullif('2209.0', 'nan'), '0') as float), 1253)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42038.5416666666', 'CO2', 'uatm', cast(coalesce(nullif('1447.0', 'nan'), '0') as float), 1253)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('30/07/2013 13:10', 'CO2', 'uatm', cast(coalesce(nullif('5924.0', 'nan'), '0') as float), 1254)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('24/03/2014 11:45', 'CO2', 'uatm', cast(coalesce(nullif('1222.0', 'nan'), '0') as float), 1254)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('26/02/2015 10:15', 'CO2', 'uatm', cast(coalesce(nullif('1618.0', 'nan'), '0') as float), 1254)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('30/07/2013 14:40', 'CO2', 'uatm', cast(coalesce(nullif('5867.0', 'nan'), '0') as float), 1255)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('24/03/2014 14:05', 'CO2', 'uatm', cast(coalesce(nullif('2454.0', 'nan'), '0') as float), 1255)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('26/02/2015 12:00', 'CO2', 'uatm', cast(coalesce(nullif('1559.0', 'nan'), '0') as float), 1255)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('30/07/2013 15:30', 'CO2', 'uatm', cast(coalesce(nullif('1622.0', 'nan'), '0') as float), 1256)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('28/02/2014 14:15', 'CO2', 'uatm', cast(coalesce(nullif('1466.0', 'nan'), '0') as float), 1256)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('24/02/2015 11:00', 'CO2', 'uatm', cast(coalesce(nullif('736.0', 'nan'), '0') as float), 1256)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('17/07/2013 10:50', 'CO2', 'uatm', cast(coalesce(nullif('990.0', 'nan'), '0') as float), 1260)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('18/02/2014 11:25', 'CO2', 'uatm', cast(coalesce(nullif('876.0', 'nan'), '0') as float), 1260)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20/02/2015 10:20', 'CO2', 'uatm', cast(coalesce(nullif('903.0', 'nan'), '0') as float), 1260)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('16/07/2013 14:30', 'CO2', 'uatm', cast(coalesce(nullif('546.0', 'nan'), '0') as float), 1261)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41976.5625', 'CO2', 'uatm', cast(coalesce(nullif('670.0', 'nan'), '0') as float), 1261)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42311.5520833333', 'CO2', 'uatm', cast(coalesce(nullif('845.0', 'nan'), '0') as float), 1261)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('22/07/2013 11:15', 'CO2', 'uatm', cast(coalesce(nullif('1721.0', 'nan'), '0') as float), 1262)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41762.4583333333', 'CO2', 'uatm', cast(coalesce(nullif('904.0', 'nan'), '0') as float), 1262)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('25/02/2015 11:40', 'CO2', 'uatm', cast(coalesce(nullif('892.0', 'nan'), '0') as float), 1262)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('22/07/2013 13:10', 'CO2', 'uatm', cast(coalesce(nullif('1651.0', 'nan'), '0') as float), 1265)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41762.5555555555', 'CO2', 'uatm', cast(coalesce(nullif('996.0', 'nan'), '0') as float), 1265)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('25/02/2015 12:40', 'CO2', 'uatm', cast(coalesce(nullif('1051.0', 'nan'), '0') as float), 1265)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('16/07/2013 12:05', 'CO2', 'uatm', cast(coalesce(nullif('650.0', 'nan'), '0') as float), 1266)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41976.46875', 'CO2', 'uatm', cast(coalesce(nullif('462.0', 'nan'), '0') as float), 1266)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42311.4583333333', 'CO2', 'uatm', cast(coalesce(nullif('526.0', 'nan'), '0') as float), 1266)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615.5243055555', 'CO2', 'uatm', cast(coalesce(nullif('6440.0', 'nan'), '0') as float), 1268)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20/02/2014 11:50', 'CO2', 'uatm', cast(coalesce(nullif('5875.0', 'nan'), '0') as float), 1268)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42126.4583333333', 'CO2', 'uatm', cast(coalesce(nullif('5322.0', 'nan'), '0') as float), 1268)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('31/07/2013 10:35', 'CO2', 'uatm', cast(coalesce(nullif('2359.0', 'nan'), '0') as float), 1270)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('27/03/2014 12:15', 'CO2', 'uatm', cast(coalesce(nullif('702.0', 'nan'), '0') as float), 1270)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42127.4895833333', 'CO2', 'uatm', cast(coalesce(nullif('1678.0', 'nan'), '0') as float), 1270)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('23/07/2013 10:45', 'CO2', 'uatm', cast(coalesce(nullif('1390.0', 'nan'), '0') as float), 1271)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41946.4930555555', 'CO2', 'uatm', cast(coalesce(nullif('796.0', 'nan'), '0') as float), 1271)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42280.5625', 'CO2', 'uatm', cast(coalesce(nullif('789.0', 'nan'), '0') as float), 1271)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('24/07/2013 11:20', 'CO2', 'uatm', cast(coalesce(nullif('1666.0', 'nan'), '0') as float), 1272)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41946.5902777777', 'CO2', 'uatm', cast(coalesce(nullif('613.0', 'nan'), '0') as float), 1272)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42280.4861111111', 'CO2', 'uatm', cast(coalesce(nullif('865.0', 'nan'), '0') as float), 1272)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('15/07/2013 12:45', 'CO2', 'uatm', cast(coalesce(nullif('684.0', 'nan'), '0') as float), 1275)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('19/03/2014 13:00', 'CO2', 'uatm', cast(coalesce(nullif('48.0', 'nan'), '0') as float), 1275)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('13/02/2015 09:30', 'CO2', 'uatm', cast(coalesce(nullif('713.0', 'nan'), '0') as float), 1275)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('31/07/2013 11:30', 'CO2', 'uatm', cast(coalesce(nullif('772.0', 'nan'), '0') as float), 1276)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('27/03/2014 11:30', 'CO2', 'uatm', cast(coalesce(nullif('75.0', 'nan'), '0') as float), 1276)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42341.5', 'CO2', 'uatm', cast(coalesce(nullif('444.0', 'nan'), '0') as float), 1276)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('29/07/2013 11:00', 'CO2', 'uatm', cast(coalesce(nullif('2077.0', 'nan'), '0') as float), 1278)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('18/03/2014 11:15', 'CO2', 'uatm', cast(coalesce(nullif('699.0', 'nan'), '0') as float), 1278)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42097.5', 'CO2', 'uatm', cast(coalesce(nullif('771.0', 'nan'), '0') as float), 1278)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('16/07/2013 13:00', 'CO2', 'uatm', cast(coalesce(nullif('929.0', 'nan'), '0') as float), 1279)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41976.5', 'CO2', 'uatm', cast(coalesce(nullif('494.0', 'nan'), '0') as float), 1279)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42311.4895833333', 'CO2', 'uatm', cast(coalesce(nullif('630.0', 'nan'), '0') as float), 1279)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('31/07/2013 12:30', 'CO2', 'uatm', cast(coalesce(nullif('447.0', 'nan'), '0') as float), 1280)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('21/03/2014 12:05', 'CO2', 'uatm', cast(coalesce(nullif('282.0', 'nan'), '0') as float), 1280)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42127.4166666666', 'CO2', 'uatm', cast(coalesce(nullif('613.0', 'nan'), '0') as float), 1280)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('29/07/2013 11:45', 'CO2', 'uatm', cast(coalesce(nullif('2139.0', 'nan'), '0') as float), 1281)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('18/03/2014 12:15', 'CO2', 'uatm', cast(coalesce(nullif('1510.0', 'nan'), '0') as float), 1281)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42097.4513888888', 'CO2', 'uatm', cast(coalesce(nullif('1417.0', 'nan'), '0') as float), 1281)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('18/07/2013 10:15', 'CO2', 'uatm', cast(coalesce(nullif('1802.0', 'nan'), '0') as float), 1282)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20/03/2014 10:40', 'CO2', 'uatm', cast(coalesce(nullif('1175.0', 'nan'), '0') as float), 1282)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42340.4375', 'CO2', 'uatm', cast(coalesce(nullif('1070.0', 'nan'), '0') as float), 1282)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41615.6458333333', 'CO2', 'uatm', cast(coalesce(nullif('2457.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41525.4166666666', 'CO2', 'uatm', cast(coalesce(nullif('3223.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('19/08/2013 10:00', 'CO2', 'uatm', cast(coalesce(nullif('2818.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('26/08/2013 10:00', 'CO2', 'uatm', cast(coalesce(nullif('2663.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41403.5833333333', 'CO2', 'uatm', cast(coalesce(nullif('3607.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41587.5416666666', 'CO2', 'uatm', cast(coalesce(nullif('2854.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('17/09/2013 13:00', 'CO2', 'uatm', cast(coalesce(nullif('2556.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41496.5416666666', 'CO2', 'uatm', cast(coalesce(nullif('2829.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('15/10/2013 13:00', 'CO2', 'uatm', cast(coalesce(nullif('1680.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('22/10/2013 13:00', 'CO2', 'uatm', cast(coalesce(nullif('2065.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('30/10/2013 11:00', 'CO2', 'uatm', cast(coalesce(nullif('1457.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('14/11/2013 11:00', 'CO2', 'uatm', cast(coalesce(nullif('1056.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20/11/2013 11:00', 'CO2', 'uatm', cast(coalesce(nullif('1079.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('27/11/2013 11:00', 'CO2', 'uatm', cast(coalesce(nullif('1058.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41406.4583333333', 'CO2', 'uatm', cast(coalesce(nullif('1162.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20/12/2013 11:00', 'CO2', 'uatm', cast(coalesce(nullif('1148.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41821.4583333333', 'CO2', 'uatm', cast(coalesce(nullif('971.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('15/01/2014 11:00', 'CO2', 'uatm', cast(coalesce(nullif('1100.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('21/01/2014 12:25', 'CO2', 'uatm', cast(coalesce(nullif('1161.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('29/01/2014 12:55', 'CO2', 'uatm', cast(coalesce(nullif('1044.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41731.5451388888', 'CO2', 'uatm', cast(coalesce(nullif('1145.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('18/02/2014 12:15', 'CO2', 'uatm', cast(coalesce(nullif('1095.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('31/03/2014 12:15', 'CO2', 'uatm', cast(coalesce(nullif('1476.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41855.5104166666', 'CO2', 'uatm', cast(coalesce(nullif('1059.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('22/04/2014 14:00', 'CO2', 'uatm', cast(coalesce(nullif('1805.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('29/04/2014 00:00', 'CO2', 'uatm', cast(coalesce(nullif('2421.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('22/05/2014 00:00', 'CO2', 'uatm', cast(coalesce(nullif('2827.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('28/05/2014 00:00', 'CO2', 'uatm', cast(coalesce(nullif('3114.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41796', 'CO2', 'uatm', cast(coalesce(nullif('3921.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20/06/2014 00:00', 'CO2', 'uatm', cast(coalesce(nullif('3146.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41705', 'CO2', 'uatm', cast(coalesce(nullif('2124.0', 'nan'), '0') as float), 1286)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('761.0', 'nan'), '0') as float), 1287)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('642.0', 'nan'), '0') as float), 1288)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('797.0', 'nan'), '0') as float), 1289)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('542.0', 'nan'), '0') as float), 1290)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('467.0', 'nan'), '0') as float), 1291)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('427.0', 'nan'), '0') as float), 1292)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('350.0', 'nan'), '0') as float), 1293)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('372.0', 'nan'), '0') as float), 1294)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('301.0', 'nan'), '0') as float), 1295)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('302.0', 'nan'), '0') as float), 1296)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('323.0', 'nan'), '0') as float), 1297)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('558.0', 'nan'), '0') as float), 1298)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('748.0', 'nan'), '0') as float), 1299)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('371.0', 'nan'), '0') as float), 1300)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('397.0', 'nan'), '0') as float), 1301)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('432.0', 'nan'), '0') as float), 1302)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('282.0', 'nan'), '0') as float), 1303)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('299.0', 'nan'), '0') as float), 1304)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('268.0', 'nan'), '0') as float), 1305)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('302.0', 'nan'), '0') as float), 1306)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('800.0', 'nan'), '0') as float), 1307)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('314.0', 'nan'), '0') as float), 1308)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('754.0', 'nan'), '0') as float), 1309)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('272.0', 'nan'), '0') as float), 1310)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('287.0', 'nan'), '0') as float), 1311)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('274.0', 'nan'), '0') as float), 1312)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('186.0', 'nan'), '0') as float), 1313)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('308.0', 'nan'), '0') as float), 1314)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('462.0', 'nan'), '0') as float), 1315)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2014', 'CO2', 'uatm', cast(coalesce(nullif('471.0', 'nan'), '0') as float), 1316)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41772', 'CO2', 'uatm', cast(coalesce(nullif('528.0', 'nan'), '0') as float), 1317)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41772', 'CO2', 'uatm', cast(coalesce(nullif('464.0', 'nan'), '0') as float), 1318)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41865', 'CO2', 'uatm', cast(coalesce(nullif('760.0', 'nan'), '0') as float), 1319)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42065', 'CO2', 'uatm', cast(coalesce(nullif('761.0', 'nan'), '0') as float), 1320)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41774', 'CO2', 'uatm', cast(coalesce(nullif('635.0', 'nan'), '0') as float), 1320)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41865', 'CO2', 'uatm', cast(coalesce(nullif('726.0', 'nan'), '0') as float), 1320)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41970', 'CO2', 'uatm', cast(coalesce(nullif('722.0', 'nan'), '0') as float), 1320)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42064', 'CO2', 'uatm', cast(coalesce(nullif('466.0', 'nan'), '0') as float), 1321)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41773', 'CO2', 'uatm', cast(coalesce(nullif('815.0', 'nan'), '0') as float), 1321)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41864', 'CO2', 'uatm', cast(coalesce(nullif('615.0', 'nan'), '0') as float), 1321)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41969', 'CO2', 'uatm', cast(coalesce(nullif('1077.0', 'nan'), '0') as float), 1321)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42064', 'CO2', 'uatm', cast(coalesce(nullif('2610.0', 'nan'), '0') as float), 1322)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41773', 'CO2', 'uatm', cast(coalesce(nullif('3244.0', 'nan'), '0') as float), 1322)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41864', 'CO2', 'uatm', cast(coalesce(nullif('2350.0', 'nan'), '0') as float), 1322)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41970', 'CO2', 'uatm', cast(coalesce(nullif('2597.0', 'nan'), '0') as float), 1322)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42065', 'CO2', 'uatm', cast(coalesce(nullif('861.0', 'nan'), '0') as float), 1323)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41776', 'CO2', 'uatm', cast(coalesce(nullif('914.0', 'nan'), '0') as float), 1323)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41867', 'CO2', 'uatm', cast(coalesce(nullif('843.0', 'nan'), '0') as float), 1323)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41971', 'CO2', 'uatm', cast(coalesce(nullif('957.0', 'nan'), '0') as float), 1323)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42066', 'CO2', 'uatm', cast(coalesce(nullif('645.0', 'nan'), '0') as float), 1324)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41778', 'CO2', 'uatm', cast(coalesce(nullif('685.0', 'nan'), '0') as float), 1324)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41869', 'CO2', 'uatm', cast(coalesce(nullif('2751.0', 'nan'), '0') as float), 1324)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41972', 'CO2', 'uatm', cast(coalesce(nullif('1957.0', 'nan'), '0') as float), 1324)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42066', 'CO2', 'uatm', cast(coalesce(nullif('1184.0', 'nan'), '0') as float), 1325)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41777', 'CO2', 'uatm', cast(coalesce(nullif('1057.0', 'nan'), '0') as float), 1325)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41868', 'CO2', 'uatm', cast(coalesce(nullif('960.0', 'nan'), '0') as float), 1325)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41971', 'CO2', 'uatm', cast(coalesce(nullif('1140.0', 'nan'), '0') as float), 1325)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42067', 'CO2', 'uatm', cast(coalesce(nullif('1336.0', 'nan'), '0') as float), 1326)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41779', 'CO2', 'uatm', cast(coalesce(nullif('1270.0', 'nan'), '0') as float), 1326)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41870', 'CO2', 'uatm', cast(coalesce(nullif('1713.0', 'nan'), '0') as float), 1326)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41972', 'CO2', 'uatm', cast(coalesce(nullif('1499.0', 'nan'), '0') as float), 1326)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42068', 'CO2', 'uatm', cast(coalesce(nullif('2413.0', 'nan'), '0') as float), 1327)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41780', 'CO2', 'uatm', cast(coalesce(nullif('1766.0', 'nan'), '0') as float), 1327)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41871', 'CO2', 'uatm', cast(coalesce(nullif('1476.0', 'nan'), '0') as float), 1327)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41973', 'CO2', 'uatm', cast(coalesce(nullif('1975.0', 'nan'), '0') as float), 1327)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42069', 'CO2', 'uatm', cast(coalesce(nullif('1621.0', 'nan'), '0') as float), 1328)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41781', 'CO2', 'uatm', cast(coalesce(nullif('1855.0', 'nan'), '0') as float), 1328)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41872', 'CO2', 'uatm', cast(coalesce(nullif('1633.0', 'nan'), '0') as float), 1328)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41974', 'CO2', 'uatm', cast(coalesce(nullif('1574.0', 'nan'), '0') as float), 1328)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42072', 'CO2', 'uatm', cast(coalesce(nullif('3844.0', 'nan'), '0') as float), 1329)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41785', 'CO2', 'uatm', cast(coalesce(nullif('3337.0', 'nan'), '0') as float), 1329)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41875', 'CO2', 'uatm', cast(coalesce(nullif('4102.0', 'nan'), '0') as float), 1329)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41976', 'CO2', 'uatm', cast(coalesce(nullif('1915.0', 'nan'), '0') as float), 1329)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42070', 'CO2', 'uatm', cast(coalesce(nullif('903.0', 'nan'), '0') as float), 1330)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41782', 'CO2', 'uatm', cast(coalesce(nullif('1072.0', 'nan'), '0') as float), 1330)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41873', 'CO2', 'uatm', cast(coalesce(nullif('919.0', 'nan'), '0') as float), 1330)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41975', 'CO2', 'uatm', cast(coalesce(nullif('1177.0', 'nan'), '0') as float), 1330)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42071', 'CO2', 'uatm', cast(coalesce(nullif('1401.0', 'nan'), '0') as float), 1331)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41784', 'CO2', 'uatm', cast(coalesce(nullif('1952.0', 'nan'), '0') as float), 1331)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41874', 'CO2', 'uatm', cast(coalesce(nullif('1973.0', 'nan'), '0') as float), 1331)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41976', 'CO2', 'uatm', cast(coalesce(nullif('1580.0', 'nan'), '0') as float), 1331)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42074', 'CO2', 'uatm', cast(coalesce(nullif('2553.0', 'nan'), '0') as float), 1332)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41787', 'CO2', 'uatm', cast(coalesce(nullif('2141.0', 'nan'), '0') as float), 1332)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41876', 'CO2', 'uatm', cast(coalesce(nullif('2516.0', 'nan'), '0') as float), 1332)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41977', 'CO2', 'uatm', cast(coalesce(nullif('2907.0', 'nan'), '0') as float), 1332)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42075', 'CO2', 'uatm', cast(coalesce(nullif('1155.0', 'nan'), '0') as float), 1333)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41789', 'CO2', 'uatm', cast(coalesce(nullif('1749.0', 'nan'), '0') as float), 1333)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41878', 'CO2', 'uatm', cast(coalesce(nullif('1779.0', 'nan'), '0') as float), 1333)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41978', 'CO2', 'uatm', cast(coalesce(nullif('2128.0', 'nan'), '0') as float), 1333)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2005-2006', 'CO2', 'uatm', cast(coalesce(nullif('1858.2', 'nan'), '0') as float), 1334)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2005-2006', 'CO2', 'uatm', cast(coalesce(nullif('610.6', 'nan'), '0') as float), 1334)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2005-2006', 'CO2', 'uatm', cast(coalesce(nullif('845.0', 'nan'), '0') as float), 1334)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2005-2006', 'CO2', 'uatm', cast(coalesce(nullif('1858.2', 'nan'), '0') as float), 1335)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2005-2006', 'CO2', 'uatm', cast(coalesce(nullif('610.6', 'nan'), '0') as float), 1335)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2005-2006', 'CO2', 'uatm', cast(coalesce(nullif('845.0', 'nan'), '0') as float), 1335)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1056.0', 'nan'), '0') as float), 1336)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41287', 'CO2', 'uatm', cast(coalesce(nullif('2005.0', 'nan'), '0') as float), 1336)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('2444.0', 'nan'), '0') as float), 1337)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41288', 'CO2', 'uatm', cast(coalesce(nullif('2576.0', 'nan'), '0') as float), 1337)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1968.0', 'nan'), '0') as float), 1338)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41290', 'CO2', 'uatm', cast(coalesce(nullif('2560.0', 'nan'), '0') as float), 1338)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('7650.0', 'nan'), '0') as float), 1339)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41291', 'CO2', 'uatm', cast(coalesce(nullif('10351.0', 'nan'), '0') as float), 1339)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1890.0', 'nan'), '0') as float), 1340)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41292', 'CO2', 'uatm', cast(coalesce(nullif('1555.0', 'nan'), '0') as float), 1340)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('6307.0', 'nan'), '0') as float), 1341)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41293', 'CO2', 'uatm', cast(coalesce(nullif('4979.0', 'nan'), '0') as float), 1341)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('2500.0', 'nan'), '0') as float), 1342)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41295', 'CO2', 'uatm', cast(coalesce(nullif('1718.0', 'nan'), '0') as float), 1342)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41572', 'CO2', 'uatm', cast(coalesce(nullif('707.0', 'nan'), '0') as float), 1342)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('642.0', 'nan'), '0') as float), 1343)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('2008.0', 'nan'), '0') as float), 1344)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41299', 'CO2', 'uatm', cast(coalesce(nullif('2207.0', 'nan'), '0') as float), 1344)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('888.0', 'nan'), '0') as float), 1345)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41303', 'CO2', 'uatm', cast(coalesce(nullif('1447.0', 'nan'), '0') as float), 1345)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('814.0', 'nan'), '0') as float), 1346)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41327', 'CO2', 'uatm', cast(coalesce(nullif('1272.0', 'nan'), '0') as float), 1346)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1204.0', 'nan'), '0') as float), 1347)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41329', 'CO2', 'uatm', cast(coalesce(nullif('3615.0', 'nan'), '0') as float), 1347)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('8181.0', 'nan'), '0') as float), 1348)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41330', 'CO2', 'uatm', cast(coalesce(nullif('12199.0', 'nan'), '0') as float), 1348)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1789.0', 'nan'), '0') as float), 1349)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41335', 'CO2', 'uatm', cast(coalesce(nullif('4291.0', 'nan'), '0') as float), 1349)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1612.0', 'nan'), '0') as float), 1350)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41334', 'CO2', 'uatm', cast(coalesce(nullif('4521.0', 'nan'), '0') as float), 1350)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('3945.0', 'nan'), '0') as float), 1351)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41313', 'CO2', 'uatm', cast(coalesce(nullif('4346.0', 'nan'), '0') as float), 1351)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('2806.0', 'nan'), '0') as float), 1352)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41312', 'CO2', 'uatm', cast(coalesce(nullif('3093.0', 'nan'), '0') as float), 1352)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1830.0', 'nan'), '0') as float), 1353)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41308', 'CO2', 'uatm', cast(coalesce(nullif('3407.0', 'nan'), '0') as float), 1353)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('3972.0', 'nan'), '0') as float), 1354)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41315', 'CO2', 'uatm', cast(coalesce(nullif('4136.0', 'nan'), '0') as float), 1354)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1858.0', 'nan'), '0') as float), 1355)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41316', 'CO2', 'uatm', cast(coalesce(nullif('2300.0', 'nan'), '0') as float), 1355)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('904.0', 'nan'), '0') as float), 1356)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41318', 'CO2', 'uatm', cast(coalesce(nullif('1237.0', 'nan'), '0') as float), 1356)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('9985.0', 'nan'), '0') as float), 1357)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41320', 'CO2', 'uatm', cast(coalesce(nullif('11747.0', 'nan'), '0') as float), 1357)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('9769.0', 'nan'), '0') as float), 1358)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41321', 'CO2', 'uatm', cast(coalesce(nullif('10915.0', 'nan'), '0') as float), 1358)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1357.0', 'nan'), '0') as float), 1359)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41322', 'CO2', 'uatm', cast(coalesce(nullif('1552.0', 'nan'), '0') as float), 1359)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('246.0', 'nan'), '0') as float), 1360)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41286', 'CO2', 'uatm', cast(coalesce(nullif('1234.0', 'nan'), '0') as float), 1360)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1305.0', 'nan'), '0') as float), 1361)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41301', 'CO2', 'uatm', cast(coalesce(nullif('1855.0', 'nan'), '0') as float), 1361)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1469.0', 'nan'), '0') as float), 1362)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41302', 'CO2', 'uatm', cast(coalesce(nullif('1432.0', 'nan'), '0') as float), 1362)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1201.0', 'nan'), '0') as float), 1363)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41303', 'CO2', 'uatm', cast(coalesce(nullif('1317.0', 'nan'), '0') as float), 1363)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('2952.0', 'nan'), '0') as float), 1364)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41307', 'CO2', 'uatm', cast(coalesce(nullif('2493.0', 'nan'), '0') as float), 1364)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1523.0', 'nan'), '0') as float), 1365)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41304', 'CO2', 'uatm', cast(coalesce(nullif('2154.0', 'nan'), '0') as float), 1365)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('2621.0', 'nan'), '0') as float), 1366)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41314', 'CO2', 'uatm', cast(coalesce(nullif('3284.0', 'nan'), '0') as float), 1366)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('2460.0', 'nan'), '0') as float), 1367)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41315', 'CO2', 'uatm', cast(coalesce(nullif('2855.0', 'nan'), '0') as float), 1367)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('12698.0', 'nan'), '0') as float), 1368)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41331', 'CO2', 'uatm', cast(coalesce(nullif('14004.0', 'nan'), '0') as float), 1368)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('356.0', 'nan'), '0') as float), 1369)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41296', 'CO2', 'uatm', cast(coalesce(nullif('275.0', 'nan'), '0') as float), 1369)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('370.0', 'nan'), '0') as float), 1370)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41298', 'CO2', 'uatm', cast(coalesce(nullif('179.0', 'nan'), '0') as float), 1370)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('342.0', 'nan'), '0') as float), 1371)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41326', 'CO2', 'uatm', cast(coalesce(nullif('151.0', 'nan'), '0') as float), 1371)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('1813.0', 'nan'), '0') as float), 1372)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41317', 'CO2', 'uatm', cast(coalesce(nullif('2139.0', 'nan'), '0') as float), 1372)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('842.0', 'nan'), '0') as float), 1373)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41317', 'CO2', 'uatm', cast(coalesce(nullif('1397.0', 'nan'), '0') as float), 1373)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2', 'uatm', cast(coalesce(nullif('735.0', 'nan'), '0') as float), 1374)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41318', 'CO2', 'uatm', cast(coalesce(nullif('1127.0', 'nan'), '0') as float), 1374)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41289', 'CO2', 'uatm', cast(coalesce(nullif('2470.0', 'nan'), '0') as float), 1375)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41344', 'CO2', 'uatm', cast(coalesce(nullif('1410.0', 'nan'), '0') as float), 1376)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41339', 'CO2', 'uatm', cast(coalesce(nullif('955.0', 'nan'), '0') as float), 1377)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41325', 'CO2', 'uatm', cast(coalesce(nullif('215.0', 'nan'), '0') as float), 1378)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41566', 'CO2', 'uatm', cast(coalesce(nullif('2555.0', 'nan'), '0') as float), 1379)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41567', 'CO2', 'uatm', cast(coalesce(nullif('617.0', 'nan'), '0') as float), 1380)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41568', 'CO2', 'uatm', cast(coalesce(nullif('681.0', 'nan'), '0') as float), 1381)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41570', 'CO2', 'uatm', cast(coalesce(nullif('454.0', 'nan'), '0') as float), 1382)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41569', 'CO2', 'uatm', cast(coalesce(nullif('816.0', 'nan'), '0') as float), 1383)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41571', 'CO2', 'uatm', cast(coalesce(nullif('300.0', 'nan'), '0') as float), 1384)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41576', 'CO2', 'uatm', cast(coalesce(nullif('2600.0', 'nan'), '0') as float), 1385)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41574', 'CO2', 'uatm', cast(coalesce(nullif('1602.0', 'nan'), '0') as float), 1386)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41588', 'CO2', 'uatm', cast(coalesce(nullif('462.0', 'nan'), '0') as float), 1387)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41592', 'CO2', 'uatm', cast(coalesce(nullif('2529.0', 'nan'), '0') as float), 1388)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41593', 'CO2', 'uatm', cast(coalesce(nullif('331.0', 'nan'), '0') as float), 1389)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41594', 'CO2', 'uatm', cast(coalesce(nullif('1705.0', 'nan'), '0') as float), 1390)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41595', 'CO2', 'uatm', cast(coalesce(nullif('1022.0', 'nan'), '0') as float), 1391)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41598', 'CO2', 'uatm', cast(coalesce(nullif('6049.0', 'nan'), '0') as float), 1392)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41599', 'CO2', 'uatm', cast(coalesce(nullif('6647.0', 'nan'), '0') as float), 1393)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41602', 'CO2', 'uatm', cast(coalesce(nullif('1099.0', 'nan'), '0') as float), 1394)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41576', 'CO2', 'uatm', cast(coalesce(nullif('156.0', 'nan'), '0') as float), 1395)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41596', 'CO2', 'uatm', cast(coalesce(nullif('165.0', 'nan'), '0') as float), 1396)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('2813.0', 'nan'), '0') as float), 1400)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('3157.0', 'nan'), '0') as float), 1401)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('3087.0', 'nan'), '0') as float), 1402)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('3158.0', 'nan'), '0') as float), 1403)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('4070.0', 'nan'), '0') as float), 1404)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('3660.0', 'nan'), '0') as float), 1405)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('6277.0', 'nan'), '0') as float), 1406)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('703.0', 'nan'), '0') as float), 1407)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('788.0', 'nan'), '0') as float), 1408)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('435.0', 'nan'), '0') as float), 1409)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('1351.0', 'nan'), '0') as float), 1410)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('1561.0', 'nan'), '0') as float), 1411)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('1451.0', 'nan'), '0') as float), 1412)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('nan', 'CO2', 'uatm', cast(coalesce(nullif('1075.0', 'nan'), '0') as float), 1413)
    


And CO2 Flux Samples...


```python
clean_co2_flux_samples.head(1)
print(len(clean_co2_flux_samples))
```

    583



```python
for index, row in clean_co2_flux_samples.iterrows():
        
        print(insert_samples_string.format(str(row["DateTime"]), str(row["SampleType"]), str(row["Unit"]), float(row["CO2 Flux"]), int(row["location_id"])))
        cur.execute(insert_samples_string.format(str(row["DateTime"]), str(row["SampleType"]), str(row["Unit"]), float(row["CO2 Flux"]), int(row["location_id"])))
        conn.commit()
```

    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1381.28', 'nan'), '0') as float), 0)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1267.75', 'nan'), '0') as float), 0)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1449.39', 'nan'), '0') as float), 0)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1025.55', 'nan'), '0') as float), 0)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1411.55', 'nan'), '0') as float), 0)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050830', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1188.28', 'nan'), '0') as float), 0)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050830', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1002.84', 'nan'), '0') as float), 0)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050830', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1059.61', 'nan'), '0') as float), 0)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050830', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1097.45', 'nan'), '0') as float), 0)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1381.28', 'nan'), '0') as float), 63)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1267.75', 'nan'), '0') as float), 63)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1449.39', 'nan'), '0') as float), 63)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1025.55', 'nan'), '0') as float), 63)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040701', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1411.55', 'nan'), '0') as float), 63)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050830', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1188.28', 'nan'), '0') as float), 63)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050830', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1002.84', 'nan'), '0') as float), 63)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050830', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1059.61', 'nan'), '0') as float), 63)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050830', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1097.45', 'nan'), '0') as float), 63)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('306.15', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('270.2', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('370.11', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('368.21', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('779.57', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('787.14', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('375.03', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('526.02', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('389.78', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('423.84', 'nan'), '0') as float), 60)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('306.15', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('270.2', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('370.11', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('368.21', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('779.57', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('787.14', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('375.03', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('526.02', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('389.78', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('423.84', 'nan'), '0') as float), 61)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('306.15', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('270.2', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('370.11', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('368.21', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('779.57', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040702', 'CO2 Flux', 'uatm', cast(coalesce(nullif('787.14', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('375.03', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('526.02', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('389.78', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050826', 'CO2 Flux', 'uatm', cast(coalesce(nullif('423.84', 'nan'), '0') as float), 1)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040705', 'CO2 Flux', 'uatm', cast(coalesce(nullif('219.49', 'nan'), '0') as float), 2)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040705', 'CO2 Flux', 'uatm', cast(coalesce(nullif('579.0', 'nan'), '0') as float), 2)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040705', 'CO2 Flux', 'uatm', cast(coalesce(nullif('345.51', 'nan'), '0') as float), 2)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040705', 'CO2 Flux', 'uatm', cast(coalesce(nullif('522.24', 'nan'), '0') as float), 2)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040705', 'CO2 Flux', 'uatm', cast(coalesce(nullif('361.4', 'nan'), '0') as float), 2)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040705', 'CO2 Flux', 'uatm', cast(coalesce(nullif('983.92', 'nan'), '0') as float), 3)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040705', 'CO2 Flux', 'uatm', cast(coalesce(nullif('431.41', 'nan'), '0') as float), 3)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040714', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2342.49', 'nan'), '0') as float), 4)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040714', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2966.91', 'nan'), '0') as float), 4)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040714', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3708.63', 'nan'), '0') as float), 4)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040714', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2777.69', 'nan'), '0') as float), 4)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040714', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4314.12', 'nan'), '0') as float), 4)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040717', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2406.83', 'nan'), '0') as float), 5)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040718', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2921.5', 'nan'), '0') as float), 14)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040718', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2357.63', 'nan'), '0') as float), 14)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1615.9', 'nan'), '0') as float), 14)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040718', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2921.5', 'nan'), '0') as float), 6)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040718', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2357.63', 'nan'), '0') as float), 6)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1615.9', 'nan'), '0') as float), 6)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040718', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3386.97', 'nan'), '0') as float), 7)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040718', 'CO2 Flux', 'uatm', cast(coalesce(nullif('6017.07', 'nan'), '0') as float), 7)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040718', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2664.16', 'nan'), '0') as float), 7)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040719', 'CO2 Flux', 'uatm', cast(coalesce(nullif('684.96', 'nan'), '0') as float), 8)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040719', 'CO2 Flux', 'uatm', cast(coalesce(nullif('105.58', 'nan'), '0') as float), 8)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040719', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3897.85', 'nan'), '0') as float), 9)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040720', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3617.81', 'nan'), '0') as float), 10)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040720', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3352.91', 'nan'), '0') as float), 10)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050716', 'CO2 Flux', 'uatm', cast(coalesce(nullif('5070.99', 'nan'), '0') as float), 10)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050716', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4541.18', 'nan'), '0') as float), 10)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050716', 'CO2 Flux', 'uatm', cast(coalesce(nullif('5108.83', 'nan'), '0') as float), 10)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050716', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4087.07', 'nan'), '0') as float), 10)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040720', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3617.81', 'nan'), '0') as float), 48)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040720', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3352.91', 'nan'), '0') as float), 48)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050716', 'CO2 Flux', 'uatm', cast(coalesce(nullif('5070.99', 'nan'), '0') as float), 48)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050716', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4541.18', 'nan'), '0') as float), 48)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050716', 'CO2 Flux', 'uatm', cast(coalesce(nullif('5108.83', 'nan'), '0') as float), 48)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050716', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4087.07', 'nan'), '0') as float), 48)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040722', 'CO2 Flux', 'uatm', cast(coalesce(nullif('783.35', 'nan'), '0') as float), 11)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040722', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1298.02', 'nan'), '0') as float), 11)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040722', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1347.22', 'nan'), '0') as float), 11)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040722', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1313.16', 'nan'), '0') as float), 11)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040810', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-326.59', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040810', 'CO2 Flux', 'uatm', cast(coalesce(nullif('124.88', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040810', 'CO2 Flux', 'uatm', cast(coalesce(nullif('465.47', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2 Flux', 'uatm', cast(coalesce(nullif('165.75', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2 Flux', 'uatm', cast(coalesce(nullif('15.14', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2 Flux', 'uatm', cast(coalesce(nullif('15.89', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040816', 'CO2 Flux', 'uatm', cast(coalesce(nullif('65.09', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040816', 'CO2 Flux', 'uatm', cast(coalesce(nullif('132.07', 'nan'), '0') as float), 12)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2 Flux', 'uatm', cast(coalesce(nullif('145.32', 'nan'), '0') as float), 13)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2 Flux', 'uatm', cast(coalesce(nullif('169.16', 'nan'), '0') as float), 13)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040811', 'CO2 Flux', 'uatm', cast(coalesce(nullif('217.22', 'nan'), '0') as float), 13)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('567.65', 'nan'), '0') as float), 13)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('514.67', 'nan'), '0') as float), 13)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('476.82', 'nan'), '0') as float), 13)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040812', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1165.57', 'nan'), '0') as float), 15)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040812', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1180.71', 'nan'), '0') as float), 15)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040812', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1165.57', 'nan'), '0') as float), 16)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040812', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1180.71', 'nan'), '0') as float), 16)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040813', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2543.06', 'nan'), '0') as float), 17)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040813', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2278.16', 'nan'), '0') as float), 17)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040813', 'CO2 Flux', 'uatm', cast(coalesce(nullif('226.3', 'nan'), '0') as float), 18)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040813', 'CO2 Flux', 'uatm', cast(coalesce(nullif('212.68', 'nan'), '0') as float), 18)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040819', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-57.9', 'nan'), '0') as float), 18)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040819', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-106.72', 'nan'), '0') as float), 18)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040814', 'CO2 Flux', 'uatm', cast(coalesce(nullif('225.55', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040814', 'CO2 Flux', 'uatm', cast(coalesce(nullif('247.12', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040814', 'CO2 Flux', 'uatm', cast(coalesce(nullif('211.92', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040814', 'CO2 Flux', 'uatm', cast(coalesce(nullif('313.72', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040815', 'CO2 Flux', 'uatm', cast(coalesce(nullif('289.88', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040815', 'CO2 Flux', 'uatm', cast(coalesce(nullif('245.22', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040815', 'CO2 Flux', 'uatm', cast(coalesce(nullif('480.61', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040815', 'CO2 Flux', 'uatm', cast(coalesce(nullif('397.35', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040815', 'CO2 Flux', 'uatm', cast(coalesce(nullif('359.13', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040815', 'CO2 Flux', 'uatm', cast(coalesce(nullif('353.08', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040815', 'CO2 Flux', 'uatm', cast(coalesce(nullif('367.46', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040819', 'CO2 Flux', 'uatm', cast(coalesce(nullif('457.9', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040819', 'CO2 Flux', 'uatm', cast(coalesce(nullif('469.26', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('541.16', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('201.33', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('320.91', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('162.73', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('378.43', 'nan'), '0') as float), 19)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040817', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1347.22', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040817', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1653.75', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040817', 'CO2 Flux', 'uatm', cast(coalesce(nullif('851.47', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040817', 'CO2 Flux', 'uatm', cast(coalesce(nullif('563.86', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1411.55', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1445.61', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3337.77', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4692.56', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1748.36', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3822.16', 'nan'), '0') as float), 20)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-40.87', 'nan'), '0') as float), 21)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-34.44', 'nan'), '0') as float), 21)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-24.98', 'nan'), '0') as float), 21)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2 Flux', 'uatm', cast(coalesce(nullif('45.79', 'nan'), '0') as float), 21)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040824', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2319.79', 'nan'), '0') as float), 21)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040824', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2732.28', 'nan'), '0') as float), 21)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040824', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2611.18', 'nan'), '0') as float), 21)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2 Flux', 'uatm', cast(coalesce(nullif('329.61', 'nan'), '0') as float), 22)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2 Flux', 'uatm', cast(coalesce(nullif('416.28', 'nan'), '0') as float), 22)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4011.38', 'nan'), '0') as float), 22)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3201.53', 'nan'), '0') as float), 22)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2 Flux', 'uatm', cast(coalesce(nullif('292.53', 'nan'), '0') as float), 23)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040823', 'CO2 Flux', 'uatm', cast(coalesce(nullif('312.21', 'nan'), '0') as float), 23)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040824', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2316.0', 'nan'), '0') as float), 24)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040824', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2690.65', 'nan'), '0') as float), 24)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20040824', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2770.12', 'nan'), '0') as float), 24)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050301', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3776.75', 'nan'), '0') as float), 25)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050301', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4162.75', 'nan'), '0') as float), 25)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050301', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3761.61', 'nan'), '0') as float), 25)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050301', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3519.42', 'nan'), '0') as float), 25)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050302', 'CO2 Flux', 'uatm', cast(coalesce(nullif('563.86', 'nan'), '0') as float), 26)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050302', 'CO2 Flux', 'uatm', cast(coalesce(nullif('620.63', 'nan'), '0') as float), 26)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050302', 'CO2 Flux', 'uatm', cast(coalesce(nullif('552.51', 'nan'), '0') as float), 26)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050302', 'CO2 Flux', 'uatm', cast(coalesce(nullif('726.59', 'nan'), '0') as float), 26)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050303', 'CO2 Flux', 'uatm', cast(coalesce(nullif('6736.09', 'nan'), '0') as float), 27)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050303', 'CO2 Flux', 'uatm', cast(coalesce(nullif('11580.02', 'nan'), '0') as float), 27)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050303', 'CO2 Flux', 'uatm', cast(coalesce(nullif('7757.86', 'nan'), '0') as float), 27)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050303', 'CO2 Flux', 'uatm', cast(coalesce(nullif('10709.63', 'nan'), '0') as float), 27)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4427.65', 'nan'), '0') as float), 28)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4579.03', 'nan'), '0') as float), 28)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4806.09', 'nan'), '0') as float), 28)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('772.0', 'nan'), '0') as float), 29)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('983.92', 'nan'), '0') as float), 29)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('866.61', 'nan'), '0') as float), 29)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1074.75', 'nan'), '0') as float), 30)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1192.06', 'nan'), '0') as float), 30)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1184.49', 'nan'), '0') as float), 30)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1044.47', 'nan'), '0') as float), 30)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1381.28', 'nan'), '0') as float), 31)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2569.55', 'nan'), '0') as float), 31)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1839.18', 'nan'), '0') as float), 31)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('741.73', 'nan'), '0') as float), 32)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('794.71', 'nan'), '0') as float), 32)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('847.69', 'nan'), '0') as float), 32)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('972.57', 'nan'), '0') as float), 32)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1392.63', 'nan'), '0') as float), 33)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1377.49', 'nan'), '0') as float), 33)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2115.43', 'nan'), '0') as float), 33)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2123.0', 'nan'), '0') as float), 33)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1702.94', 'nan'), '0') as float), 34)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1631.04', 'nan'), '0') as float), 34)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1612.12', 'nan'), '0') as float), 34)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050305', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1396.41', 'nan'), '0') as float), 34)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1733.22', 'nan'), '0') as float), 35)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1774.85', 'nan'), '0') as float), 35)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2819.32', 'nan'), '0') as float), 35)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2331.14', 'nan'), '0') as float), 35)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('703.88', 'nan'), '0') as float), 36)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('260.74', 'nan'), '0') as float), 36)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('248.63', 'nan'), '0') as float), 36)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('961.22', 'nan'), '0') as float), 36)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('719.02', 'nan'), '0') as float), 37)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('677.39', 'nan'), '0') as float), 37)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1052.04', 'nan'), '0') as float), 37)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1369.92', 'nan'), '0') as float), 37)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1672.67', 'nan'), '0') as float), 38)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1665.1', 'nan'), '0') as float), 38)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1661.32', 'nan'), '0') as float), 38)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1854.32', 'nan'), '0') as float), 38)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050308', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1525.08', 'nan'), '0') as float), 39)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050308', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1926.22', 'nan'), '0') as float), 39)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050308', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1161.79', 'nan'), '0') as float), 39)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1097.45', 'nan'), '0') as float), 40)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1241.26', 'nan'), '0') as float), 40)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1581.85', 'nan'), '0') as float), 40)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1029.34', 'nan'), '0') as float), 40)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2 Flux', 'uatm', cast(coalesce(nullif('840.12', 'nan'), '0') as float), 40)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2 Flux', 'uatm', cast(coalesce(nullif('889.32', 'nan'), '0') as float), 40)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2 Flux', 'uatm', cast(coalesce(nullif('741.73', 'nan'), '0') as float), 40)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3296.14', 'nan'), '0') as float), 41)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3190.18', 'nan'), '0') as float), 41)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3228.02', 'nan'), '0') as float), 41)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050309', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3197.75', 'nan'), '0') as float), 41)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050312', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4995.3', 'nan'), '0') as float), 42)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050312', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4541.18', 'nan'), '0') as float), 42)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050312', 'CO2 Flux', 'uatm', cast(coalesce(nullif('5335.89', 'nan'), '0') as float), 42)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050312', 'CO2 Flux', 'uatm', cast(coalesce(nullif('5108.83', 'nan'), '0') as float), 42)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050312', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4276.28', 'nan'), '0') as float), 43)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050312', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3262.08', 'nan'), '0') as float), 43)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050312', 'CO2 Flux', 'uatm', cast(coalesce(nullif('17672.77', 'nan'), '0') as float), 43)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050312', 'CO2 Flux', 'uatm', cast(coalesce(nullif('15326.5', 'nan'), '0') as float), 43)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050313', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2263.02', 'nan'), '0') as float), 44)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050313', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2308.44', 'nan'), '0') as float), 44)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050313', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2970.69', 'nan'), '0') as float), 44)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050313', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2811.75', 'nan'), '0') as float), 44)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050713', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3757.83', 'nan'), '0') as float), 45)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050713', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4162.75', 'nan'), '0') as float), 45)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050713', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4124.91', 'nan'), '0') as float), 45)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050713', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2626.32', 'nan'), '0') as float), 45)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050713', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2334.93', 'nan'), '0') as float), 45)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050713', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3281.01', 'nan'), '0') as float), 45)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050713', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2482.51', 'nan'), '0') as float), 45)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050715', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1782.41', 'nan'), '0') as float), 46)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050715', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2550.63', 'nan'), '0') as float), 46)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050715', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1865.67', 'nan'), '0') as float), 46)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050715', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2259.24', 'nan'), '0') as float), 46)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050715', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4957.46', 'nan'), '0') as float), 47)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050715', 'CO2 Flux', 'uatm', cast(coalesce(nullif('7871.39', 'nan'), '0') as float), 47)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050715', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4276.28', 'nan'), '0') as float), 47)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050715', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4389.81', 'nan'), '0') as float), 47)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050719', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2906.36', 'nan'), '0') as float), 49)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050719', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2512.79', 'nan'), '0') as float), 49)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050719', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2361.42', 'nan'), '0') as float), 49)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050719', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3035.02', 'nan'), '0') as float), 49)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050719', 'CO2 Flux', 'uatm', cast(coalesce(nullif('745.51', 'nan'), '0') as float), 50)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050719', 'CO2 Flux', 'uatm', cast(coalesce(nullif('601.71', 'nan'), '0') as float), 50)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050719', 'CO2 Flux', 'uatm', cast(coalesce(nullif('995.28', 'nan'), '0') as float), 50)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050719', 'CO2 Flux', 'uatm', cast(coalesce(nullif('817.41', 'nan'), '0') as float), 50)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050721', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2058.67', 'nan'), '0') as float), 51)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050721', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2607.4', 'nan'), '0') as float), 51)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050721', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2145.71', 'nan'), '0') as float), 51)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050721', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2618.75', 'nan'), '0') as float), 51)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050725', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1634.83', 'nan'), '0') as float), 52)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050725', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1449.39', 'nan'), '0') as float), 52)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050725', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1544.0', 'nan'), '0') as float), 52)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050725', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1392.63', 'nan'), '0') as float), 52)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1286.67', 'nan'), '0') as float), 52)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1332.08', 'nan'), '0') as float), 52)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1006.63', 'nan'), '0') as float), 52)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('0.0', 'nan'), '0') as float), 52)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050725', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1634.83', 'nan'), '0') as float), 53)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050725', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1449.39', 'nan'), '0') as float), 53)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050725', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1544.0', 'nan'), '0') as float), 53)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050725', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1392.63', 'nan'), '0') as float), 53)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1286.67', 'nan'), '0') as float), 53)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1332.08', 'nan'), '0') as float), 53)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1006.63', 'nan'), '0') as float), 53)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('0.0', 'nan'), '0') as float), 53)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1895.94', 'nan'), '0') as float), 54)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2255.45', 'nan'), '0') as float), 54)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1112.59', 'nan'), '0') as float), 54)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050726', 'CO2 Flux', 'uatm', cast(coalesce(nullif('654.69', 'nan'), '0') as float), 54)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050727', 'CO2 Flux', 'uatm', cast(coalesce(nullif('571.43', 'nan'), '0') as float), 55)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050727', 'CO2 Flux', 'uatm', cast(coalesce(nullif('692.53', 'nan'), '0') as float), 55)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050727', 'CO2 Flux', 'uatm', cast(coalesce(nullif('745.51', 'nan'), '0') as float), 55)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050727', 'CO2 Flux', 'uatm', cast(coalesce(nullif('457.9', 'nan'), '0') as float), 55)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4162.75', 'nan'), '0') as float), 56)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2251.67', 'nan'), '0') as float), 56)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2603.61', 'nan'), '0') as float), 56)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4768.24', 'nan'), '0') as float), 56)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2459.81', 'nan'), '0') as float), 57)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2414.4', 'nan'), '0') as float), 57)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2403.04', 'nan'), '0') as float), 57)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050818', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2433.32', 'nan'), '0') as float), 57)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2501.44', 'nan'), '0') as float), 58)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2512.79', 'nan'), '0') as float), 58)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2478.73', 'nan'), '0') as float), 58)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2728.49', 'nan'), '0') as float), 58)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('0.0', 'nan'), '0') as float), 59)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2630.1', 'nan'), '0') as float), 59)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2486.3', 'nan'), '0') as float), 59)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050820', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2599.83', 'nan'), '0') as float), 59)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050829', 'CO2 Flux', 'uatm', cast(coalesce(nullif('356.1', 'nan'), '0') as float), 62)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050829', 'CO2 Flux', 'uatm', cast(coalesce(nullif('378.43', 'nan'), '0') as float), 62)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050829', 'CO2 Flux', 'uatm', cast(coalesce(nullif('267.55', 'nan'), '0') as float), 62)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050829', 'CO2 Flux', 'uatm', cast(coalesce(nullif('503.31', 'nan'), '0') as float), 62)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050831', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1498.59', 'nan'), '0') as float), 64)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050831', 'CO2 Flux', 'uatm', cast(coalesce(nullif('0.0', 'nan'), '0') as float), 64)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050831', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1665.1', 'nan'), '0') as float), 64)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050831', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1460.75', 'nan'), '0') as float), 64)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050904', 'CO2 Flux', 'uatm', cast(coalesce(nullif('356.1', 'nan'), '0') as float), 65)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050904', 'CO2 Flux', 'uatm', cast(coalesce(nullif('255.06', 'nan'), '0') as float), 65)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050904', 'CO2 Flux', 'uatm', cast(coalesce(nullif('267.55', 'nan'), '0') as float), 65)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20050904', 'CO2 Flux', 'uatm', cast(coalesce(nullif('700.1', 'nan'), '0') as float), 65)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061125', 'CO2 Flux', 'uatm', cast(coalesce(nullif('692.53', 'nan'), '0') as float), 66)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061125', 'CO2 Flux', 'uatm', cast(coalesce(nullif('647.12', 'nan'), '0') as float), 66)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061125', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1165.57', 'nan'), '0') as float), 66)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061125', 'CO2 Flux', 'uatm', cast(coalesce(nullif('896.88', 'nan'), '0') as float), 66)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061125', 'CO2 Flux', 'uatm', cast(coalesce(nullif('183.16', 'nan'), '0') as float), 67)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061125', 'CO2 Flux', 'uatm', cast(coalesce(nullif('337.56', 'nan'), '0') as float), 67)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061125', 'CO2 Flux', 'uatm', cast(coalesce(nullif('238.41', 'nan'), '0') as float), 67)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061127', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2959.34', 'nan'), '0') as float), 68)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061127', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2493.87', 'nan'), '0') as float), 68)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061127', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2842.02', 'nan'), '0') as float), 68)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061127', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2421.96', 'nan'), '0') as float), 69)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061127', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2437.1', 'nan'), '0') as float), 69)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061127', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2414.4', 'nan'), '0') as float), 69)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061130', 'CO2 Flux', 'uatm', cast(coalesce(nullif('923.37', 'nan'), '0') as float), 70)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061130', 'CO2 Flux', 'uatm', cast(coalesce(nullif('756.86', 'nan'), '0') as float), 70)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061130', 'CO2 Flux', 'uatm', cast(coalesce(nullif('772.0', 'nan'), '0') as float), 70)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061130', 'CO2 Flux', 'uatm', cast(coalesce(nullif('885.53', 'nan'), '0') as float), 70)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061130', 'CO2 Flux', 'uatm', cast(coalesce(nullif('230.47', 'nan'), '0') as float), 71)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061130', 'CO2 Flux', 'uatm', cast(coalesce(nullif('239.17', 'nan'), '0') as float), 71)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061130', 'CO2 Flux', 'uatm', cast(coalesce(nullif('299.34', 'nan'), '0') as float), 71)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061130', 'CO2 Flux', 'uatm', cast(coalesce(nullif('250.9', 'nan'), '0') as float), 71)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061130', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1188.28', 'nan'), '0') as float), 72)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061130', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1025.55', 'nan'), '0') as float), 72)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061130', 'CO2 Flux', 'uatm', cast(coalesce(nullif('476.82', 'nan'), '0') as float), 72)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('5676.48', 'nan'), '0') as float), 73)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('6660.4', 'nan'), '0') as float), 73)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4200.6', 'nan'), '0') as float), 73)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4806.09', 'nan'), '0') as float), 73)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('5335.89', 'nan'), '0') as float), 73)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1328.3', 'nan'), '0') as float), 74)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1116.37', 'nan'), '0') as float), 74)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1127.73', 'nan'), '0') as float), 74)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1089.88', 'nan'), '0') as float), 74)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1048.26', 'nan'), '0') as float), 74)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1971.63', 'nan'), '0') as float), 75)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2331.14', 'nan'), '0') as float), 75)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1914.87', 'nan'), '0') as float), 75)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2043.53', 'nan'), '0') as float), 75)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2887.44', 'nan'), '0') as float), 76)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2580.91', 'nan'), '0') as float), 76)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4087.07', 'nan'), '0') as float), 77)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4200.6', 'nan'), '0') as float), 77)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061211', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4238.44', 'nan'), '0') as float), 77)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2565.77', 'nan'), '0') as float), 78)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2849.59', 'nan'), '0') as float), 78)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2728.49', 'nan'), '0') as float), 78)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3860.01', 'nan'), '0') as float), 79)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3780.54', 'nan'), '0') as float), 79)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4049.22', 'nan'), '0') as float), 80)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3231.81', 'nan'), '0') as float), 80)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3587.54', 'nan'), '0') as float), 80)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1059.61', 'nan'), '0') as float), 81)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1286.67', 'nan'), '0') as float), 81)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1661.32', 'nan'), '0') as float), 81)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1101.24', 'nan'), '0') as float), 81)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1014.2', 'nan'), '0') as float), 82)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('730.37', 'nan'), '0') as float), 82)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('885.53', 'nan'), '0') as float), 82)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1438.04', 'nan'), '0') as float), 82)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1933.79', 'nan'), '0') as float), 83)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2001.91', 'nan'), '0') as float), 83)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061213', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1842.96', 'nan'), '0') as float), 83)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061215', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1933.79', 'nan'), '0') as float), 84)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061215', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1589.41', 'nan'), '0') as float), 84)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061215', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1786.2', 'nan'), '0') as float), 84)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061215', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1354.79', 'nan'), '0') as float), 85)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061215', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1407.77', 'nan'), '0') as float), 85)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061215', 'CO2 Flux', 'uatm', cast(coalesce(nullif('968.79', 'nan'), '0') as float), 85)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20061215', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1358.57', 'nan'), '0') as float), 85)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3341.55', 'nan'), '0') as float), 86)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1930.0', 'nan'), '0') as float), 86)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2505.22', 'nan'), '0') as float), 86)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1695.38', 'nan'), '0') as float), 87)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1154.22', 'nan'), '0') as float), 87)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1854.32', 'nan'), '0') as float), 87)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1180.71', 'nan'), '0') as float), 88)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1294.24', 'nan'), '0') as float), 88)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1861.89', 'nan'), '0') as float), 88)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2043.53', 'nan'), '0') as float), 89)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2300.87', 'nan'), '0') as float), 89)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2244.1', 'nan'), '0') as float), 89)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070111', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2418.18', 'nan'), '0') as float), 89)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070123', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2940.42', 'nan'), '0') as float), 90)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070123', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1884.59', 'nan'), '0') as float), 90)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070123', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2145.71', 'nan'), '0') as float), 90)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070123', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2660.38', 'nan'), '0') as float), 91)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070123', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2565.77', 'nan'), '0') as float), 91)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070123', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2804.18', 'nan'), '0') as float), 91)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('20070123', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2440.89', 'nan'), '0') as float), 91)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41772', 'CO2 Flux', 'uatm', cast(coalesce(nullif('425.0', 'nan'), '0') as float), 1317)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41772', 'CO2 Flux', 'uatm', cast(coalesce(nullif('225.0', 'nan'), '0') as float), 1318)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41865', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-308.0', 'nan'), '0') as float), 1319)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42065', 'CO2 Flux', 'uatm', cast(coalesce(nullif('325.0', 'nan'), '0') as float), 1320)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41774', 'CO2 Flux', 'uatm', cast(coalesce(nullif('396.0', 'nan'), '0') as float), 1320)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41865', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4959.0', 'nan'), '0') as float), 1320)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41970', 'CO2 Flux', 'uatm', cast(coalesce(nullif('466.0', 'nan'), '0') as float), 1320)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42064', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-87.0', 'nan'), '0') as float), 1321)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41773', 'CO2 Flux', 'uatm', cast(coalesce(nullif('875.0', 'nan'), '0') as float), 1321)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41864', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2450.0', 'nan'), '0') as float), 1321)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41969', 'CO2 Flux', 'uatm', cast(coalesce(nullif('95.0', 'nan'), '0') as float), 1321)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42064', 'CO2 Flux', 'uatm', cast(coalesce(nullif('785.0', 'nan'), '0') as float), 1322)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41773', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4198.0', 'nan'), '0') as float), 1322)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41864', 'CO2 Flux', 'uatm', cast(coalesce(nullif('5116.0', 'nan'), '0') as float), 1322)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41970', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4154.0', 'nan'), '0') as float), 1322)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42065', 'CO2 Flux', 'uatm', cast(coalesce(nullif('152.0', 'nan'), '0') as float), 1323)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41776', 'CO2 Flux', 'uatm', cast(coalesce(nullif('233.0', 'nan'), '0') as float), 1323)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41867', 'CO2 Flux', 'uatm', cast(coalesce(nullif('209.0', 'nan'), '0') as float), 1323)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41971', 'CO2 Flux', 'uatm', cast(coalesce(nullif('644.0', 'nan'), '0') as float), 1323)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42066', 'CO2 Flux', 'uatm', cast(coalesce(nullif('25.0', 'nan'), '0') as float), 1324)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41778', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-4.0', 'nan'), '0') as float), 1324)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41869', 'CO2 Flux', 'uatm', cast(coalesce(nullif('456.0', 'nan'), '0') as float), 1324)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41972', 'CO2 Flux', 'uatm', cast(coalesce(nullif('166.0', 'nan'), '0') as float), 1324)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42066', 'CO2 Flux', 'uatm', cast(coalesce(nullif('274.0', 'nan'), '0') as float), 1325)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41777', 'CO2 Flux', 'uatm', cast(coalesce(nullif('392.0', 'nan'), '0') as float), 1325)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41868', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1194.0', 'nan'), '0') as float), 1325)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41971', 'CO2 Flux', 'uatm', cast(coalesce(nullif('80.0', 'nan'), '0') as float), 1325)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42067', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1838.0', 'nan'), '0') as float), 1326)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41779', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2266.0', 'nan'), '0') as float), 1326)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41870', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4959.0', 'nan'), '0') as float), 1326)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41972', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1384.0', 'nan'), '0') as float), 1326)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42068', 'CO2 Flux', 'uatm', cast(coalesce(nullif('90.0', 'nan'), '0') as float), 1327)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41780', 'CO2 Flux', 'uatm', cast(coalesce(nullif('335.0', 'nan'), '0') as float), 1327)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41871', 'CO2 Flux', 'uatm', cast(coalesce(nullif('132.0', 'nan'), '0') as float), 1327)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41973', 'CO2 Flux', 'uatm', cast(coalesce(nullif('54.0', 'nan'), '0') as float), 1327)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42069', 'CO2 Flux', 'uatm', cast(coalesce(nullif('773.0', 'nan'), '0') as float), 1328)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41781', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1796.0', 'nan'), '0') as float), 1328)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41872', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2445.0', 'nan'), '0') as float), 1328)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41974', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1155.0', 'nan'), '0') as float), 1328)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42072', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1284.0', 'nan'), '0') as float), 1329)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41785', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1717.0', 'nan'), '0') as float), 1329)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41875', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2320.0', 'nan'), '0') as float), 1329)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41976', 'CO2 Flux', 'uatm', cast(coalesce(nullif('473.0', 'nan'), '0') as float), 1329)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42070', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2027.0', 'nan'), '0') as float), 1330)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41782', 'CO2 Flux', 'uatm', cast(coalesce(nullif('659.0', 'nan'), '0') as float), 1330)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41873', 'CO2 Flux', 'uatm', cast(coalesce(nullif('279.0', 'nan'), '0') as float), 1330)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41975', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3996.0', 'nan'), '0') as float), 1330)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42071', 'CO2 Flux', 'uatm', cast(coalesce(nullif('738.0', 'nan'), '0') as float), 1331)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41784', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1214.0', 'nan'), '0') as float), 1331)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41874', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1338.0', 'nan'), '0') as float), 1331)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41976', 'CO2 Flux', 'uatm', cast(coalesce(nullif('384.0', 'nan'), '0') as float), 1331)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42074', 'CO2 Flux', 'uatm', cast(coalesce(nullif('894.0', 'nan'), '0') as float), 1332)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41787', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3803.0', 'nan'), '0') as float), 1332)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41876', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1465.0', 'nan'), '0') as float), 1332)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41977', 'CO2 Flux', 'uatm', cast(coalesce(nullif('851.0', 'nan'), '0') as float), 1332)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('42075', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3497.0', 'nan'), '0') as float), 1333)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41789', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3647.0', 'nan'), '0') as float), 1333)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41878', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3154.0', 'nan'), '0') as float), 1333)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41978', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2229.0', 'nan'), '0') as float), 1333)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('559.91', 'nan'), '0') as float), 1336)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41287', 'CO2 Flux', 'uatm', cast(coalesce(nullif('235.425', 'nan'), '0') as float), 1336)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('581.08', 'nan'), '0') as float), 1337)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41288', 'CO2 Flux', 'uatm', cast(coalesce(nullif('438.73', 'nan'), '0') as float), 1337)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1199.39', 'nan'), '0') as float), 1338)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41290', 'CO2 Flux', 'uatm', cast(coalesce(nullif('831.47', 'nan'), '0') as float), 1338)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4566.515', 'nan'), '0') as float), 1339)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('201.845', 'nan'), '0') as float), 1340)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41292', 'CO2 Flux', 'uatm', cast(coalesce(nullif('101.47', 'nan'), '0') as float), 1340)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1129.31', 'nan'), '0') as float), 1341)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41293', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1705.28', 'nan'), '0') as float), 1341)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('523.41', 'nan'), '0') as float), 1342)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41295', 'CO2 Flux', 'uatm', cast(coalesce(nullif('143.08', 'nan'), '0') as float), 1342)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41572', 'CO2 Flux', 'uatm', cast(coalesce(nullif('61.32', 'nan'), '0') as float), 1342)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('102.565', 'nan'), '0') as float), 1343)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1030.395', 'nan'), '0') as float), 1344)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41299', 'CO2 Flux', 'uatm', cast(coalesce(nullif('514.285', 'nan'), '0') as float), 1344)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('93.44', 'nan'), '0') as float), 1345)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41303', 'CO2 Flux', 'uatm', cast(coalesce(nullif('422.67', 'nan'), '0') as float), 1345)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('72.27', 'nan'), '0') as float), 1346)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41327', 'CO2 Flux', 'uatm', cast(coalesce(nullif('560.64', 'nan'), '0') as float), 1346)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('197.1', 'nan'), '0') as float), 1347)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41329', 'CO2 Flux', 'uatm', cast(coalesce(nullif('2047.65', 'nan'), '0') as float), 1347)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4885.16', 'nan'), '0') as float), 1348)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41330', 'CO2 Flux', 'uatm', cast(coalesce(nullif('12151.58', 'nan'), '0') as float), 1348)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4069.75', 'nan'), '0') as float), 1349)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41335', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3350.335', 'nan'), '0') as float), 1349)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1220.195', 'nan'), '0') as float), 1350)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3171.12', 'nan'), '0') as float), 1352)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41312', 'CO2 Flux', 'uatm', cast(coalesce(nullif('708.1', 'nan'), '0') as float), 1352)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('809.57', 'nan'), '0') as float), 1353)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41308', 'CO2 Flux', 'uatm', cast(coalesce(nullif('711.75', 'nan'), '0') as float), 1353)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1117.63', 'nan'), '0') as float), 1354)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41315', 'CO2 Flux', 'uatm', cast(coalesce(nullif('611.74', 'nan'), '0') as float), 1354)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('160.6', 'nan'), '0') as float), 1355)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41316', 'CO2 Flux', 'uatm', cast(coalesce(nullif('165.71', 'nan'), '0') as float), 1355)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('279.955', 'nan'), '0') as float), 1356)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41318', 'CO2 Flux', 'uatm', cast(coalesce(nullif('156.585', 'nan'), '0') as float), 1356)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1049.74', 'nan'), '0') as float), 1357)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41320', 'CO2 Flux', 'uatm', cast(coalesce(nullif('8321.635', 'nan'), '0') as float), 1357)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1038.425', 'nan'), '0') as float), 1358)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41321', 'CO2 Flux', 'uatm', cast(coalesce(nullif('4530.38', 'nan'), '0') as float), 1358)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('322.66', 'nan'), '0') as float), 1359)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41322', 'CO2 Flux', 'uatm', cast(coalesce(nullif('429.97', 'nan'), '0') as float), 1359)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41301', 'CO2 Flux', 'uatm', cast(coalesce(nullif('963.965', 'nan'), '0') as float), 1361)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('316.455', 'nan'), '0') as float), 1362)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41302', 'CO2 Flux', 'uatm', cast(coalesce(nullif('584.365', 'nan'), '0') as float), 1362)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41303', 'CO2 Flux', 'uatm', cast(coalesce(nullif('547.865', 'nan'), '0') as float), 1363)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1165.445', 'nan'), '0') as float), 1364)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41307', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1789.23', 'nan'), '0') as float), 1364)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1146.1', 'nan'), '0') as float), 1365)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41304', 'CO2 Flux', 'uatm', cast(coalesce(nullif('401.5', 'nan'), '0') as float), 1365)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1860.77', 'nan'), '0') as float), 1366)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41314', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1035.505', 'nan'), '0') as float), 1366)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1271.295', 'nan'), '0') as float), 1367)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41315', 'CO2 Flux', 'uatm', cast(coalesce(nullif('617.215', 'nan'), '0') as float), 1367)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('7495.64', 'nan'), '0') as float), 1368)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41331', 'CO2 Flux', 'uatm', cast(coalesce(nullif('9408.24', 'nan'), '0') as float), 1368)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-24.82', 'nan'), '0') as float), 1369)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41296', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-36.5', 'nan'), '0') as float), 1369)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-25.55', 'nan'), '0') as float), 1370)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41298', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-30.66', 'nan'), '0') as float), 1370)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41326', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-166.44', 'nan'), '0') as float), 1371)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('235.06', 'nan'), '0') as float), 1372)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41317', 'CO2 Flux', 'uatm', cast(coalesce(nullif('288.715', 'nan'), '0') as float), 1372)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('153.3', 'nan'), '0') as float), 1373)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41317', 'CO2 Flux', 'uatm', cast(coalesce(nullif('532.535', 'nan'), '0') as float), 1373)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('2012', 'CO2 Flux', 'uatm', cast(coalesce(nullif('97.09', 'nan'), '0') as float), 1374)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41318', 'CO2 Flux', 'uatm', cast(coalesce(nullif('728.175', 'nan'), '0') as float), 1374)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41339', 'CO2 Flux', 'uatm', cast(coalesce(nullif('57.305', 'nan'), '0') as float), 1377)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41325', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-85.775', 'nan'), '0') as float), 1378)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41566', 'CO2 Flux', 'uatm', cast(coalesce(nullif('81.03', 'nan'), '0') as float), 1379)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41568', 'CO2 Flux', 'uatm', cast(coalesce(nullif('98.185', 'nan'), '0') as float), 1381)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41569', 'CO2 Flux', 'uatm', cast(coalesce(nullif('129.575', 'nan'), '0') as float), 1383)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41571', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-8.395', 'nan'), '0') as float), 1384)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41574', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1241.73', 'nan'), '0') as float), 1386)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41588', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-12.045', 'nan'), '0') as float), 1387)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41594', 'CO2 Flux', 'uatm', cast(coalesce(nullif('91.615', 'nan'), '0') as float), 1390)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41595', 'CO2 Flux', 'uatm', cast(coalesce(nullif('206.59', 'nan'), '0') as float), 1391)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41598', 'CO2 Flux', 'uatm', cast(coalesce(nullif('3967.55', 'nan'), '0') as float), 1392)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41599', 'CO2 Flux', 'uatm', cast(coalesce(nullif('1531.175', 'nan'), '0') as float), 1393)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41602', 'CO2 Flux', 'uatm', cast(coalesce(nullif('294.555', 'nan'), '0') as float), 1394)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41576', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-101.105', 'nan'), '0') as float), 1395)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('41596', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-152.57', 'nan'), '0') as float), 1396)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37714', 'CO2 Flux', 'uatm', cast(coalesce(nullif('98.1696', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37744', 'CO2 Flux', 'uatm', cast(coalesce(nullif('55.46018', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37775', 'CO2 Flux', 'uatm', cast(coalesce(nullif('32.02244', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37805', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-18.4033', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37836', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-134.317', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37867', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-59.4988', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37897', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-25.1504', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37928', 'CO2 Flux', 'uatm', cast(coalesce(nullif('13.07068', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37958', 'CO2 Flux', 'uatm', cast(coalesce(nullif('43.58015', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37989', 'CO2 Flux', 'uatm', cast(coalesce(nullif('314.9206', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('38020', 'CO2 Flux', 'uatm', cast(coalesce(nullif('12.10373', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('38049', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-57.5745', 'nan'), '0') as float), 1397)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37714', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-71.2874', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37744', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-32.7537', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37775', 'CO2 Flux', 'uatm', cast(coalesce(nullif('65.50733', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37805', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-36.607', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37836', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-34.6804', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37867', 'CO2 Flux', 'uatm', cast(coalesce(nullif('61.65396', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37897', 'CO2 Flux', 'uatm', cast(coalesce(nullif('44.31379', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37928', 'CO2 Flux', 'uatm', cast(coalesce(nullif('82.8475', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37958', 'CO2 Flux', 'uatm', cast(coalesce(nullif('105.9677', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37989', 'CO2 Flux', 'uatm', cast(coalesce(nullif('277.4428', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('38020', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-19.2669', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('38049', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-67.434', 'nan'), '0') as float), 1398)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37714', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-13.4868', 'nan'), '0') as float), 1399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37744', 'CO2 Flux', 'uatm', cast(coalesce(nullif('67.43402', 'nan'), '0') as float), 1399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37775', 'CO2 Flux', 'uatm', cast(coalesce(nullif('21.19355', 'nan'), '0') as float), 1399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37805', 'CO2 Flux', 'uatm', cast(coalesce(nullif('50.09384', 'nan'), '0') as float), 1399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37836', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-19.2669', 'nan'), '0') as float), 1399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37867', 'CO2 Flux', 'uatm', cast(coalesce(nullif('-21.1935', 'nan'), '0') as float), 1399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37897', 'CO2 Flux', 'uatm', cast(coalesce(nullif('25.04692', 'nan'), '0') as float), 1399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37928', 'CO2 Flux', 'uatm', cast(coalesce(nullif('109.8211', 'nan'), '0') as float), 1399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37958', 'CO2 Flux', 'uatm', cast(coalesce(nullif('325.61', 'nan'), '0') as float), 1399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('37989', 'CO2 Flux', 'uatm', cast(coalesce(nullif('215.7889', 'nan'), '0') as float), 1399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('38020', 'CO2 Flux', 'uatm', cast(coalesce(nullif('13.4868', 'nan'), '0') as float), 1399)
    
    
        INSERT INTO co2data_sample ( date, sample_type, unit, measurement, site_location_id) 
        values ('38049', 'CO2 Flux', 'uatm', cast(coalesce(nullif('32.75367', 'nan'), '0') as float), 1399)
    


Delete Cursur, Close DB Connection, AND FINISHED!!!


```python
cur.close()
conn.close()
```

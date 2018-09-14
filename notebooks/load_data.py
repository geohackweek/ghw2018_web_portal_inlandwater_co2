#!/bin/env python
# Elena C Reinisch 20180912
# setup script to load data and put into friendly database

# load libraries
from __future__ import (absolute_import, division, print_function)
import os

import matplotlib as mpl
import matplotlib.pyplot as plt

from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from geopandas import GeoSeries, GeoDataFrame

# load data
co2_data_table = pd.read_excel("../data/co2.xlsx", skiprows=range(1, 2))

# set up geometry
geometry = [Point(xy) for xy in zip(co2_data_table['Longitude'], co2_data_table['Latitude'])]
geometry = GeoSeries(geometry)
geometry.crs = {'init': 'epsg:4326'}

co2_geo_data_table = GeoDataFrame(co2_data_table, geometry=geometry, crs=geometry.crs)

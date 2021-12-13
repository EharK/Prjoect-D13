from os import name
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from pyproj import Proj, transform
import plotly.graph_objects as go
from math import sqrt

df = pd.read_csv("lidarFiles/cameraDriving_back_frames.csv", skipinitialspace=True, usecols= ['autonomous', 'steering_angle', 'vehicle_speed', 'position_x', 'position_y', 'position_z', 'roll', 'pitch', 'yaw'])

def driving_whiteness(df):
    sum=0
    whitenessValues=[]
    D = df.shape[0]
    for i in range(D):
        if i < 2:
            sum += abs(df["steering_angle"][i]/0.1)
        elif i > D-3:
            sum += abs(df["steering_angle"][i]/0.1)
        else:
            sum = abs((df["steering_angle"][i]-df["steering_angle"][i-1])/0.1)
        whitenessValues.append(sqrt((1/D)*sum))
    return whitenessValues

# DATA PREPARATION
df['autonomous'] = df['autonomous'].replace([True, False], [1, 0])
df = df.assign(driving_whiteness=driving_whiteness(df))

def cordsToWSG84(df):
    estcords = Proj(init='epsg:3301')
    worldcords = Proj(init='epsg:4326')
    lon, lat = transform(estcords, worldcords, df.position_x+650000, df.position_y+6465000)
    return (lat, lon)

def plotByColor(df, color, title="Driving trajectory"):
    lat, lon = cordsToWSG84(df)

    fig = px.scatter_mapbox(df, lat=lat, lon=lon, size_max=5, zoom=12.5, height=800, width=1900, color=color,
        hover_data={'autonomous': True, 'position_x': False, 'position_y': False, 'position_z': False, 'roll': False, 'pitch': False, 'yaw': False}, 
        title=title, opacity=0.4)
    
    fig.add_trace(go.Scattermapbox(
         lat=lat,
         lon=lon,
         mode='markers',
         marker=go.scattermapbox.Marker(
            size=df["autonomous"].tolist(),
            color='rgb(255,255,255)',
            sizemin=1.3,
         ),
         name="  TOGGLE -> Autonomous driving"
     ))

    fig.update_layout(mapbox_style="open-street-map")
    fig.show()

#plotByColor(df, "vehicle_speed", "Trajectory")
#plotByColor(df, "position_z", "Trajectory")
plotByColor(df, 'driving_whiteness', "Trajectory")
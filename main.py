import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from pyproj import Proj, transform

df = pd.read_csv("lidarFiles/cameraDriving_froward_frames.csv", skipinitialspace=True, usecols= ['autonomous','vehicle_speed', 'position_x', 'position_y', 'position_z', 'roll', 'pitch', 'yaw'])

# DATA PREPARATION
df['autonomous'] = df['autonomous'].replace([True, False], [1, 0])

def cordsToWSG84(df):
    estcords = Proj(init='epsg:3301')
    worldcords = Proj(init='epsg:4326')
    lon, lat = transform(estcords, worldcords, df.position_x+650000, df.position_y+6465000)
    return (lat, lon)

def plotByColor(df, color, title):
    lat, lon = cordsToWSG84(df)
    
    fig = px.scatter_mapbox(df, lat=lat, lon=lon, size=df['autonomous'].tolist(), size_max=10, zoom=12.5, height=1000, width=1900, 
        hover_data={'autonomous': True, 'position_x': False, 'position_y': False, 'position_z': False, 'roll': False, 'pitch': False, 'yaw': False}, 
        color_discrete_sequence=[("black", 0), ("black", 1)], title=title, opacity=0.4)

    fig.add_trace(px.scatter_mapbox(df, lat=lat, lon=lon, color=color).data[0])

    # fig.add_trace(go.Scattermapbox(
    #     lat=lat,
    #     lon=lon,
    #     mode='markers',
    #     marker=go.scattermapbox.Marker(
    #         size=df['autonomous'].tolist(),
    #         sizemin=1,
    #         color='rgb(0,255,0)',
    #         opacity=0.7
    #     ),
    #     below="fig",
    #     hoverinfo='none'
    # ))

    fig.update_layout(mapbox_style="open-street-map")
    fig.show()

plotByColor(df, "vehicle_speed", "Trajectory")
plotByColor(df, "position_z", "Trajectory")
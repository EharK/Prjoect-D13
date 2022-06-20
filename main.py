import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pyproj import Proj, transform
import plotly.graph_objects as go
from math import sqrt

df = pd.read_csv("lidarFiles/lidar_frames.csv", skipinitialspace=True, usecols= ['autonomous', 'steering_angle', 'vehicle_speed', 'position_x', 'position_y', 'position_z', 'roll', 'pitch', 'yaw'])


# ------------------- DRIVING WHITENESS ---------------------
def driving_whiteness(df):
    whitenessValues=[]
    D = df.shape[0]  
    for i in range(D):
        sum=0
        keskmisteArv=0
        for j in range(i-20, i+21):
            if not j>D-1 and not j<1:
                keskmisteArv+=1
                sum += abs(df["steering_angle"][j]-df["steering_angle"][j-1])
        sum = sum/keskmisteArv
        whitenessValues.append(sqrt((1/D)*sum))
    return whitenessValues
# -----------------------------------------------------------



# ------------------- DATA PREPARATION ----------------------

# converts true/false values to numeric values (0 and 1) to
# use it as a size scale when creating a trace on the map
df.autonomous = df.autonomous.replace([True, False], [1, 0])

# calculates driving whiteness with previously defined function
# and assigns returned values to a dataframe column
df = df.assign(driving_whiteness=driving_whiteness(df))

# converts m/s -> km/h
df.vehicle_speed = df.vehicle_speed*60*60/1000

# -----------------------------------------------------------



# ------------------ COORDINATE SYSTEM ----------------------
def cordsToWSG84(df):
    estcords = Proj(init='epsg:3301')       # Estonian Coordinate System of 1997
    worldcords = Proj(init='epsg:4326')     # World Geodetic System 1984

    # actual conversion with pyproj -->
    longitude, latitude = transform(estcords, worldcords, df.position_x+650000, df.position_y+6465000)

    return (latitude, longitude)
# -----------------------------------------------------------



# ----------- GENERIC PLOT-ON-MAP FUNCTION ------------------
def plotByColor(df, color, title="Driving trajectory"):

    # converts epsg:3301 from csv to epsg:4326 WSG84 coordinate system -->
    lat, lon = cordsToWSG84(df)

    # generates main trace on map that represents the main information of the 
    # plot (speed/height/whiteness of the driving) based on the functions "color" 
    # variable value (one of the dataframe column names)
    fig = px.scatter_mapbox(df, lat=lat, lon=lon, size_max=5, zoom=12.5, height=960, width=1800, color=color,
        hover_data={'autonomous': True, 'position_x': False, 'position_y': False, 'position_z': False, 'roll': False, 'pitch': False, 'yaw': False}, 
        title=title)
    
    # generates the trace of autonomous drivin on the map which exists 
    # when the car is driving by itself but disappears when driving
    # is taken over by the driver
    fig.add_trace(go.Scattermapbox(
         lat=lat,
         lon=lon,
         mode='markers',
         marker=go.scattermapbox.Marker(
            size=df["autonomous"].tolist(),
            color='rgb(255,255,255)',
            sizemin=1.3,
            opacity=0.8
         ),
         # spaces necessary to get rid of overlaping titles -->
         name="                                       TOGGLE -> Autonomous driving"
     ))
    fig.update_layout(mapbox_style="open-street-map")
    fig.show()
# -----------------------------------------------------------

# FOLLOWING TRACES ARE ALL COMBINED WITH AUTONOMOUS 
# DRIVING TRACE (white) THAT CAN BE TOGGLED

# generates trace showcasing vehicle speed
plotByColor(df, "vehicle_speed", "Trajectory")
# generates trace showcasing the height of driving from sea-level
plotByColor(df, "position_z", "Trajectory")
# generates trace showcasing driving whiteness
plotByColor(df, 'driving_whiteness', "Trajectory")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 14:30:41 2021

@author: aaronhenry
"""


import plotly
import plotly.tools as tls

import numpy as np
import pandas as pd
from sqlalchemy import create_engine # database connection
import datetime as dt
from IPython.display import display

# import chart_studio.plotly as py # interactive graphing
import plotly.io as pio
import plotly.graph_objs as go
import plotly.offline as py
import plotly.express as px
from plotly.subplots import make_subplots
pio.renderers.default='browser'

from baseball_scraper import playerid_lookup
from baseball_scraper import statcast_pitcher


#READ IN LOCAL CSV to SQLITE DB

pd.read_csv('JacobDegrom.csv', nrows=2).head()

#wc -l < JacobDegrom.csv # Number of lines in dataset IN TERMINAL

disk_engine = create_engine('sqlite:///JacobDegrom.db') # Initializes database with filename 311_8M.db in current directory

start = dt.datetime.now()

chunksize = 100
j = 0
index_start = 1

for df in pd.read_csv('JacobDegrom.csv', chunksize=chunksize, iterator=True, encoding='utf-8'):

    df = df.rename(columns={c: c.replace(' ', '') for c in df.columns}) # Remove spaces from columns

   # df['CreatedDate'] = pd.to_datetime(df['CreatedDate']) # Convert to datetimes
   # df['ClosedDate'] = pd.to_datetime(df['ClosedDate'])

    df.index += index_start

   # # Remove the un-interesting columns
   # columns = ['Agency', 'CreatedDate', 'ClosedDate', 'ComplaintType', 'Descriptor',
   #            'CreatedDate', 'ClosedDate', 'TimeToCompletion',
   #           'City']

   # for c in df.columns:
   #    if c not in columns:
   #        df = df.drop(c, axis=1)


    j+=1
    #print '{} seconds: completed {} rows'.format((dt.datetime.now() - start).seconds(), j*chunksize)

    df.to_sql('data', disk_engine, if_exists='append')
    index_start = df.index[-1] + 1
    
    
#------------------------------------------------------------
    
    
#pitch locations SQL query
heat = pd.read_sql_query('SELECT plate_x, plate_z, pitch_name, stand '
                         'FROM data', disk_engine)

#pitch location plot
fig3 = go.Figure()
for p in heat['pitch_name'].unique()[:4]:
    for s in heat['stand'].unique()[:2]:
        df = heat[heat['pitch_name']==p]
    
        fig3.add_traces(go.Scatter(x=df.loc[df['stand'] == s, 'plate_x'], y=df.loc[df['stand'] == s, 'plate_z'], name = p+" "+s+" "+"Handed", mode="markers"))
    

fig3.add_trace(
    go.Scatter(x=[-0.85,0.85,0.85,-0.85,-0.85], y=[3.5,3.5,1.5,1.5,3.5], mode="lines", showlegend=False))

fig3.layout.xaxis.range = [-2, 2]
fig3.layout.yaxis.range = [0, 5]
fig3.update_layout(height=700, width=700, title_text="L/R Jacob Degrom 2020 Pitch Location Plots")
fig3.write_html("LR JacobDegrom2020.html")

fig3.show()


#using statcast directly --- YU DARVISH 2020 EXAMPLE

playerid_lookup('darvish', 'yu')

darvish_stats = statcast_pitcher("2020-1-1", "2021-1-1", 506433)

#pitch location scatter plot
fig4 = go.Figure()
for p in darvish_stats['pitch_name'].unique()[:6]:
    for s in darvish_stats['stand'].unique()[:2]:
        df = darvish_stats[darvish_stats['pitch_name']==p]
    
        fig4.add_traces(go.Scatter(
            x=df.loc[df['stand'] == s, 'plate_x'], 
            y=df.loc[df['stand'] == s, 'plate_z'], 
            text=df['release_speed'].astype(str) + " MPH",
            name = p+" "+s+" "+"Handed", mode="markers"))
    
fig4.add_trace(
    go.Scatter(x=[-0.85,0.85,0.85,-0.85,-0.85], y=[3.5,3.5,1.5,1.5,3.5], mode="lines", showlegend=False))

fig4.update_traces(marker=dict(opacity=0.8))
fig4.layout.xaxis.range = [-2, 2]
fig4.layout.yaxis.range = [0, 5]
fig4.update_layout(height=700, width=700, title_text="L/R Yu Darvish 2020 Pitch Locator")


fig4.write_html("LR YuDarvish2020.html")

fig4.show()



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 14:30:41 2021

@author: aaronhenry
"""


import pandas as pd
from sqlalchemy import create_engine # database connection

# import chart_studio.plotly as py # interactive graphing
import plotly.io as pio
import plotly.graph_objs as go
pio.renderers.default='browser'

from baseball_scraper import playerid_lookup
from baseball_scraper import statcast_pitcher


def SpecifyDataSource():
    fname = input('First name: ') 
    lname = input('Last name: ')
    return fname, lname
    
#Ask user
local_or_scrape = input('Do you have a statcast .csv with the name of your pitcher in your working directory? (y/n): ')
fname, lname = SpecifyDataSource()

#READ IN LOCAL CSV to SQLITE DB

#-----------------------------------------------------------
# Initializes database with filename in current working directory
disk_engine = create_engine('sqlite:///' + fname + lname + '.db') 
#-----------------------------------------------------------


#Read in CSV in chunks
#Setting desired chunksize
chunksize = 100
#Indexing tools
j = 0
index_start = 1

if local_or_scrape in ('y', 'yes', 'Yes', 'Yep'):

    for df in pd.read_csv(fname + lname +'.csv', chunksize=chunksize, iterator=True, encoding='utf-8'):
    
    # Remove spaces from columns
        df = df.rename(columns={c: c.replace(' ', '') for c in df.columns}) 


        df.index += index_start
        j+=1

        df.to_sql('data', disk_engine, if_exists='append')
        index_start = df.index[-1] + 1
else:
    pass
 
#------------------------------------------------------------
    

#pitch locations SQL query
heat = pd.read_sql_query('SELECT plate_x, plate_z, pitch_name, stand '
                         'FROM data', disk_engine)

#pitch location plot
fig3 = go.Figure()
for p in heat['pitch_name'].unique()[:4]:
    for s in heat['stand'].unique()[:2]:
        df = heat[heat['pitch_name']==p]
        fig3.add_traces(go.Scatter(x=df.loc[df['stand'] == s, 'plate_x'], 
                                   y=df.loc[df['stand'] == s, 'plate_z'], 
                                   name = p+" "+s+" "+"Handed", mode="markers"))
#Strikezone
fig3.add_trace(
    go.Scatter(x=[-0.85,0.85,0.85,-0.85,-0.85], 
               y=[3.5,3.5,1.5,1.5,3.5], 
               mode="lines", showlegend=False))

#Axes and titling / saving
fig3.layout.xaxis.range = [-2, 2]
fig3.layout.yaxis.range = [0, 5]
fig3.update_layout(height=700, width=700, title_text= fname + lname + "Pitch Location Plot")
fig3.write_html(fname + lname + "PitchLocator.html")

fig3.show()


#------------------------------------------------------------
#using statcast directly --- YU DARVISH 2020 EXAMPLE


playerid = pd.DataFrame(playerid_lookup(lname, fname)).iloc[0]['key_mlbam']

darvish_stats = statcast_pitcher("2020-1-1", "2021-1-1", playerid)

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
    go.Scatter(x=[-0.85,0.85,0.85,-0.85,-0.85], 
               y=[3.5,3.5,1.5,1.5,3.5], 
               mode="lines", showlegend=False))

fig4.update_traces(marker=dict(opacity=0.8))
fig4.layout.xaxis.range = [-2, 2]
fig4.layout.yaxis.range = [0, 5]
fig4.update_layout(height=700, width=700, title_text= fname + lname + "Pitch Location Plot")
fig4.write_html(fname + lname + "Pitch Locator.html")

fig4.show()



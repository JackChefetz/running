import streamlit as st
import pandas as pd
import altair as alt
import sys
import os

# Set page config for wide layout
st.set_page_config(layout="wide")

st.title("Running Data Dashboard")

# Add src to path and load data
sys.path.append(os.path.abspath('src'))
from load_and_merge import load_and_merge

df = load_and_merge()

def time_to_minutes(pace):
    """Convert Avg Pace (in M:SS) to a numeric value (total minutes)"""
    parts = pace.split(':')
    if len(parts) == 2:
        minutes = float(parts[0])
        seconds = float(parts[1])
        return minutes + seconds/60
    return None

def time_to_hours(pace):
    """Convert Avg Pace (in HH:MM:SS) to a numeric value (total hours)"""
    parts = pace.split(':')
    if len(parts) == 3:
        hours = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        return hours + minutes/60 + seconds/3600
    return None

df['avg_pace_minutes'] = df['Avg Pace'].apply(time_to_minutes)
df['time_hours'] = df['Time'].apply(time_to_hours)
df['Calories'] = pd.to_numeric(df['Calories'], errors='coerce')
df['cal/hr'] = df['Calories'] / df['time_hours']

brush = alt.selection_interval(
    encodings=['x','y'],
    resolve='intersect')

col = alt.condition(brush, alt.Color('Location:N'), alt.ColorValue('rgba(200, 200, 200, 0.4)'))

# Base histogram: shows all data in gray
p11_base = alt.Chart(df).mark_bar(color='gray').encode(
    x=alt.X('Distance:Q', bin=alt.Bin(maxbins=28), title='Distance'),
    y=alt.Y('count()', title='Count')
)

# Overlay: shows only the selected data, colored by location
p11_selected = alt.Chart(df).mark_bar().encode(
    x=alt.X('Distance:Q', bin=alt.Bin(maxbins=28)),
    y='count()',
    color=alt.Color('Location:N')
).transform_filter(brush)

# Combine the layers
p11 = (p11_base + p11_selected).add_params(brush).properties(width=430, height=260)

p21 = alt.Chart(df).mark_circle().encode(
    x=alt.X('Date:T', title='Date'),
    y=alt.Y('Distance:Q', title='Distance'),
    color=col
).add_params(brush).properties(width=550, height=260)

p31 = alt.Chart(df).mark_circle().encode(
    x='Distance:Q',
    y=alt.Y('avg_pace_minutes:Q', title='Average Pace (minutes)', scale=alt.Scale(domain=[7,11])),
    color=col
).add_params(brush).properties(width=350, height=260)

p41 = alt.Chart(df).mark_circle().encode(
    x='Date:T',
    y=alt.Y('avg_pace_minutes:Q', title='Average Pace (minutes)', scale=alt.Scale(domain=[7,11])),
    color=col
).add_params(brush).properties(width=350, height=260)

p51 = alt.Chart(df).mark_circle().encode(
    x='Distance:Q',
    y=alt.Y('Avg HR:Q', scale=alt.Scale(domain=[130,190])),
    color=col
).add_params(brush).properties(width=350, height=260)

fig = alt.vconcat(p11, p21, p31, p41, p51)

# Display the chart
st.altair_chart(fig, use_container_width=False)

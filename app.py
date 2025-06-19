# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 18:32:27 2025

@author: Admin
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Simulated dataset ---
np.random.seed(42)
cities = ['Delhi', 'Mumbai', 'Bangalore']
dates = pd.date_range(start='2024-01-01', periods=10, freq='M')
data = []

for city in cities:
    values = np.random.randint(70, 100, size=10)
    for d, v in zip(dates, values):
        data.append({'Date': d, 'City': city, 'Value': v})

df = pd.DataFrame(data)

# --- UI: City Selection ---
st.title("City-wise Trend Dashboard with Significance Highlighting")
city = st.selectbox("Select City", df['City'].unique())

# --- Filter by City ---
city_df = df[df['City'] == city].copy()
city_df['Significant'] = city_df['Value'] > 88  # simple significance test

# --- Chart: Line + Colored Points ---
fig = go.Figure()

# Line (always gray)
fig.add_trace(go.Scatter(
    x=city_df['Date'],
    y=city_df['Value'],
    mode='lines',
    name='Value Trend',
    line=dict(color='lightgray'),
))

# Colored points
for sig in [True, False]:
    subset = city_df[city_df['Significant'] == sig]
    fig.add_trace(go.Scatter(
        x=subset['Date'],
        y=subset['Value'],
        mode='markers',
        name='Significant' if sig else 'Not Significant',
        marker=dict(
            color='red' if sig else 'blue',
            size=10
        )
    ))

# Layout
fig.update_layout(
    title=f"{city} - Value Over Time",
    xaxis_title='Date',
    yaxis_title='Value',
    legend_title='Point Type',
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

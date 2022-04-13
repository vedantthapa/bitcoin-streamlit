#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   app.py
@Time    :   2022/04/13 15:46:11
@Author  :   Vedant Thapa 
@Contact :   thapavedant@gmail.com
'''

import pandas as pd
import streamlit as st
from bitcoin import *

st.title("Bitcoin Prices")
st.write("""This app plots the Bitcoin Prices over the specified interval of time in the selected currency. You may hover over the graph to see the tooltip.""")

days = st.slider("No of Days", min_value=1, max_value=365, value=90)
currency = st.radio("Currency", options=('CAD', 'USD', 'INR'))

df = get_prices(days, currency)

st.subheader("Graph")
col1, col2 = st.columns(2)
with col1:
    adjust_scale = st.checkbox("Adjust Scale")
with col2:
    avg_line = st.checkbox("Show Average Line")

st.altair_chart(plot_prices(df, include_zero=not adjust_scale,
                rule=avg_line), use_container_width=True)

st.text(
    f"Average value for the selected time period is {round(df.Prices.mean(), 2)} {currency}")

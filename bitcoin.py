#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   bitcoin.py
@Time    :   2022/04/13 15:06:36
@Author  :   Vedant Thapa 
@Contact :   thapavedant@gmail.com
'''

import requests
import pandas as pd
import altair as alt


def get_prices(days, currency):
    response = requests.get(
        f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency={currency}&days={days}&interval=daily")
    data = pd.DataFrame(response.json()["prices"], columns=['Date', 'Prices'])
    data['Date'] = pd.to_datetime(data['Date'], unit="ms")

    return data


def plot_prices(source, x="Date", y="Prices", include_zero=True, rule=False):

    hover = alt.selection_single(
        fields=[x],
        nearest=True,
        on="mouseover",
        empty="none",
        clear="mouseout"
    )

    base = alt.Chart(source)

    area = (
        base
        .mark_area(
            line={'color': 'gray'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='white', offset=0.05),
                       alt.GradientStop(color='gray', offset=1)],
                x1=1,
                x2=1,
                y1=1,
                y2=0
            )
        )
        .encode(alt.X('Date:T'), alt.Y('Prices:Q', scale=alt.Scale(zero=include_zero)))
    )

    tooltips = (
        base
        .mark_rule(opacity=0)
        .encode(
            x=x,
            y=y,
            tooltip=[x, alt.Tooltip(y, format=".2f")],
        )
        .add_selection(hover)
    )
    if rule:
        rule = base.mark_rule(strokeDash=[12, 6], size=3, color='red').encode(
            y='average(Prices)',
        )
        return (area + rule + tooltips)
    else:
        return (area + tooltips)

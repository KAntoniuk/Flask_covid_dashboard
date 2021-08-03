import plotly
from flask import Flask, render_template, send_file, request, Response, flash

import time

from pandas._config import dates
from uk_covid19 import Cov19API
import ipywidgets as wdg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
# import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go

from data_analysis.analysis import (
    access_api, create_df1
)

app = Flask(__name__)


@app.route('/')
@app.route("/index")
def index():
    access_api()
    uk_df = create_df1("overview.json")

    graphs_cases = [
        go.Bar(
            x=uk_df.index,  # assign x as the dataframe column 'x'
            y=uk_df['cases'],
            name="Daily cases",
            showlegend=False,
            hovertemplate="%{y:,.0f}"
        )
    ]

    cases_layout = dict(
        {
            "title": {
                "text": "Daily New Cases",
                "font": {"family": "Roboto", "size": 18},
            },
            "margin": {
                "l": 40,
                "r": 40,
                "t": 65,
                "b": 40,
            },
            "hovermode": "x unified",
            "hoverlabel": {
                "bgcolor": "white",
                "font_size": 16,
                "font_family": "Roboto",
            },
            "yaxis": {"fixedrange": True},
        }
    )

    deaths_layout = dict(
        {
            "title": {
                "text": "Daily New Cases",
                "font": {"family": "Roboto", "size": 18},
            },
            "margin": {
                "l": 40,
                "r": 40,
                "t": 65,
                "b": 40,
            },
            "hovermode": "x unified",
            "hoverlabel": {
                "bgcolor": "white",
                "font_size": 16,
                "font_family": "Roboto",
            },
            "yaxis": {"fixedrange": True},
        }
    )




    graphs_deaths = [
        go.Bar(
            x=uk_df.index,  # assign x as the dataframe column 'x'
            y=uk_df['deaths'],
            name="Daily deaths",
            showlegend = False,
            hovertemplate = "%{y:,.0f}"

        )
    ]

    cases_dict = dict(data=graphs_cases, layout=cases_layout)
    deaths_dict = dict(data=graphs_deaths, layout=deaths_layout)


    figuresJSON1 = json.dumps(cases_dict, cls=plotly.utils.PlotlyJSONEncoder)
    figuresJSON2 = json.dumps(deaths_dict, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        'index.html',
        plot1=figuresJSON1,
        plot2=figuresJSON2
    )


if __name__ == '__main__':
    app.run()

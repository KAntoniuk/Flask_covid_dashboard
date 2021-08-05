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
    access_api, create_df1, get_current_numbers
)
from data_analysis.vaccinations import (
    download_vaccinations, create_vac_df)


app = Flask(__name__)


@app.route('/')
@app.route("/index")
def index():
    access_api()
    download_vaccinations()
    uk_df = create_df1("overview.json")
    vac_df = create_vac_df("vaccinations.json")

    uk_current_cases, uk_current_deaths = get_current_numbers(uk_df)

    cases_graph = []
    death_graph = []
    vac_graph=[]

    cases_graph.append(
        go.Bar(
            x=uk_df.index,  # assign x as the dataframe column 'x'
            y=uk_df['cases'],
            name="Daily cases",
            showlegend=False,
            hovertemplate="%{y:,.0f}:",
            #marker_color="#34568B"

        )
    )

    cases_graph.append(
        go.Scatter(
            x=uk_df.date.tolist(),
            y=uk_df["7dayCases"].tolist(),
            name="7 day moving average",
            showlegend=False,
            hovertemplate="%{y:,.0f}",
        )
    )

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
                "text": "Daily New Deaths",
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

    death_graph.append(
        go.Bar(
            x=uk_df.index,  # assign x as the dataframe column 'x'
            y=uk_df['deaths'],
            name="Daily deaths",
            showlegend=False,
            hovertemplate="%{y:,.0f}",
            #marker_color="#FF6F61"
        )
    )

    death_graph.append(
        go.Scatter(
            x=uk_df.date.tolist(),
            y=uk_df["7dayDeaths"].tolist(),
            name="7 day moving average",
            showlegend=False,
            hovertemplate="%{y:,.0f}",
        )
    )

    vac_graph.append(
        go.Scatter(
            x=vac_df.date.tolist(),
            y=vac_df["firstDose"].tolist(),
            name="First dose",
            showlegend=False,
            hovertemplate="%{y:,.0f}",
        )
    )

    vac_graph.append(
        go.Scatter(
            x=vac_df.date.tolist(),
            y=vac_df["secondDose"].tolist(),
            name="Second dose",
            showlegend=False,
            hovertemplate="%{y:,.0f}",
        )
    )

    vac_layout = dict(
        {
            "title": {
                "text": "Vaccination doses",
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

    cases_dict = dict(data=cases_graph, layout=cases_layout)
    deaths_dict = dict(data=death_graph, layout=deaths_layout)
    vac_dict = dict(data=vac_graph, layout=vac_layout)

    figuresJSON1 = json.dumps(cases_dict, cls=plotly.utils.PlotlyJSONEncoder)
    figuresJSON2 = json.dumps(deaths_dict, cls=plotly.utils.PlotlyJSONEncoder)
    figuresJSON3 = json.dumps(vac_dict, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        'index.html',
        plot1=figuresJSON1,
        plot2=figuresJSON2,
        plot3=figuresJSON3,
        uk_current_cases=f"{uk_current_cases:,.0f}",
        uk_current_deaths=f"{uk_current_deaths:,.0f}"
    )


if __name__ == '__main__':
    app.run()

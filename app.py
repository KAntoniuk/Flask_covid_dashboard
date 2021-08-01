import plotly
from flask import Flask, render_template, send_file, request, Response, flash

import time
from uk_covid19 import Cov19API
import ipywidgets as wdg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
# import seaborn as sns

from data_analysis.analysis import (
    access_api, create_df1, return_graphs
)

app = Flask(__name__)


@app.route('/')
@app.route("/index")
def index():
    access_api()
    uk_current_cases = create_df1("overview.json")

    graphs = return_graphs(uk_current_cases)
    ids = [f"figure-{i}" for i, _ in enumerate(graphs)]
    figuresJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template(
        'index.html',
        ids=ids,
        figuresJSON=figuresJSON,
        uk_current_cases=uk_current_cases
    )


if __name__ == '__main__':
    app.run()

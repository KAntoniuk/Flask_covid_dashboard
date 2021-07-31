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
def index():
    access_api()
    df1 = create_df1("overview.json")
    print(df1)
    graphs = return_graphs(df1)
    figuresJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', figuresJSON=figuresJSON)


if __name__ == '__main__':
    app.run()

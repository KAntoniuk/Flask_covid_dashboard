from flask import Flask, render_template, send_file, request, Response, flash


import time
from uk_covid19 import Cov19API
import ipywidgets as wdg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
#import seaborn as sns

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
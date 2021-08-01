from uk_covid19 import Cov19API
import time
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt


def access_api():
    filters1 = [
        "areaType=overview"
    ]

    structure1 = {
        "date": "date",
        "cases": "newCasesByPublishDate",
        "hospital": "hospitalCases",
        "deaths": "newDeaths28DaysByPublishDate",
    }

    filters2 = [
        'areaType=nation',
        'areaName=England'
    ]

    structure2 = {
        "date": "date",
        "hospital": "hospitalCases",
        "ventilator": "covidOccupiedMVBeds"
    }

    filters3 = [
        'areaType=nation',
        'areaName=England'
    ]

    structure3 = {
        "males": "maleCases",
        "females": "femaleCases"
    }

    api_overview = Cov19API(filters=filters1, structure=structure1)
    overview = api_overview.get_json()

    time.sleep(1)

    api_ventilator = Cov19API(filters=filters2, structure=structure2)
    ventilator = api_ventilator.get_json()

    time.sleep(1)

    api_age = Cov19API(filters=filters3, structure=structure3)
    age = api_age.get_json()

    with open("overview.json", "wt") as OUTF:
        json.dump(overview, OUTF)

    with open("ventilator.json", "wt") as OUTF:
        json.dump(ventilator, OUTF)

    with open("age.json", "wt") as OUTF:
        json.dump(age, OUTF)


def parse_date(date_string):
    return pd.to_datetime(date_string, format="%Y-%m-%d")


def create_df1(file):
    """creates a pandas dataframe from a "json" dictionary from uk-covid19 API software development kit"""
    with open(file, "rt") as INFILE:
        data = json.load(INFILE)
    data_list = data['data']
    dates = [dictionary['date'] for dictionary in data_list]
    dates.sort()
    startdate = parse_date(dates[0])
    enddate = parse_date(dates[-1])

    index = pd.date_range(startdate, enddate, freq='D')
    df = pd.DataFrame(index=index, columns=['date', 'cases', 'hospital', 'deaths'])

    for entry in data_list:
        date = parse_date(entry['date'])
        for column in ['cases', 'hospital', 'deaths']:
            if pd.isna(df.loc[date, column]):
                value = float(entry[column]) if entry[column] != None else 0.0
                df.loc[date, column] = value
        df.loc[date, 'date'] = date




    df.fillna(0.0, inplace=True)
    print(df)
    return df


def create_df2(file):
    '''creates a pandas dataframe from a "json" dictionary from uk-covid19 API software development kit'''
    with open(file, "rt") as INFILE:
        data = json.load(INFILE)
    data_list = data['data']
    dates = [dictionary['date'] for dictionary in data_list]
    dates.sort()
    startdate = parse_date(dates[0])
    enddate = parse_date(dates[-1])

    index = pd.date_range(startdate, enddate, freq='D')
    df = pd.DataFrame(index=index, columns=['hospital', 'ventilator'])

    for entry in data_list:
        date = parse_date(entry['date'])
        for column in ['hospital', 'ventilator']:
            if pd.isna(df.loc[date, column]):
                value = float(entry[column]) if entry[column] != None else 0.0
                df.loc[date, column] = value

    df.fillna(0.0, inplace=True)
    return df


def create_df3(file):
    '''creates a pandas dataframe from a "json" dictionary from uk-covid19 API software development kit'''
    with open(file, "rt") as INFILE:
        data = json.load(INFILE)

    datadic = data['data'][0]
    males = datadic['males']
    females = datadic['females']

    ageranges = [x['age'] for x in males]

    def min_age(agerange):
        agerange = agerange.replace('+', '')  # remove the + from 90+
        start = agerange.split('_')[0]
        return int(start)

    ageranges.sort(key=min_age)

    df = pd.DataFrame(index=ageranges, columns=['Males', 'Females', 'Total'])

    for entry in males:
        ageband = entry['age']  # our index position
        df.loc[ageband, 'Males'] = entry['value']

    for entry in females:
        ageband = entry['age']
        df.loc[ageband, 'Females'] = entry['value']

    df['Total'] = df['Males'] + df['Females']

    for entry in males:  # each entry is a dictionary
        ageband = entry['age']  # our index position
        df.loc[ageband, 'Males'] = entry['value']

    for entry in females:
        ageband = entry['age']
        df.loc[ageband, 'Females'] = entry['value']

    df['Total'] = df['Males'] + df['Females']

    df.fillna(0.0, inplace=True)
    return df

def return_graphs(df):
    cases_graph = []
    cases_graph.append(
        go.Bar(
            x=df.date.tolist(),
            y=df.cases.tolist(),
            name="UK Overview",
            showlegend=False,
            #hovertemplate="%{y:,.0f}",
        )
    )
    #cases_graph.append(
     #   go.Scatter(
      #      x=df.date.tolist(),
       #     y=df["7dayCases"].tolist(),
        #    name="7 day moving average",
         #   showlegend=False,
       #     hovertemplate="%{y:,.0f}",
       # )
    #)

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
    graphs=[]
    graphs.append(dict(data=cases_graph, layout=cases_layout))
    return graphs


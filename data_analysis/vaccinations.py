from uk_covid19 import Cov19API
import json
import pandas as pd

def download_vaccinations():

    filters1 = [
        "areaType=overview"
    ]

    structure1 = {
        "date": "date",
        "firstDose": "cumPeopleVaccinatedFirstDoseByPublishDate",
        "secondDose": "cumPeopleVaccinatedSecondDoseByPublishDate"
    }

    api_vac = Cov19API(filters=filters1, structure=structure1)
    vac_json = api_vac.get_json()

    with open("vaccinations.json", "wt") as OUTF:
        json.dump(vac_json, OUTF)

def parse_date(date_string):
    return pd.to_datetime(date_string, format="%Y-%m-%d")

def create_vac_df(file):
    with open(file, "rt") as INFILE:
        data = json.load(INFILE)
        data_list = data['data']
        dates = [dictionary['date'] for dictionary in data_list]
        dates.sort()
        startdate = parse_date(dates[0])
        enddate = parse_date(dates[-1])

        index = pd.date_range(startdate, enddate, freq="D")
        df = pd.DataFrame(index=index, columns=['date', 'firstDose', 'secondDose'])

        for entry in data_list:
            date = parse_date(entry["date"])
            for column in ['firstDose', 'secondDose']:
                value = float(entry[column])
                df.loc[date, column] = value
            df.loc[date, 'date'] = date

        print(df)
        return df
download_vaccinations()
create_vac_df('vaccinations.json')





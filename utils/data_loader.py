import pandas as pd

def load_tick_data(path='data/Tick Sightings.xlsx'):
    df = pd.read_excel(path)

    df = df.drop_duplicates()
    df['date'] = pd.to_datetime(df['date'], errors="coerce")

    return df
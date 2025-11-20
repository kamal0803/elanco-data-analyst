import pandas as pd

def load_tick_data(path='data/Tick Sightings.xlsx'):
    df = pd.read_excel(path)

    dict_species_latinName = {}

    for idx, row in df.iterrows():
        if pd.notna(row['species']) and pd.notna(row['latinName']) and row[
            'species'] not in dict_species_latinName.keys():
            dict_species_latinName[row['species']] = row['latinName']

    for idx, row in df.iterrows():
        if pd.isna(df.at[idx, 'species']):

            latinName = df.at[idx, 'latinName']

            for species, latin in dict_species_latinName.items():
                if latin == latinName:
                    df.at[idx, 'species'] = species

    for idx, row in df.iterrows():
        if pd.isna(df.at[idx, 'latinName']):
            species = df.at[idx, 'species']

            if species in dict_species_latinName:
                df.at[idx, 'latinName'] = dict_species_latinName[species]

    df = df.drop_duplicates()
    df['date'] = pd.to_datetime(df['date'], errors="coerce")

    return df
import pandas as pd
import numpy as np

# def process_in_chunk(chunk):
#     chunk.drop_duplicates(inplace=True)
#     chunk['date'] = pd.to_datetime(chunk['date'], errors="coerce")

def load_tick_data(path='data/Tick Sightings.xlsx'):

    # For handling large datasets
    # 1. Process data in batches instead of entire data frame.
    # Since now dataframe has just 1000 rows, chunking will slow down processing because of multiple for loop calls

    # IMPLEMENTED BELOW

    # df = pd.read_excel(path)
    #
    # chunk_size = 100
    #
    # for i in range(0, len(df), chunk_size):
    #     chunk = df.iloc[i:i + chunk_size]
    #     process_in_chunk(chunk)

    df = pd.read_excel(path)

    dict_species_latinName = {}

    # Dictionary for mapping species with their latinName
    for idx, row in df.iterrows():
        if pd.notna(row['species']) and pd.notna(row['latinName']) and row[
            'species'] not in dict_species_latinName.keys():
            dict_species_latinName[row['species']] = row['latinName']

    # Filling missing species name using latinName
    for idx, row in df.iterrows():
        if pd.isna(df.at[idx, 'species']):

            latinName = df.at[idx, 'latinName']

            for species, latin in dict_species_latinName.items():
                if latin == latinName:
                    df.at[idx, 'species'] = species

    # Filling missing latinName name using species
    for idx, row in df.iterrows():
        if pd.isna(df.at[idx, 'latinName']):
            species = df.at[idx, 'species']

            if species in dict_species_latinName:
                df.at[idx, 'latinName'] = dict_species_latinName[species]

    # Filling location basis on probability distribution
    location_probabilities = df['location'].value_counts(normalize=True)
    df['location'] = df['location'].fillna(np.random.choice(location_probabilities.index, p=location_probabilities.values))

    # Since data is very sparse its's challenging to estimate date values which are missing, so they are dropped.
    # IMP - General thumb rule is to drop columns if it's less < 5 % of overall data
    df = df.dropna(subset=['date'])

    df = df.drop_duplicates()
    df['date'] = pd.to_datetime(df['date'], errors="coerce")

    return df
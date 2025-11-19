import pandas as pd

def sightings_per_region(df):
    region_counts = df.groupby("location").size().reset_index(name="count")
    return region_counts.to_dict(orient="records")


def weekly_trends(df):
    df_copy = df.copy()
    df_copy["week"] = df_copy["date"].dt.isocalendar().week
    weekly = df_copy.groupby("week").size().reset_index(name="count")
    return weekly.to_dict(orient="records")


def monthly_trends(df):
    df_copy = df.copy()
    df_copy["month"] = df_copy["date"].dt.month
    monthly = df_copy.groupby("month").size().reset_index(name="count")
    return monthly.to_dict(orient="records")

# def species_by_location(df, location):
#     df_copy = df.copy()
#
#     # Filter by location (case-insensitive)
#     df_copy = df_copy[df_copy["location"].str.contains(location, case=False, na=False)]
#
#     # Get species counts per location
#     species_counts = df_copy.groupby("species").size().reset_index(name="count")
#
#     return species_counts.to_dict(orient="records")


def species_by_location(df, location):

    location = location.strip()
    cities = df['location'].unique()

    if location not in cities:
        return None

    d = {}
    species_list = df['species'].unique()

    for city in cities:
        d[city] = {}   # create inner dict for each city

        for sp in species_list:
            count = len(df[(df['location'] == city) & (df['species'] == sp)])
            d[city][sp] = count

    return d[location]

def species_count_by_city(df):
    d = {}

    cities = df['location'].unique()
    species_list = df['species'].unique()

    for city in cities:
        d[city] = {}   # create inner dict for each city

        for sp in species_list:
            count = len(df[(df['location'] == city) & (df['species'] == sp)])
            d[city][sp] = count

    return d

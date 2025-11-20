import pandas as pd

def filter_data(df, start=None, end=None, location=None):

    df_copy = df.copy()
    df_copy["date"] = pd.to_datetime(df_copy["date"], errors="coerce")

    if start:
        try:
            start_date = pd.to_datetime(start, errors="raise")
        except Exception:
            return {"error": "Invalid start date format. Use YYYY-MM-DD"}, None

        df_copy = df_copy[df_copy["date"] >= start_date]

    if end:
        try:
            end_date = pd.to_datetime(end, errors="raise")
        except Exception:
            return {"error": "Invalid end date format. Use YYYY-MM-DD"}, None

        df_copy = df_copy[df_copy["date"] <= end_date]
    if location:
        df_copy = df_copy[df_copy["location"].str.lower() == location.strip().lower()]

    return None, df_copy

def sightings_per_location_aggregate(df):

    location_counts = df.groupby("location").size().reset_index(name="count")

    return location_counts.to_dict(orient="records")


def weekly_trends(df):

    df_copy = df.copy()
    df_copy["week"] = df_copy["date"].dt.isocalendar().week
    weekly = df_copy.groupby("week").size().reset_index(name="count")

    return weekly.to_dict(orient="records")


def monthly_trends(df):

    df_copy = df.copy()
    df_copy["month"] = df_copy["date"].dt.month
    monthly = df_copy.groupby("month").size().reset_index(name="count")

    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    monthly["month"] = (monthly.index+1).map(month_names)

    return monthly.to_dict(orient="records")

def yearly_trends(df):

    df_copy = df.copy()
    df_copy["year"] = df["date"].dt.year
    yearly = df_copy.groupby("year").size().reset_index(name="count")

    return yearly.to_dict(orient="records")

def species_by_each_location(df, location):

    if location is None or location.strip() == "":
        return {"error": "No location provided. Please provide a location"}, 400

    location = location.strip().lower()

    cities = [c.lower() for c in df['location'].unique()]

    if location not in cities:
        return {
            "error": f"'{location}' is not a valid city.",
            "valid_cities": list(df["location"].unique())
        }, 404

    d = {}
    species = df["species"].unique()

    for sp in species:
        count = len(df[(df["location"].str.lower() == location) &
                       (df["species"] == sp)])
        d[sp] = count

    return d, 200

def species_count_by_all_locations(df):
    d = {}

    cities = df['location'].unique()
    species_list = df['species'].unique()

    for city in cities:
        d[city] = {}

        for sp in species_list:
            count = len(df[(df['location'] == city) & (df['species'] == sp)])
            d[city][sp] = count

    return d

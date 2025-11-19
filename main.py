from flask import Flask, jsonify, request, render_template
from utils.data_loader import load_tick_data
from utils.aggregations import sightings_per_region, weekly_trends, monthly_trends,species_count_by_city, species_by_location
import pandas as pd

app = Flask(__name__)

df = load_tick_data()

@app.route("/")
def home():
    return {"message": "Elanco Tick Sighting API is running!"}

@app.route("/sightings", methods=["GET"])
def get_sightings():
    return jsonify(df.to_dict(orient="records"))

@app.route("/filter", methods=["GET"])
def filter_data():
    df_copy = df.copy()

    start = request.args.get("start")
    end = request.args.get("end")

    location = request.args.get("location")
    df_copy["date"] = pd.to_datetime(df_copy["date"], errors="coerce")


    if start:
        df_copy = df_copy[df_copy["date"] >= pd.to_datetime(start)]
    if end:
        df_copy = df_copy[df_copy["date"] <= pd.to_datetime(end)]
    if location:
        df_copy = df_copy[df_copy["location"].str.lower() == location.strip().lower()]

    return jsonify(df_copy.to_dict(orient="records"))

@app.route("/stats/regions")
def region_stats():
    return jsonify(sightings_per_region(df))

@app.route("/stats/trends")
def trends():
    return { "weekly": weekly_trends(df), "monthly": monthly_trends(df) }

@app.route("/dashboard-data")
def dashboard_data():
    return { "monthly": monthly_trends(df), "weekly": weekly_trends(df), "regions": sightings_per_region(df) }

@app.route("/stats/species", methods=["GET"])
def species_stats():
    location = request.args.get("location")

    if not location:
        return jsonify({"error": "Please provide a location parameter"}), 400

    result = species_by_location(df, location)

    if result is None:
        return jsonify({
            "error": f"'{location}' is not a valid city. "
                     f"Valid cities are: {list(df['location'].unique())}"
        }), 404

    return jsonify(result)

@app.route("/stats/cities")
def city_stats():
    return jsonify(species_count_by_city(df))



if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, jsonify, request
from utils.data_loader import load_tick_data
from utils.aggregations import (sightings_per_location_aggregate, yearly_trends, weekly_trends,
                                monthly_trends,species_count_by_all_locations, filter_data, species_by_each_location)
from functools import lru_cache
app = Flask(__name__)

df = load_tick_data()

@app.route("/")
def home():
    return {"message": "API is running!"}

@lru_cache(maxsize=1)
@app.route("/sightings", methods=["GET"])
def get_sightings():
    return jsonify(df.to_dict(orient="records"))

@app.route("/filter", methods=["GET"])
def filter():

    start = request.args.get("start")
    end = request.args.get("end")
    location = request.args.get("location")

    error, filter_df = filter_data(df, start=start, end=end, location=location)

    if error:
        return jsonify(error), 400

    return jsonify(filter_df.to_dict(orient="records"))

@app.route("/stats/locations")
def location_stats_aggregate():

    return jsonify(sightings_per_location_aggregate(df))

@app.route("/dashboard-data")
def dashboard_data():

    return { "weekly": weekly_trends(df), "monthly": monthly_trends(df),
             "yearly": yearly_trends(df)}


@app.route("/stats/location-species", methods=["GET"])
def species_stats():
    location = request.args.get("location")

    result, status = species_by_each_location(df, location)

    return jsonify(result), status

@app.route("/stats/all-locations-species")
def all_location_stats():
    return jsonify(species_count_by_all_locations(df))

if __name__ == "__main__":
    app.run(debug=True)
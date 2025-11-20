from flask import Flask, jsonify, request, render_template
from utils.data_loader import load_tick_data
from utils.aggregations import (sightings_per_region, yearly_trends, weekly_trends,
                                monthly_trends,species_count_by_location, filter_data, species_by_location)

app = Flask(__name__)

df = load_tick_data()

@app.route("/")
def home():
    return {"message": "API is running!"}

@app.route("/sightings", methods=["GET"])
def get_sightings():
    return jsonify(df.to_dict(orient="records"))

@app.route("/filter", methods=["GET"])
def filter():

    start = request.args.get("start")
    end = request.args.get("end")
    location = request.args.get("location")

    filter_df = filter_data(df, start, end, location)

    return jsonify(filter_df.to_dict(orient="records"))

@app.route("/stats/regions")
def region_stats():
    return jsonify(sightings_per_region(df))

@app.route("/stats/trends")
def trends():
    return { "weekly": weekly_trends(df), "monthly": monthly_trends(df) }

@app.route("/dashboard-data")
def dashboard_data():

    return { "weekly": weekly_trends(df), "monthly": monthly_trends(df),
             "yearly": yearly_trends(df), "regions": sightings_per_region(df)}


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
    return jsonify(species_count_by_location(df))

if __name__ == "__main__":
    app.run(debug=True)
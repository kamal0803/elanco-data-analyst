# Elanco Placement Program: Technical Task - Backend

This project involves developing a backend MVP with Python and Flask to process and serve tick-sighting data provided by Elanco.

## Overview

The backend loads and processes tick-sighting data, applies filters, computes trends, and provides species and location statistics via REST API endpoints. Data is stored in a Pandas Dataframe.

The system is designed with clean separation of concerns, consistent error handling, and future scalability in mind.

## Architecture & Key Design Choices

### Modular Choices

All data processing logic of filtering, trend calculations, species aggregation, and data cleaning is implemented inside the `utils/` module.

Implementation of defining routes, passing request parameters to the utility functions, and returning JSON responses is done in `main.py`.

This separation ensures a cleaner architecture where so that the application is easier to maintain, extend, or debug.

### Caching and Logging

Frequent endpoints (e.g., `/sightings`) use lru_cache to avoid recomputing results.

Basic logging in this application captures when certain endpoints are hit, invalid date or location values and successful operations.

### Consistent Error Handling

A robust error handling mechanism is implemented to catch errors such as invalid date formats, invalid or missing locations. An appropriate error message is displayed with a status code.

### Data Preprocessing

In the utils/ module, several data cleaning operations are performed:

a. Filling missing species/Latin names using dictionary mapping, filling missing values of location by probability distribution, dropping missing dates
b. Chunking to handle large datasets (soft implementation)
c. Removing duplicates


## Endpoints

GET `/sightings`
Returns the complete tick-sightings dataset in JSON format.

GET `/filter?start=YYYY-MM-DD&end=YYYY-MM-DD&location=location`
It accepts 3 optional parameters of start date, end date and location, and returns a filtered subset of the dataset. A robust error handling is implemented to display error messages and status code when encountered.

GET `/stats/locations`
Returns aggregated sighting counts per location.

GET `/trends`
Returns a JSON object containing weekly trends, monthly trends and yearly trends.

GET `/stats/location-species?location=location`
It accepts a mandatory location as parameter. Returns species-level counts for the given location.

GET `/stats/all-locations-species`
Returns a JSON object showing the count of each species across all locations.

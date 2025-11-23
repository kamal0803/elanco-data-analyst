# Elanco Placement Program: Technical Task - MVP Backend

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

- The dataset may contain several missing fields such as _species_, _Latin names_, _locations_, and _dates_. Each type of missing value is handled using an appropriate strategy.
  - Missing Species / Latin Names
    - A dictionary is created for mapping species with their corresponding Latin names.
    - Any missing value is filled based on the dictionary to ensure internal consistency.
  - Missing Locations
    - Location values are imputed using a probability-based approach by calculating the frequency distribution of existing locations.
    - Each missing location is filled by random sampling from this distribution.
  - Missing date
    - Since the data is very sparse, it’s challenging to estimate date values for missing values, removal is the safest option. Following common data quality guidance, if fewer than 5% of rows have missing values for a critical field, it is generally acceptable to drop them.
- Chunking to handle large datasets (soft implementation)
- Removing duplicates


## Endpoints

GET `/sightings` <br />
Returns the complete tick-sightings dataset in JSON format.

GET `/filter?start=YYYY-MM-DD&end=YYYY-MM-DD&location=location` <br />
It accepts 3 optional parameters of start date, end date and location, and returns a filtered subset of the dataset. A robust error handling is implemented to display error messages and status code when encountered.

GET `/stats/locations` <br />
Returns aggregated sighting counts per location.

GET `/trends` <br />
Returns a JSON object containing weekly trends, monthly trends and yearly trends.

GET `/stats/location-species?location=location` <br />
It accepts a mandatory location as parameter. Returns species-level counts for the given location.

GET `/stats/all-location-species` <br />
Returns the count of each species across all locations.

## AI/ML Insights (Extension Task)

### Machine Learning model to predict ticks for the upcoming weeks
A machine learning model is built to predict ticks for any location for upcoming n-weeks. Since the data is very sparse, ARIMA (Autoregressive Integrated Moving Average) is preferred over Deep Learning, which is the usual choice for time-series data. 

Deep Learning methods are data hungry algorithms, requiring large volumes of data. ARIMA, on the other hand, works extremely well on small time series, capturing trends with minimal data.

For this task, ARIMA provides a practical and accurate solution, with very low MAE (Mean Absolute Error) on training data.

### Use of MLFlow
MLflow is a state-of-the-art platform for tracking machine learning experiments. It allows logging model parameters, metrics, artifacts, and comparing multiple runs through an intuitive UI. This makes it easy to evaluate different model configurations and identify which version of the model performs best.

In this project, MLflow is used to compare how variations in ARIMA hyperparameters (p, d, q) influence forecasting accuracy. By logging metrics such as MAE and MSE across several runs, MLflow provides a clear, visual way to understand which configuration offers the strongest predictive performance.

In principle, MLflow plays a key role in enabling MLOps practices such as experiment tracking, reproducibility, and comparison across model versions.

Currently, the ML model is kept outside the main API to keep the backend service lightweight and focused, and to support independent experimentation in line with good MLOps practices. A future enhancement would be to integrate the ML model into the backend.

## How to run the project

### Prerequisites
- Python 3.9+
- pip installed
- Virtual environment (recommended)

### Steps to run in the terminal
- git clone https://github.com/kamal0803/elanco-data-analyst
- cd elanco-data-analyst
- pip install -r requirements.txt
- python main.py

The front-end UI is accessible at `http://127.0.0.1:5000`

## Future Enhancements (if more time was available)
- Writing unit tests using pytest for end-to-end testing.
- Integrating the ML model developed to predict the ticks in upcoming weeks in the backend.
- Persistence storage using databases such as PostgreSQL to support larger datasets.
- Apply more MLOps principles by
  - Setting up a CI/CD pipeline using Github actions to automate workflows.
  - Package the entire application using Docker, and integrate it with MLFlow by running MLFlow tracking server in Docker.
  - Deploying the models in the cloud.

## References

- https://pandas.pydata.org/docs/user_guide/scale.html
- System Design Interview - An Insider’s Guide by Alex Xu

## Related Experience

I have previously developed backend and data-processing applications using Flask, Pandas, and REST APIs, which strengthened my skills in API design, data validation, and clean backend architecture. This experience directly contributed to how I structured the Elanco MVP backend.

### Relevant Github projects

- Flask Movie App - https://github.com/kamal0803/flask-top-movies-app
- Flask Cafe App - https://github.com/kamal0803/flask-cafe-application
- Node.js Travel Tracker - https://github.com/kamal0803/Travel-Tracker

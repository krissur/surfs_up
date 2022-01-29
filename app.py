# import our dependencies 
import datetime as dt
import numpy as np
import pandas as pd

# Add the SQLAlchemy dependencies after the other dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import the dependencies that we need for Flask
from flask import Flask, jsonify

# set up our database engine for the Flask application
    #create_engine() function allows us to access and query our SQLite database file
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes  w/ prepare () function (base= database) explanation in 9.1.5
Base = automap_base()
Base.prepare(engine, reflect=True)

# save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# create a Flask application called "app"
app = Flask(__name__)

# define the welcome route using the code below route 1
@app.route("/")
# add routing info below
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

    # referencing above cell-  When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route. 
#This convention signifies that this is version 1 of our application. 
#This line can be updated to support future versions of the app as well.

#creating NEW ROUTE-preciptation  Every time you create a new route, your code should be aligned to the left in order to avoid errors
@app.route("/api/v1.0/precipitation")
#create the precipitation() function
def precipitation():
  prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365) #add the line of code that calculates the date one year ago from the most recent date in the database
  precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all() #previous year
  precip = {date: prcp for date, prcp in precipitation}
  return jsonify(precip)

  # create Stations Route
@app.route("/api/v1.0/stations")  
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#create Temperature Route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#create stats route with a start & end date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

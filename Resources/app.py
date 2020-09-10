import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func
from flask import Flask, jsonify
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station=Base.classes.station
app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )
@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_query = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_query.append(prcp_dict)

    return jsonify(all_query)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation"""
    results = session.query(Measurement.station).all()

    session.close()

    all_stations=list(np.ravel(results))
   

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    year_prior_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_data = session.query(Measurement.tobs).filter(
        Measurement.date >= year_prior_date).filter(Measurement.station == 'USC00519281').all()
    
    all_temps = list(np.ravel(year_data))
    return jsonify(all_temps)


@app.route("/api/v1.0/temp/<start>")
def start(start):
    session= Session(engine)
    
    temp_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    temps_start = list(np.ravel(temp_start))
    return jsonify(temps_start)


@app.route("/api/v1.0/temp/<start>/<end>")
def end_start(start,end):
    session = Session(engine)

    temp_end_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temps_end_start = list(np.ravel(temp_end_start))
    return jsonify(temps_end_start)


if __name__ == '__main__':
    app.run(debug=True)

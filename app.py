import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify


##Setting up the Database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model # reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# We can view all of the classes that automap found;# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

##Setting up Flask
app = Flask(__name__)

###Writing Flask Route
@app.route("/")
def homepage():

    return(
        f"Welcome to my page!<br><br>"
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"Date format is yyyy-mm-dd <br>"
        f"/api/v1.0/start<br>"
        f"Date format is yyyy-mm-dd/yyyy-mm-dd<br>"
        f"/api/v1.0/start/end<br>"

    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    year_ago

# Perform a query to retrieve the data and precipitation scores
    Prcp_results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago).all()
    prcplist = [Prcp_results]
    return jsonify(prcplist)

@app.route("/api/v1.0/stations")
def stations():
    stations_results = session.query(Station.station, Station.name).all()
    
    stations = {}
    for station in stations_results:
        # station_dict = {
            stations[station[0]]=station[1]
        
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tempsofobs():
    active_stations = session.query(Measurement.station,func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    active_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station==active_stations[0][0]).\
    filter(Measurement.date>=year_ago).all()
    ###creating empty list to store all values
    alltobs = []
    for temp in active_tobs:
        tobs_dict = {}
        tobs_dict ["date"] = temp.date
        tobs_dict ["tobs"] = temp.tobs
        alltobs.append(tobs_dict)
    return jsonify(alltobs)

##Date format is yyyy-mm-dd
@app.route("/api/v1.0/<start>/")
def startdate(start):
    temp_station = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date>=start).group_by(Measurement.date).all()
    # sdate = {}
    # for dates in temp_station:
    #     sdate[dates[0]]={dates[1],dates[2],round(dates[3],0)}
    
    sdate = []
    for dates in temp_station:
        datedict = {}
        datedict['Start Date'] = start
        datedict['Average Temperature'] = float(dates[3])
        datedict['Highest Temperature'] = float(dates[2])
        datedict['Lowest Temperature'] = float(dates[1])
        sdate.append(datedict)
    return jsonify(sdate)      

##Date format is yyyy-mm-dd/yyyy-mm-dd
@app.route("/api/v1.0/<start>/<end>/")
def startenddate(start, end):
    send_station = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date>=start,Measurement.date<=end).group_by(Measurement.date).all()
    sendate = {}
    for sendate in send_station:
        sendate['Start Date'] = start
        sendate['Average Temperature'] = float(sendate[3])
        sendate['Highest Temperature'] = float(sendate[2])
        sendate['Lowest Temperature'] = float(sendate[1])
    return jsonify(sendate)  
app.run(debug=True)
        # sdate.append(datedict)
    # for sendates in send_station:
    #     sendate[sendates[0]]={sendates[1],sendates[2],sendates[3]}
    
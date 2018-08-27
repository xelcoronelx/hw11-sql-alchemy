from flask import Flask, jsonify


import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)

prev_date = dt.date(2017,8,23) - dt.timedelta(days=365)

@app.route('/')
def home():
    return 'Welcome to the Home Page'



@app.route('/api/v1.0/precipitation')
def precipitation_route():
    # one year ago from last date
    
    precip_results = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date > prev_date).all()

    precip_data = {date: prcp for date, prcp in precip_results}
    return jsonify(precip_data)


@app.route('/api/v1.0/stations')
def station_route():
    stations = session.query(Station.station).all()
    station_list = []
    for item in stations:
        station_list.append(item[0])

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs_route():
    
    tobs = results = session.query(Measurement.tobs)\
                     .filter(Measurement.date > prev_date).all()
    tobs_list = []
    for item in tobs:
        tobs_list.append(item[0])
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def start_route(start=None):
    # for a given start date...

    Beginning_day =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                     .filter(Measurement.date >= start)
    
    results1 = [row[:3] for row in Beginning_day]
    
    return jsonify(results1)





#     return 'Welcome to the Home Page'

# @app.route('/api/v1.0/<start>/<end>')
# def home():
#     return 'Welcome to the Home Page'



if __name__ == '__main__':
    app.run(debug=True)
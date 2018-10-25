# Weather Station Monitoring

weatherstation is a python-based application that provides a dashboard showing output from multiple temperature sensors located in the house. 

It currently has the capability of monitoring and outputing temperature data from the sensors but the application has the potential to be extended to forecasting as well.

![Dashboard screenshot](screenshot.png)

Figure 1: Temperature time series from different sensors within the house. Time resolution is 5 minutes.

The x-axis represents the timestamp with 5-minute resolution whereas the y-axis stands for the temperatures in Celcius. There is the option to display data from the last three days (default), last day and last hour.

The present graph represents monitored data from all sensors in the house. Measurements are taken 12 times within the hour, i.e. every 5 minutes.

## How to setup

weatherstation is written using python and uses a library called dash, which provides interactive plot.ly graphs to show the output. If you have docker already installed, you don't need to worry about python installation.

You'll need to ensure your weather station is logging temperatures into a database with time and temp columns, like this:

```
time | temp
----------
2018-06-03T14:45:35|21.312
2018-06-03T14:47:57|21.312
2018-06-03T14:50:19|21.375
2018-06-03T14:52:41|21.312
2018-06-03T14:55:03|21.312
2018-06-03T14:57:25|21.312
2018-06-03T14:59:48|21.375
```
This is a UTC datetime and a temperature in degrees celsius as a numeric(5,3)

Add the database connection details to a file called database.ini (see the example)

To start the dashboard run:

```
docker run --name weather -d -p 5000:5000 -v $(pwd)/database.ini:/app/conf/database.ini lucyb/weatherstation
```

Then access the dashboard in a browser, using the address http://localhost:5000

### First way

To build it without docker:
```
cd app
pip3 install -r requirements.txt
cd web
python app.py
```

### Second way

To build your own docker image:

1. Checkout this code 
2. Add the connection details to the database in app/database.ini
3. Then run:
```
docker build . -t weatherstation
```

## Future work
In the future:

1. Display more historical data from each sensor.
2. Another important part of the work will focus on analysing the monitored data and also forecasting temperatures and humidity levels for the next hour (short-term forecasting). 
3. Output the monitored data from more sensors.

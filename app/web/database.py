import configparser
import pandas as pd

def sensor_list():
    conn = _connection_string()
    #sql = 'SELECT sensor_id, name, max(time_to) FROM sensor_locations GROUP BY sensor_id, name'
    sql = 'SELECT id, sensor as name FROM sensors'
    return pd.read_sql(sql, conn)


def all_temp_data(id):
    conn = _connection_string()
    sql = f'SELECT time as "Time", reading as "Temp" FROM sensor_readings WHERE sensor_id={id} ORDER BY time'
    return pd.read_sql(sql, conn)


def current_temp(id=None):
    conn = _connection_string()
    if id:
        sql = f'SELECT reading as "Temp" FROM sensor_readings WHERE sensor_id={id} ORDER BY time DESC LIMIT 1'
        df = pd.read_sql(sql, conn)
        return df.Temp.iloc[0]

    sql = ('SELECT s.sensor, r1.reading '
    'FROM sensor_readings r1 '
    'INNER JOIN sensors s '
    'ON s.id = r1.sensor_id '
    'INNER JOIN (SELECT sensor_id, MAX(time) AS time '
    'FROM sensor_readings '
    'WHERE measure_type = \'temperature\' '
    'GROUP BY sensor_id) r2 '
    'ON r1.sensor_id = r2.sensor_id AND r1.time = r2.time '
    'WHERE r1.measure_type = \'temperature\'')

    df = pd.read_sql(sql, conn)
    return df


def _connection_string():
    config = _parse_config()
    host = config["host"]
    database = config["db"]
    user = config["username"]
    password = config["password"]

    connect = "postgresql://{}:{}@{}/{}".format(user, password, host, database)
    return connect


def _parse_config():
    config = configparser.ConfigParser()
    config.read('../conf/database.ini')
    return config['database']

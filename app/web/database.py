import configparser
import pandas as pd

def sensor_list():
    conn = _connection_string()
    sql = ('SELECT sensor_id as id, name '
            'FROM sensor_locations '
            'WHERE time_to is NULL '
            'GROUP BY sensor_id, name')
    return pd.read_sql(sql, conn)

def temp_data_last_day(id, measure_type):
    conn = _connection_string()
    sql = ('SELECT time as "Time", reading as "Temp" '
            'FROM sensor_readings '
            f'WHERE sensor_id={id} '
            'AND time >= NOW() - \'1 day\'::INTERVAL '
            f'AND measure_type = \'{measure_type}\' '
            'ORDER BY time')
    return pd.read_sql(sql, conn)

def all_temp_data(id):
    conn = _connection_string()
    sql = ('SELECT time as "Time", reading as "Temp" '
            'FROM sensor_readings '
            f'WHERE sensor_id={id} '
            'AND measure_type =\'temperature\' '
            'ORDER BY time')
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

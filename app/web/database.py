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
            'AND time >= NOW() - \'3 days\'::INTERVAL '
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


def current_reading(ids=[]):
    sensor_ids = ','.join(map(str,ids))
    conn = _connection_string()

    sql = ('SELECT r1.sensor_id as id, r1.reading, r1.measure_type '
            'FROM sensor_readings r1 '
            'INNER JOIN (SELECT sensor_id, measure_type, MAX(time) AS time '
            'FROM sensor_readings '
            'GROUP BY sensor_id, measure_type) r2 '
            'ON r1.sensor_id = r2.sensor_id '
            'AND r1.time = r2.time '
            'AND r1.measure_type = r2.measure_type '
            f'WHERE r1.sensor_id in ({sensor_ids}) '
            'ORDER BY r1.sensor_id, r1.measure_type')

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

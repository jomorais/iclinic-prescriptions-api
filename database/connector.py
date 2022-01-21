from peewee import SqliteDatabase, MySQLDatabase

DEFAULT_BTBASE_SETTINGS = {
  "database_name": "iclinic",
  "connector": "mysql",
  "host": "db",
  "user": "root",
  "password": "iclinic",
  "port": 3306
}


def sqlite_connector():
    return SqliteDatabase('Prescriptions.sqlite')


def mysql_connector():
    return MySQLDatabase(DEFAULT_BTBASE_SETTINGS['database_name'],
                         user=DEFAULT_BTBASE_SETTINGS['user'],
                         password=DEFAULT_BTBASE_SETTINGS['password'],
                         host=DEFAULT_BTBASE_SETTINGS['host'],
                         port=DEFAULT_BTBASE_SETTINGS['port'])


def get_connector():
    return mysql_connector()

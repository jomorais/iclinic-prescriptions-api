from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase

DEFAULT_BTBASE_SETTINGS = {
  "database_name": "iclinic",
  "connector": "postgresql",
  "host": "db",
  "user": "iclinic",
  "password": "iclinic",
  "port": 5432
}


def sqlite_connector():
    return SqliteDatabase('Prescriptions.sqlite')


def mysql_connector():
    return MySQLDatabase(DEFAULT_BTBASE_SETTINGS['database_name'],
                         user=DEFAULT_BTBASE_SETTINGS['user'],
                         password=DEFAULT_BTBASE_SETTINGS['password'],
                         host=DEFAULT_BTBASE_SETTINGS['host'],
                         port=DEFAULT_BTBASE_SETTINGS['port'])


def postgresql_connector():
    return PostgresqlDatabase(DEFAULT_BTBASE_SETTINGS['database_name'],
                              user=DEFAULT_BTBASE_SETTINGS['user'],
                              password=DEFAULT_BTBASE_SETTINGS['password'],
                              host=DEFAULT_BTBASE_SETTINGS['host'],
                              port=DEFAULT_BTBASE_SETTINGS['port'])


def get_connector():
    return postgresql_connector()

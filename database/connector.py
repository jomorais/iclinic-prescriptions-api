from peewee import SqliteDatabase


def sqlite_connector():
    return SqliteDatabase('Prescriptions.sqlite')


def get_connector():
    return sqlite_connector()

from database.connector import get_connector
from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase


def test_connector_sqlite():
    def setup():
        return get_connector(connector="sqlite")

    connector = setup()
    assert type(connector) == SqliteDatabase


def test_connector_mysql():
    def setup():
        return get_connector(connector="mysql")

    connector = setup()
    assert type(connector) == MySQLDatabase


def test_connector_postgresql():
    def setup():
        return get_connector(connector="postgresql")

    connector = setup()
    assert type(connector) == PostgresqlDatabase

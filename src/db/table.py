from sqlalchemy import Column, Integer, MetaData, String, Table

from settings import LANGUAGES_DB_TABLE_NAME, PERIODIC_DB_TABLE_NAME

"""DB table used for storing languages per Discord channel."""
languages_table = Table(
    LANGUAGES_DB_TABLE_NAME,
    MetaData(),
    Column("channel_id", Integer(), primary_key=True),
    Column("language", String(), nullable=False),
)

"""DB table used for storing periodic media data per Discord channel."""
periodic_table = Table(
    PERIODIC_DB_TABLE_NAME,
    MetaData(),
    Column("channel_id", Integer(), primary_key=True),
    Column("interval", Integer(), nullable=False),
)

from sqlalchemy import Column, Integer, MetaData, String, Table

from settings import LANGUAGES_DB_TABLE_NAME

"""DB table used for storing languages per Discord channel."""
languages_table = Table(
    LANGUAGES_DB_TABLE_NAME,
    MetaData(),
    Column("channel_id", String(), primary_key=True),
    Column("language", String(), nullable=False),
)

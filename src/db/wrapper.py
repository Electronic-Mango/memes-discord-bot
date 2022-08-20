"""
Wrapper for SQLite DB, used for storing languages per Discord channel.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker

from db.model import LanguageModel
from db.table import languages_table
from settings import LANGUAGES_DB_PATH

_engine = create_engine(f"sqlite:///{LANGUAGES_DB_PATH}")
_session = sessionmaker(_engine)


def initialize_database() -> None:
    """Initialize DB, map model with table, create table if necessary"""
    mapper(LanguageModel, languages_table)
    languages_table.create(_engine, checkfirst=True)


def store_language(channel_id: int, language: str) -> None:
    """Store text language to Discord channel ID mapping"""
    with _session() as session:
        session.merge(LanguageModel(channel_id, language))
        session.commit()


def remove_language(channel_id: int) -> None:
    """Remove stored language for a given Discord channel ID"""
    with _session() as session:
        session.query(LanguageModel).filter(LanguageModel.channel_id == channel_id).delete()
        session.commit()


def get_language(channel_id: int) -> str:
    """Get stored language for a given Discord channel ID, or None if absent"""
    with _session() as session:
        model = session.query(LanguageModel).filter(LanguageModel.channel_id == channel_id).first()
        return model.language if model else None

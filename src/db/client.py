"""
Wrapper for SQLite DB, used for storing languages per Discord channel.
"""

from logging import getLogger

from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker

from db.model import LanguageModel, PeriodicModel
from db.table import languages_table, periodic_table
from settings import CHANNEL_DATA_DB_PATH

_logger = getLogger(__name__)
_engine = create_engine(f"sqlite:///{CHANNEL_DATA_DB_PATH}")
_session = sessionmaker(_engine)


def initialize_database() -> None:
    """Initialize DB, map model with table, create table if necessary"""
    _logger.info(f"Initializing the DB [{_engine}]")
    mapper(LanguageModel, languages_table)
    languages_table.create(_engine, checkfirst=True)
    mapper(PeriodicModel, periodic_table)
    periodic_table.create(_engine, checkfirst=True)


def store_language(channel_id: int, language: str) -> None:
    """Store text language to Discord channel ID mapping"""
    _logger.info(f"Storing language [{channel_id}] [{language}]")
    with _session() as session:
        session.merge(LanguageModel(channel_id, language))
        session.commit()


def remove_language(channel_id: int) -> None:
    """Remove stored language for a given Discord channel ID"""
    _logger.info(f"Removing language [{channel_id}]")
    with _session() as session:
        session.query(LanguageModel).filter(LanguageModel.channel_id == channel_id).delete()
        session.commit()


def get_language(channel_id: int) -> str:
    """Get stored language for a given Discord channel ID, or None if absent"""
    _logger.info(f"Getting language [{channel_id}]")
    with _session() as session:
        model = session.query(LanguageModel).filter(LanguageModel.channel_id == channel_id).first()
        _logger.info(f"Found [{model}]")
        return model.language if model else None


def store_interval(channel_id: int, interval: int) -> None:
    """Store Discord channel ID to periodic media interval mapping"""
    _logger.info(f"Storing interval [{channel_id}] [{interval}]")
    with _session() as session:
        session.merge(PeriodicModel(channel_id, interval))
        session.commit()


def remove_interval(channel_id: int) -> None:
    """Remove stored interval for a given Discord channel ID"""
    _logger.info(f"Removing [{channel_id}]")
    with _session() as session:
        session.query(PeriodicModel).filter(PeriodicModel.channel_id == channel_id).delete()
        session.commit()


def get_all_periodic_media_data() -> list[tuple[str, str]]:
    """Get all stored periodic media data"""
    _logger.info("Getting all stored periodic media data")
    with _session() as session:
        all_periodic_data = session.query(PeriodicModel).all()
        parsed_periodic_data = [(data.channel_id, data.interval) for data in all_periodic_data]
        _logger.info(f"Found {parsed_periodic_data}")
        return parsed_periodic_data

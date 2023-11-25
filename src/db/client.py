"""
Wrapper for SQLite DB, used for storing languages per Discord channel.
"""

from logging import getLogger

from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import Session

from db.model import Base, LanguageModel, PeriodicModel
from settings import CHANNEL_DATA_DB_PATH

_logger = getLogger(__name__)
_engine = create_engine(f"sqlite:///{CHANNEL_DATA_DB_PATH}", echo=True)


def initialize_database() -> None:
    """Initialize DB, create tables if necessary"""
    _logger.info(f"Initializing the DB [{_engine}]")
    Base.metadata.create_all(_engine)


def store_language(channel_id: int, language: str) -> None:
    """Store text language to Discord channel ID mapping"""
    _logger.info(f"Storing language [{channel_id}] [{language}]")
    with Session(_engine) as session:
        session.merge(LanguageModel(channel_id=channel_id, language=language))
        session.commit()


def remove_language(channel_id: int) -> None:
    """Remove stored language for a given Discord channel ID"""
    _logger.info(f"Removing language [{channel_id}]")
    with Session(_engine) as session:
        query = delete(LanguageModel).where(LanguageModel.channel_id == channel_id)
        session.execute(query)
        session.commit()


def get_language(channel_id: int) -> str:
    """Get stored language for a given Discord channel ID, or None if absent"""
    _logger.info(f"Getting language [{channel_id}]")
    with Session(_engine) as session:
        query = select(LanguageModel).where(LanguageModel.channel_id == channel_id)
        model = session.execute(query).first()
        _logger.info(f"Found [{model}]")
        return model.language if model else None


def store_interval(channel_id: int, interval: int) -> None:
    """Store Discord channel ID to periodic media interval mapping"""
    _logger.info(f"Storing interval [{channel_id}] [{interval}]")
    with Session(_engine) as session:
        session.merge(PeriodicModel(channel_id=channel_id, interval=interval))
        session.commit()


def remove_interval(channel_id: int) -> None:
    """Remove stored interval for a given Discord channel ID"""
    _logger.info(f"Removing [{channel_id}]")
    with Session(_engine) as session:
        query = delete(PeriodicModel).where(LanguageModel.channel_id == channel_id)
        session.execute(query)
        session.commit()


def get_all_periodic_media_data() -> list[tuple[str, str]]:
    """Get all stored periodic media data"""
    _logger.info("Getting all stored periodic media data")
    with Session(_engine) as session:
        query = select(PeriodicModel)
        all_periodic_data = session.scalars(query).all()
        parsed_periodic_data = [(entry.channel_id, entry.interval) for entry in all_periodic_data]
        _logger.info(f"Found {parsed_periodic_data}")
        return parsed_periodic_data

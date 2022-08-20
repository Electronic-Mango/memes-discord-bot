from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker

from db.model import LanguageModel
from db.table import languages_table
from settings import LANGUAGES_DB_PATH

_engine = create_engine(f"sqlite:///{LANGUAGES_DB_PATH}")
_session = sessionmaker(_engine)


def initialize_database() -> None:
    mapper(LanguageModel, languages_table)
    languages_table.create(_engine, checkfirst=True)


def store_language(channel_id: int, language: str) -> None:
    with _session() as session:
        session.merge(LanguageModel(channel_id, language))
        session.commit()


def remove_language(channel_id: int) -> None:
    with _session() as session:
        session.query(LanguageModel).filter(LanguageModel.channel_id == channel_id).delete()
        session.commit()


def get_language(channel_id: int) -> str:
    with _session() as session:
        model = session.query(LanguageModel).filter(LanguageModel.channel_id == channel_id).first()
        return model.language if model else None

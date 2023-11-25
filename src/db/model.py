from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from settings import LANGUAGES_DB_TABLE_NAME, PERIODIC_DB_TABLE_NAME


class Base(DeclarativeBase):
    pass


class LanguageModel(Base):
    """DB model used for storing languages per Discord channel"""

    __tablename__ = LANGUAGES_DB_TABLE_NAME

    channel_id: Mapped[int] = mapped_column(primary_key=True)
    language: Mapped[int] = mapped_column(nullable=False)


class PeriodicModel(Base):
    """DB model used for storing periodic media data per Discord channel"""

    __tablename__ = PERIODIC_DB_TABLE_NAME

    channel_id: Mapped[int] = mapped_column(primary_key=True)
    interval: Mapped[int] = mapped_column(nullable=False)

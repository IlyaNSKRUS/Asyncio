import os

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String

POSTGRES_DB = os.getenv("POSTGRES_DB", "netology_asyncio_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "qwerty12")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = (f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
          f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = 'swapi_people'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    height: Mapped[str] = mapped_column(String, nullable=True)
    mass: Mapped[str] = mapped_column(String, nullable=True)
    hair_color: Mapped[str] = mapped_column(String, nullable=True)
    skin_color: Mapped[str] = mapped_column(String, nullable=True)
    eye_color: Mapped[str] = mapped_column(String, nullable=True)
    birth_year: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[str] = mapped_column(String, nullable=True)
    homeworld: Mapped[str] = mapped_column(String, nullable=True)
    films: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    species: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    vehicles: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    starships: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    created: Mapped[str] = mapped_column(String, nullable=True)
    edited: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=True)


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()






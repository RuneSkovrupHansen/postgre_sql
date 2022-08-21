from ossaudiodev import SOUND_MIXER_ALTPCM
from sqlalchemy.orm import Session, registry, declarative_base, relationship
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, insert, select, text

import sqlalchemy


def create_engine(type: str, username: str, password: str, address: str, port: str, database: str, echo: bool = False, future: bool = True):
    """Create database from arguments.

    Note that psycopg2 is used as the default dbapi for postgresql databases.
    """

    return sqlalchemy.create_engine(
        f"{type}://{username}:{password}@{address}:{port}/{database}", echo=echo, future=future)


def main():

    engine = create_engine(
        "postgresql",
        username="postgres",
        password="1234",
        address="localhost",
        port="5432",
        database="dvdrental"
    )

    metadata_obj = MetaData()

    film = Table("film", metadata_obj, autoload_with=engine)
    language = Table("language", metadata_obj, autoload_with=engine)

    stmt = select(film.c.title).where(
        film.c.language_id != "2")
    print(stmt)

    with Session(engine) as session:
        result = session.execute(stmt)
        for row in result:
            print(row)

    # print(film.columns)


if __name__ == "__main__":
    main()

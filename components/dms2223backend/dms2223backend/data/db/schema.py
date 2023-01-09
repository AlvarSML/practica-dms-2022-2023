""" Schema class module.
"""
from sqlalchemy import create_engine, event  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.orm import sessionmaker, scoped_session, registry  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.config import BackendConfiguration
from dms2223backend.data.db import Base
from sqlalchemy import MetaData


# Required for SQLite to enforce FK integrity when supported
@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):  # pylint: disable=unused-argument
    """ Sets the SQLite foreign keys enforcement pragma on connection.

    Args:
        - dbapi_connection: The connection to the database API.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.close()


class Schema():
    """ Class responsible of the schema initialization and session generation.
    """

    def __init__(self, base:Base, config: BackendConfiguration):
        """ Constructor method.

        Initializes the schema, deploying it if necessary.

        Args:
            - config (AuthConfiguration): The instance with the schema connection parameters.

        Raises:
            - RuntimeError: When the connection cannot be created/established.
        """
        db_connection_string: str = config.get_db_connection_string() or ''
        self.__create_engine = create_engine(db_connection_string)
        self.__session_maker = scoped_session(sessionmaker(bind=self.__create_engine))
        base.metadata.create_all(bind=self.__create_engine)
        self.__metadata: MetaData = MetaData()
        self.__dec_base: Base = base

    def new_session(self) -> Session:
        """ Constructs a new session.

        Returns:
            - Session: A new `Session` object.
        """
        return self.__session_maker()

    def remove_session(self) -> None:
        """ Frees the existing thread-local session.
        """
        self.__session_maker.remove()

    def clear_database(self) -> None:
        """ !! ELIMINA TODOS LOS DATOS DE LA BASE DE DATOS
            !! SOLO PARA PRUEBAS
        """
        self.__dec_base.metadata.drop_all(bind=self.__create_engine)
        self.__dec_base.metadata.create_all(bind=self.__create_engine)
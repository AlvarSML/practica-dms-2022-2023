""" Modulo para acceso a daros de BDD de usuario
"""
from dms2223backend.data.db import Usuario
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select, exists # type: ignore

class UsuarioFuncs():
    """ Clase con  funciones ORM de usuario
    """
    @staticmethod
    def get_by_nombre(session:Session, nombre:str) -> Usuario:
        """  Se obtiene el id de un usuario mediante su nombre
        """
        stmt = select(Usuario).where(Usuario.nombre == nombre)
        usu:Usuario = session.execute(stmt).first()

        return usu[0]

    @staticmethod
    def get_or_create(session:Session, nombre:str) -> Usuario:
        """  Se obtiene el id de un usuario mediante su nombre
        """
        if session.query(exists().where(Usuario.nombre == nombre)).scalar():
            usu:Usuario = session.query(Usuario).filter_by(nombre=nombre).first()
        else:
            usu:Usuario = UsuarioFuncs.create(session=session,usu=Usuario(nombre=nombre))
        return usu

    @staticmethod
    def create(session:Session, usu:Usuario) -> Usuario:
        """ Se solicita un usuario, si no existe se crea
        """
        session.add(usu)
        session.commit()
        session.refresh(usu)
        return usu

    @staticmethod
    def get_all(session:Session) -> List[Usuario]:
        stmt = select(Usuario)
        usuarios:List[Usuario] = [] 
        for usu in session.execute(stmt):
            usuarios.append(usu[0])
        return usuarios

    @staticmethod
    def get(session:Session,nombre:str) -> Optional[Usuario]:
        usu = session.query(Usuario).filter(Usuario.nombre == nombre).first()
        return usu

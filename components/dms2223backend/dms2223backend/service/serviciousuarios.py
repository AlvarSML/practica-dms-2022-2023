from typing import List, Dict, ClassVar
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db import Schema

from dms2223backend.data.db.Elemento import Pregunta, Respuesta, Comentario
from dms2223backend.data.db import Usuario, Voto
from dms2223backend.data.resultsets import UsuarioFuncs

from sqlalchemy import select

from .authservice import AuthService

class UsuariosServicio():
    @staticmethod
    def get_or_create(schema:Schema,nombre:str) -> Usuario:
        """ Pide un usuario, si no existe lo crea
            Es necesario para asegurar que un usuario autenticado esta
            tambien en la BDD del backend
        """
        session: Session = schema.new_session()
        usu = UsuarioFuncs.get_by_nombre(session,nombre)

        if usu is None:
            usu = UsuarioFuncs.create(
                Usuario(
                    nombre=nombre
                )
            )
            session.add(usu)
            session.commit()
            session.refresh(usu)

        schema.remove_session()
        return usu

    @staticmethod
    def get_all(schema:Schema) -> List[Dict]:
        """ Obtiene todos los usuarios existentes
        """
        session: Session = schema.new_session()
        usuarios:List[Dict] = []
        for usu in UsuarioFuncs.get_all(session):
            usuarios.append({
                "id":usu.id_usuario,
                "nombre":usu.nombre
            })
        return usuarios

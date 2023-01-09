""" Modulo encargado de realizar las consultas de datos a
    la base de datos a traves del ORM
"""

from typing import Optional
from datetime import datetime
from dms2223backend.data.db.Elemento import  Comentario
from sqlalchemy.orm.session import Session  # type: ignore

class ComentarioFuncs():
    """ Calase con funciones estaticas relativas a comentarios
    """
    @staticmethod
    def get(session:Session, cid:int) -> Optional[Comentario]:
        """ Obtiene un comentario activo en la session
        """
        comentario = session.query(Comentario).filter(Comentario.id_comentario == cid).first()
        return comentario

    @staticmethod
    def create(session:Session, comment:Comentario) -> Comentario:
        """ Crea y devuleve un nuevo comentario activo en la session
        """
        session.add(comment)
        session.commit()
        session.refresh(comment)
        return comment
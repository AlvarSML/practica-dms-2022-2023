""" Modulo encargado de realizar las consultas de datos a
    la base de datos a traves del ORM
"""

from typing import List, Dict, Optional
from datetime import datetime

from dms2223backend.data.db.Elemento import  Comentario

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select # type: ignore


import sys

class ComentarioFuncs():

    def get(session:Session, cid:int) -> Comentario:
        """ Obtiene un comentario activo en la session
        """
        comentario = session.query(Comentario).filter(Comentario.id_comentario == cid).first()
        return comentario

    def create(session:Session, comment:Comentario) -> Comentario:
        """ Crea y devuleve un nuevo comentario activo en la session
        """
        session.add(comment)
        session.commit()
        session.refresh(comment)
        return comment
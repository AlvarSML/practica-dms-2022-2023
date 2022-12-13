""" Modulo encargado de realizar las consultas de datos a
    la base de datos a traves del ORM
"""

from typing import List, Dict, Optional
from datetime import datetime

from dms2223backend.data.db.Usuario import Usuario
from dms2223backend.data.db.Elemento import Pregunta, Respuesta, Comentario
from dms2223backend.data.db.Voto import Voto

from dms2223backend.service import RespuestasServicio

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select # type: ignore


import sys

class ComentarioFuncs():

    def get(session:Session, cid:int):
        """ Obtiene un comentario activo en la session
        """
        comentario = session.query(Comentario).filter(Comentario.id_comentario == cid).first()
        return comentario

""" Modulo encargado de realizar las consultas de datos a
    la base de datos a traves del ORM
"""

from typing import List, Dict, Optional
from datetime import datetime

from dms2223backend.data.db import Feedback, Pregunta, Respuesta, Comentario

from dms2223backend.service import RespuestasServicio

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select # type: ignore


import sys

class FeedBackFuncs():

    def get(session:Session, fname:str) -> Feedback:
        """ Obtiene un comentario activo en la session
        """
        feedback = session.query(Feedback) \
            .filter(Feedback.descripcion == fname) \
            .first()
        return feedback

    def create(session:Session, fback:Feedback) -> Feedback:
        """ Crea un tipo nuevo de feedback y lo devuelve
        """
        session.add(fback)
        session.commit()
        session.refresh(fback)
        return(fback)

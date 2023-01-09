""" Modulo encargado de realizar las consultas de datos a
    la base de datos a traves del ORM
"""
from typing import Optional
from datetime import datetime
from dms2223backend.data.db import Feedback, Pregunta, Respuesta, Comentario
from sqlalchemy.orm.session import Session  # type: ignore

class FeedBackFuncs():
    """ Funciones estaticas sobre el feedback
    """
    @staticmethod
    def get(session:Session, fname:str) -> Optional[Feedback]:
        """ Obtiene un comentario activo en la session
        """
        feedback = session.query(Feedback) \
            .filter(Feedback.descripcion == fname) \
            .first()
        return feedback

    @staticmethod
    def create(session:Session, feedback:Feedback) -> Feedback:
        """ Crea un tipo nuevo de feedback y lo devuelve
        """
        session.add(feedback)
        session.commit()
        session.refresh(feedback)
        return(feedback)

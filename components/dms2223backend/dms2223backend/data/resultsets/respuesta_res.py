from typing import List, Dict, Optional
from datetime import datetime


from dms2223backend.data.db.Elemento import Pregunta, Respuesta, Comentario
from dms2223backend.data.db.Voto import Voto

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select # type: ignore


import sys

class RespuestaFuncs():

    @staticmethod
    def create(session:Session, resp:Respuesta) -> Respuesta:
        """ Crea una nueva respuesta a una pregunta y devulve la classe
            activa en la sesión
        """
        session.add(resp)
        session.commit()
        # ! Importante, se recuperoa la pregunta creada, con id fecha y demas datos
        session.refresh(resp)
        return resp

    @staticmethod
    def get(session:Session, aid:int) -> Respuesta:
        """ Obtiene una respuesta activa en la session
        """
        respuesta = session.query(Respuesta).filter(Respuesta.id_respuesta == aid).first()
        return respuesta

from typing import List, Dict, Optional
from datetime import datetime

from dms2223backend.data.db.Usuario import Usuario
from dms2223backend.data.db.Elemento import Pregunta, Respuesta, Comentario
from dms2223backend.data.db import Reporte, ReportePregunta, ReporteRespuesta, ReporteComentario, Estado_moderacion
from dms2223backend.data.db.Voto import Voto

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select # type: ignore

import sys

class ReporteFuncs():

    @staticmethod
    def get_question_reps(session:Session):
        stmt = select(ReportePregunta)
        reps:List[ReportePregunta] = []
        for rep in session.execute(stmt):
            reps.append(rep[0])
        return reps
    
    @staticmethod
    def create_question_reps(session:Session,reporte:ReportePregunta)->ReportePregunta:
        """ Crea un reporte a una pregunta especificamente
        """
        session.add(reporte)
        session.commit()
        session.refresh(reporte)
        return reporte

    @staticmethod
    def create_rep(session:Session,reporte:Reporte) -> Reporte:
        """ Añade un reporte a la session, de cualquier tipo (no se si es aconsejable)
            Principio de liskov*
          !  Como el id es de un elemento se meta lo que se meta deberia funcionar
        """
        session.add(reporte)
        session.commit()
        session.refresh(reporte)
        return reporte

    @staticmethod
    def get_reps(session:Session,tipo:type,estados:List[Estado_moderacion]) -> List[Reporte]:
        """ Obtiene todos los reportes de un tipo
            Permite expandir los estados de moderacion
        """
        print(tipo,file=sys.stderr)
        reps = session.query(tipo).filter(tipo.estado.in_(estados)).all()
        return reps

    @staticmethod
    def set_state(session:Session,reporte:Reporte,estado:Estado_moderacion) -> Reporte:
        """ Cambia el estado de cualquier reporte 
            Lsikov
        """
        reporte.estado = estado
        session.commit()
        session.refresh(reporte)
        return reporte

    @staticmethod
    def get_rep(session:Session,tipo:type ,rid:int) -> Reporte:
        """ Obtiene un reporte segun su id
        """
        return session.query(tipo).filter(tipo.id_reporte == rid).first()


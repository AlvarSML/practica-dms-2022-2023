""" Modulo de para acceder a la BDD sobre reportes
"""
from typing import List, Optional
from dms2223backend.data.db import Reporte, ReportePregunta, Estado_moderacion

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select # type: ignore

class ReporteFuncs():

    @staticmethod
    def get_question_reps(session:Session):
        """ Obtiene todos los reportes a preguntas
            ! Deprecado
        """
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
    def get_rep(session:Session,tipo:type ,rid:int) -> Optional[Reporte]:
        """ Obtiene un reporte segun su id
        """
        return session.query(tipo).filter(tipo.id_reporte == rid).first()


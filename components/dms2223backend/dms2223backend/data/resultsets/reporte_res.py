from typing import List, Dict, Optional
from datetime import datetime

from dms2223backend.data.db.Usuario import Usuario
from dms2223backend.data.db.Elemento import Pregunta, Respuesta, Comentario
from dms2223backend.data.db import Reporte, ReportePregunta, ReporteRespuesta, ReporteComentario
from dms2223backend.data.db.Voto import Voto

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select # type: ignore

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
        session.add(reporte)
        session.commit()
        session.refresh(reporte)
        return reporte

    @staticmethod
    def create_rep(session:Session,reporte:Reporte) -> Reporte:
        """ Añade un reporte a la session, de cualquier tipo
            Principio de liskov
        """
        session.add(reporte)
        session.commit()
        session.refresh(reporte)
        return reporte
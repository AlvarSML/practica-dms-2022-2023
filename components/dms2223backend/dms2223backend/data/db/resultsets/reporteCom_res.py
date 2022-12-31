from typing import List, Dict, Optional
from dms2223backend.data.db.results import ReporteCom
from dms2223backend.data.reportstatus import ReportStatus

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select # type: ignore


class ReporteComFuncs():

    @staticmethod
    def create(session:Session, username: str, reason: str, cid: int) -> ReporteCom: #Estaba mal, mirar desde el spec lo que necesitamos
        if not reason:
            raise ValueError('Campo razón vacío.')
        if not cid:
            raise ValueError('Id reporte comentario vacío.')
       
        nueva = ReporteCom(username, reason, cid, ReportStatus.PENDING) #En el orden del result

        session.add(nueva)
        session.commit()
        return nueva
        
    @staticmethod
    def get_reporteCom(session:Session, id:int) -> ReporteCom:
        stmt = session.query(ReporteCom).where(ReporteCom.id == id).first()
        return stmt

    @staticmethod
    def list_all(session: Session) -> List[ReporteCom]:
       
        stmt = session.query(ReporteCom).all()
        return stmt

    

    
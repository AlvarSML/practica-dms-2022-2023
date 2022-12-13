from typing import List, Dict, Optional
from datetime import datetime

from dms2223backend.data.db.Usuario import Usuario
from dms2223backend.data.db.Elemento import Pregunta, Respuesta, Comentario
from dms2223backend.data.db.Voto import Voto

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select # type: ignore

class PreguntaRes():
    """ Clase de alto nivel que va a contener los datos completos de una pregunta
        Incluye las operaciones de acceso a tablas
        No se si respetar la herencia, de momento no
    """
    titulo: str
    id_pregunta: int #Es el mismo que el de elemento
    fecha: datetime
    autor: Usuario
    contenido: str
    visibilidad: bool
    votos = List[Voto]
    respuestas = List[Respuesta]


class PreguntaFuncs():
    """ Calase apra acceder a los datos
    """
    @staticmethod
    def list_all(max:Optional[int], session: Session) -> List[Dict]:
        """ Se obtienen todos los registros de pregunta, con un limite si se especifica
        """

        listaPreguntas: List[PreguntaRes] = []
        stmt = select(Pregunta)

        if (max):
            stmt = stmt.limit(max)        

        for preg in session.execute(stmt):
            p = {
                "qid": preg[0].id_pregunta,
                "title": preg[0].titulo,
                "timestamp": preg[0].fecha,
                "autor" : preg[0].autor.nombre,
                "pos_votes": 0,
                "neg_votes": 0
            }
            listaPreguntas.append(p)

        # Esto tiene que devolver la lista bien formateada
        return listaPreguntas

    @staticmethod
    def create(session:Session,pregunta:Pregunta) -> Pregunta:
        """ Inserta una pregunta en la bdd
        """
        session.add(pregunta)
        session.commit()
        # ! Importante, se recuperoa la pregunta creada, con id fecha y demas datos
        session.refresh(pregunta)

        return pregunta

    @staticmethod
    def get(session:Session,qid:int) -> Pregunta:
        """ Obtiene una instancia de pregunta activa en la sesion
        """
        preg = session.query(Pregunta).filter(Pregunta.id_pregunta == qid).first()
        return preg
    
    
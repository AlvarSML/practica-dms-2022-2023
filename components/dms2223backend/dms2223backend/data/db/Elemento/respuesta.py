from sqlalchemy import Column,String,Text,Boolean,DateTime,ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dms2223backend.data.db.Usuario.usuario import Usuario
from dms2223backend.data.db.Elemento.elemento import Elemento
from dms2223backend.data.db.Elemento.pregunta import Pregunta
from sqlalchemy.orm import relationship


class Respuesta(Elemento):
    __tablename__='respuesta'

    id_respuesta = Column(Integer, ForeignKey("elemento.id_elemento") ,primary_key=True)
    id_pregunta = Column(Integer, ForeignKey("pregunta.id_pregunta"))

    pregunta = relationship("Pregunta", 
        back_populates="respuestas", 
        primaryjoin="Respuesta.id_pregunta == Pregunta.id_pregunta")

    comentarios = relationship(
        "Comentario", 
        primaryjoin="Respuesta.id_respuesta == Comentario.id_respuesta")

    reportes = relationship("ReporteRespuesta",
        primaryjoin="Respuesta.id_respuesta == ReporteRespuesta.id_respuesta"
        )

    __mapper_args__ = {
        "polymorphic_identity": "respuesta",
    }

    def __init__(self,
        contenido:str,
        autor:int,
        pregunta:Pregunta
        ):
        super().__init__(contenido=contenido,autor=autor)
        self.pregunta = pregunta
    
    def __repr__(self) -> str:        
        return  f"Pregunta(id_respuesta={self.id_respuesta!r}, \
        contenido={self.contenido!r}, \
        fecha={self.fecha!r}, \
        autor={self.autor!r},\
        visibilidad={str(self.visibilidad)!r} \
        )"
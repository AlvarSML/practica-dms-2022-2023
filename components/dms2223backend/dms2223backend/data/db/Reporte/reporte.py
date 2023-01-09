""" todas las clases derivadas de reporte
"""
import enum
from sqlalchemy import Column,String,Text,DateTime, \
    ForeignKey, Integer, Enum # type: ignore
from datetime import datetime
from dms2223backend.data.db.Usuario.usuario import Usuario
from dms2223backend.data.db.Elemento.pregunta import Pregunta
from dms2223backend.data.db.Elemento.respuesta import Respuesta
from dms2223backend.data.db.Elemento.comentario import Comentario
from ..base import Base #Base declarativa
from sqlalchemy.orm import relationship # type: ignore

class Estado_moderacion(enum.Enum):
    pending = 0
    accepted = 1
    rejected = 2
    discarded = 3

class Reporte(Base):
    __tablename__= 'reporte'

    id_reporte = Column(Integer, primary_key=True)
    id_autor = Column(Integer, ForeignKey("usuario.id_usuario"))
    moderador = Column(Integer , ForeignKey("usuario.id_usuario"))
    fecha = Column(DateTime, default=datetime.now())

    razon_reporte = Column(Text)
    resultado_moderacion = Column(String(100))
    estado = Column(Enum(Estado_moderacion), default=Estado_moderacion.pending, index=True)

    type = Column(String(50)) #Especifica el tipo de reporte que es

    __mapper_args__ = {
        "polymorphic_identity": "reporte",
        "polymorphic_on": type,
    }

    def __init__(self,
        autor:Usuario,
        razon_reporte:str
        ):
        self.autor = autor
        self.razon_reporte = razon_reporte

class ReportePregunta(Reporte):
    id_pregunta = Column(Integer, ForeignKey("pregunta.id_pregunta"))
    pregunta = relationship("Pregunta",
        back_populates="reportes")

    autor = relationship("Usuario",
        back_populates="reportesPregs",
        primaryjoin="Reporte.id_autor == Usuario.id_usuario")

    __mapper_args__ = {
        "polymorphic_identity": "reporte_pregunta",
    }

    def __init__(
        self,
        autor:Usuario,
        razon_reporte:str,
        pregunta: Pregunta
        ):
        super().__init__(
            autor=autor,
            razon_reporte=razon_reporte)
        self.pregunta = pregunta

class ReporteRespuesta(Reporte):
    id_respuesta = Column(Integer, ForeignKey("respuesta.id_respuesta"))
    respuesta = relationship("Respuesta",
        back_populates="reportes")
    autor = relationship("Usuario",
        back_populates="reportesResps",
        primaryjoin="Reporte.id_autor == Usuario.id_usuario")

    __mapper_args__ = {
        "polymorphic_identity": "reporte_respuesta",
    }

    def __init__(
        self,
        autor:Usuario,
        razon_reporte:str,
        respuesta: Respuesta
        ):
        super().__init__(
            autor=autor,
            razon_reporte=razon_reporte)
        self.respuesta = respuesta

class ReporteComentario(Reporte):
    id_comentario = Column(Integer, ForeignKey("comentario.id_comentario"))
    comentario = relationship("Comentario",
        back_populates="reportes")

    autor = relationship("Usuario",
        back_populates="reportesComs",
        primaryjoin="Reporte.id_autor == Usuario.id_usuario")
    
    __mapper_args__ = {
        "polymorphic_identity": "reporte_comentario",
    }

    def __init__(
        self,
        autor:Usuario,
        razon_reporte:str,
        comentario: Comentario
        ):
        super().__init__(
            autor=autor,
            razon_reporte=razon_reporte)
        self.comentario = comentario
    
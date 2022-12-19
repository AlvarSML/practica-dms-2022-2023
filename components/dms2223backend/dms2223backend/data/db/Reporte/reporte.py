import enum
from sqlalchemy import Column,String,Text,Boolean,DateTime, \
    ForeignKey, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dms2223backend.data.db.Usuario.usuario import Usuario
from dms2223backend.data.db.Elemento.elemento import Elemento
from dms2223backend.data.db.Elemento.pregunta import Pregunta
from dms2223backend.data.db.Elemento.respuesta import Respuesta
from dms2223backend.data.db.Elemento.comentario import Comentario
from ..base import Base #Base declarativa
from sqlalchemy.orm import relationship

class estado_moderacion(enum.Enum):
    pendiente = 0
    aceptado = 1
    rechazado = 2
    descartado = 3 # Ni se ha leido

class Reporte(Base):
    __tablename__= 'reporte'

    id_reporte = Column(Integer, primary_key=True)
    id_autor = Column(Integer, ForeignKey("usuario.id_usuario"))
    moderador = Column(Integer , ForeignKey("usuario.id_usuario"))
    fecha = Column(DateTime, default=datetime.now())

    razon_reporte = Column(Text)
    resultado_moderacion = Column(String(100))  
    estado = Column(Enum(estado_moderacion), default=estado_moderacion.pendiente)

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
    
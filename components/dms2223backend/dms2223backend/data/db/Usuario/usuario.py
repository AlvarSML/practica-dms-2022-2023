""" Calse usuario de la base de datos
"""
from sqlalchemy import String, Column, Integer
from ..base import Base #Base declarativa
from sqlalchemy.orm import relationship

class Usuario(Base):
    
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True)
    nombre = Column(String(50) ,nullable=False, unique=True, index=True)

    elementos = relationship('Elemento', back_populates="autor")

    preguntas = relationship(
        'Pregunta',
        primaryjoin="Usuario.id_usuario == Pregunta.id_autor",
        overlaps="elementos")
    respuestas = relationship(
        'Respuesta',
        primaryjoin="Usuario.id_usuario == Respuesta.id_autor",
        overlaps="elementos")
    comentarios = relationship(
        'Comentario',
        primaryjoin="Usuario.id_usuario == Comentario.id_autor",
        overlaps="elementos")

    reportesPregs = relationship(
        'ReportePregunta',
          primaryjoin="Usuario.id_usuario == ReportePregunta.id_autor")
    reportesResps = relationship(
        'ReporteRespuesta',
          primaryjoin="Usuario.id_usuario == ReporteRespuesta.id_autor")
    reportesComs = relationship(
        'ReporteComentario',
          primaryjoin="Usuario.id_usuario == ReporteComentario.id_autor")


    def __init__(self,nombre:str):
        self.nombre = nombre
""" Clase feedback de la base de datos
"""
from sqlalchemy import Column,String,Text, Integer
from ..base import Base #Base declarativa
from sqlalchemy.orm import relationship

class Feedback(Base):
    __tablename__='feedback'

    id_feedback = Column(Integer, primary_key=True)
    descripcion = Column(Text, unique=True, index=True)
    color_asociado = Column(String(100))

    comentarios = relationship(
        "Comentario", 
        primaryjoin="Feedback.id_feedback == Comentario.id_feedback")

    def __init__(self,
        descripcion:str,
        color_asociado:str,
    ):
        self.descripcion = descripcion
        self.color_asociado = color_asociado

    def __repr__(self) -> str:
        return f"Feedback(\
            id_feedback={self.id_feedback!r}\
            color_asociado={self.color_asociado!r}\
            descripcion={self.descripcion!r})"
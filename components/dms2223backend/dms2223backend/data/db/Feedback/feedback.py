from sqlalchemy import Column,String,Text,Boolean,DateTime,ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dms2223backend.data.db.Usuario.usuario import Usuario
from dms2223backend.data.db.Elemento.elemento import Elemento
from ..base import Base #Base declarativa

class Feedback(Base):
    __tablename__='feedback'

    id_feedback = Column(Integer, primary_key=True)
    descripcion = Column(Text, unique=True, index=True)
    color_asociado = Column(String(100))

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
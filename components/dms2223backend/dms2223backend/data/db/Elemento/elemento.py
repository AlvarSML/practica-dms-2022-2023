from sqlalchemy import Column,String,Text,Boolean,DateTime,ForeignKey,Integer
from sqlalchemy.ext.declarative import declarative_base
from dms2223backend.data.db.Usuario.usuario import Usuario
from ..base import Base #Base declarativa
from sqlalchemy.orm import relationship

from datetime import datetime

class Elemento(Base):
    __tablename__ = 'elemento'

    id_elemento = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.now())
    
    id_autor = Column(Integer, ForeignKey(Usuario.id_usuario))

    autor = relationship("Usuario",back_populates="elementos")
    votos = relationship(
        "Voto",
        back_populates="elemento",
        lazy='dynamic')

    contenido = Column(Text)
    visibilidad = Column(Boolean, default=True) #En caso de true es visible en caso de false esta oculto
    type = Column(String(50)) #Especifica el tipo de elemento que es

    __mapper_args__ = {
        "polymorphic_identity": "elemento",
        "polymorphic_on": type,
    }

    def __init__(self,
        contenido:str,
        autor:Usuario,
        ):
        self.contenido = contenido
        self.autor = autor
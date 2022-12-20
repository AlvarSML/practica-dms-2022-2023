import enum
from sqlalchemy import Column,String,Text,Boolean,DateTime, \
    ForeignKey,Integer,Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dms2223backend.data.db.Usuario.usuario import Usuario
from dms2223backend.data.db.Elemento.elemento import Elemento
from ..base import Base #Base declarativa

from sqlalchemy.orm import relationship

class Tipo_voto(enum.Enum):
    positivo = 1
    negativo = 0

class Voto(Base):
    __tablename__ = 'voto'

    id_voto = Column(Integer, primary_key=True)
    id_elemento = Column(Integer, ForeignKey("elemento.id_elemento"))
    id_autor = Column(Integer, ForeignKey("usuario.id_usuario"),index=True)

    tipo = Column(Enum(Tipo_voto))
    
    autor = relationship("Elemento")
    elemento = relationship("Elemento", back_populates="votos")

    def __init__(
        self,
        elemento:Elemento,
        autor:Usuario,
        tipo:Tipo_voto = Tipo_voto.positivo
        ):
        self.elemento = elemento
        self.autor=autor
        self.tipo = tipo

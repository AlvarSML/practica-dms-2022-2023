from sqlalchemy import Column,String,Text,Boolean,DateTime,ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dms2223backend.data.db.Usuario.usuario import Usuario
from dms2223backend.data.db.Elemento.elemento import Elemento
from dms2223backend.data.db.Elemento.elemento import Pregunta


class Respuesta(Elemento):
    __tablename__='respuesta'
    id_respuesta = Column(Integer, ForeignKey("elemento.id_elemento") ,primary_key=True)
    id_pregunta = Column(Integer, ForeignKey("pregunta.id_pregunta") ,primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "respuesta",
    }

    def __init__(self,
        contenido:str,
        fecha:datetime,
        autor:int,
        visibilidad:bool
        ):
        super().__init__(contenido=contenido,fecha=fecha,autor=autor,visibilidad=visibilidad)
    
    def __repr__(self) -> str:        
        return  f"Pregunta(id_respuesta={self.id_respuesta!r}, \
        contenido={self.contenido!r}, \
        fecha={self.fecha!r}, \
        autor={self.autor!r},\
        visibilidad={str(self.visibilidad)!r} \
        )"
from sqlalchemy import Column,String,Text,Boolean,DateTime,ForeignKey,Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dms2223backend.data.db.Usuario.usuario import Usuario
from dms2223backend.data.db.Elemento.elemento import Elemento
from sqlalchemy.orm import relationship

Base = declarative_base()

class Pregunta(Elemento):



    __tablename__='pregunta'
    id_pregunta = Column(Integer, ForeignKey("elemento.id_elemento") ,primary_key=True)
    titulo = Column(String(200))
    # TODO: meter resto de atributos -> ver spec.yml (schema question full model)


    respuestas = relationship("Respuesta", 
        primaryjoin="Pregunta.id_pregunta == Respuesta.id_pregunta"
        )

    reportes = relationship("ReportePregunta",
        primaryjoin="Pregunta.id_pregunta == ReportePregunta.id_pregunta"
        )

    __mapper_args__ = {
        "polymorphic_identity": "pregunta",
    }
    
    def __init__(self,
        titulo:str,
        contenido:str,
        autor:Usuario
        # TODO: meter resto de atributos -> ver spec.yml (schema question new model)
        ):
        super().__init__(contenido=contenido,autor=autor)
        self.titulo = titulo

    def __repr__(self) -> str:        
        return  f"Pregunta(id_pregunta={self.id_pregunta!r}, \
        titulo={self.titulo!r}, \
        contenido={self.contenido!r}, \
        fecha={self.fecha!r}, \
        autor={self.autor!r},\
        visibilidad={str(self.visibilidad)!r} \
        )"
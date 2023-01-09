""" Clase comentario de la bdd
"""

from sqlalchemy import Column, ForeignKey, Integer
from dms2223backend.data.db.Elemento.elemento import Elemento
from dms2223backend.data.db.Elemento.respuesta import Respuesta
from dms2223backend.data.db.Feedback.feedback import Feedback
from sqlalchemy.orm import relationship

class Comentario(Elemento):
    __tablename__='comentario'

    id_comentario= Column(Integer, ForeignKey("elemento.id_elemento") ,primary_key=True)
    id_respuesta = Column(Integer, ForeignKey("respuesta.id_respuesta"))
    id_feedback = Column(Integer, ForeignKey("feedback.id_feedback"))

    feedback = relationship(
        "Feedback",
        foreign_keys=[id_feedback],
        overlaps="comentarios")

    respuesta = relationship(
        "Respuesta", 
        back_populates="comentarios", 
        foreign_keys=[id_respuesta])

    reportes = relationship(
        "ReporteComentario",
        primaryjoin="Comentario.id_comentario == ReporteComentario.id_comentario"
        )

    __mapper_args__ = {
        "polymorphic_identity": "comentario",
    }

    def __init__(self,
        contenido:str,
        autor:int,
        feedback:Feedback,
        respuesta: Respuesta
        ):
        super().__init__(contenido=contenido,autor=autor)
        self.feedback = feedback
        self.respuesta = respuesta

    def __repr__(self) -> str:        
        return  f"Comentario(id_comentario={self.id_comentario!r}, \
        contenido={self.contenido!r}, \
        fecha={self.fecha!r}, \
        autor={self.autor!r},\
        visibilidad={str(self.visibilidad)!r} \
        feedback={self.feedback} \
        )"
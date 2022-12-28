from typing import List, Dict
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db import Schema
from .authservice import AuthService
from dms2223backend.data.sentiment import  Sentiment
from dms2223backend.data.db.results.comentario import Comentario
from dms2223backend.data.db.resultsets.comentario_res import ComentarioFuncs

class servicioComentario():

    def init(self):
        self.auth_service = AuthService(apikey_secret='1234',host="172.10.1.10",port=4000)

    def crear_comentario(schema:Schema, autor: str, body: str, aid: int, sentiment: Sentiment) -> Comentario:
        session: Session = schema.new_session()
        comentario = ComentarioFuncs.create(session, autor, body, aid, sentiment)
        #AQUI MAITE CREA UN DICCIONARIO Y CREO QUE NO ES NECESARIO
        schema.remove_session()
        return comentario

    def get_comentario(schema:Schema, id:int) -> Comentario:
        session: Session = schema.new_session()
        comentarioADevolver = ComentarioFuncs.get_comentario(session, id)
        schema.remove_session()
        return comentarioADevolver

    def get_comentarios(schema:Schema, aid:int) -> List[Comentario]:
        session: Session = schema.new_session()
        comentariosADevolver = ComentarioFuncs.list_all(session, aid)
        schema.remove_session()
        return comentariosADevolver
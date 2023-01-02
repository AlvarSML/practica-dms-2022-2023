from dms2223backend.data.db.resultsets.respuesta_res import RespuestaFuncs
from dms2223backend.data.db import Schema
from sqlalchemy.orm.session import Session  # type: ignore
from typing import List, Dict

class ServicioRespuestas():

    def getRespuestasAPregunta(schema: Schema, qid: int):
        """Devuelve un diccionario de las respuestas correspondientes a la pregunta
           pasada por parametro.

        Args: qid: pregunta de la que se quieren sus respuesta. 
              schema: elemento de consulta centralizado.

        Returns: Diccionario con las respuestas encontradas.
        """

        session: Session = schema.new_session()

        out: List[Dict] = RespuestaFuncs.list_all(session,qid)
        lista_respuestas: List = []

        for respuesta in out:
            lista_respuestas.append({
                "id":respuesta.id,
                "qid":respuesta.qid,
                "body":respuesta.body,
                "owner":{"username":respuesta.username},
            })
        schema.remove_session()
        return lista_respuestas
    
    def create_Respuesta(schema:Schema,username:str,body:Dict):
        """Crea una respuesta y devuelve el diccionario de la respuesta creada.

        Args: qid: Identificador de la pregunta que se va a responder.
                 username: Usuario que responde a la pregunta.
                 body: Cuerpo de la respuesta.
                 schema: elemento de consulta centralizado.
        Returns: Diccionario de la respuesta creada. 
        """
        session: Session = schema.new_session()

        res: Dict = RespuestaFuncs.create(session,username=username, body=body)

        respuesta: Dict = {
            "id":res.id,
            "qid":res.qid,
            "body":res.body,
            "owner":{"username":res.username},
            "oculto":res.oculto
        }

        schema.remove_session()

        return respuesta
    
    @staticmethod
    def ocultarRes(schema: Schema, id: int):
        """Oculta la respuesta
        """
        session: Session = schema.new_session()

        res = RespuestaFuncs.get_respuesta(session,id)
        res.hidden = True

        session.add(res)
        session.commit()

        schema.remove_session()
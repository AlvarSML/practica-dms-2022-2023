""" RespuestasServicio class module.
"""

from typing import List, Dict, ClassVar
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db import Schema



from dms2223backend.data.db.Elemento import Pregunta, Respuesta, Comentario
from dms2223backend.data.db import ReporteRespuesta


from dms2223backend.data.resultsets import RespuestaFuncs, FeedBackFuncs, \
    UsuarioFuncs, ReporteFuncs, ComentarioFuncs

from sqlalchemy import select

import sys

class RespuestasServicio():
    """ Clase "estatica" que permite el acceso a las operaciones de creacion o consulta
        derivados de respuesta
    """

    @staticmethod
    def set_comment(schema:Schema,comentario:Dict) -> Dict:
        """ Construye la instancia de comentario para insertar en la base de datos
            TODO: Comprobar que la respuesta existe
        """
        session: Session = schema.new_session()

        # Datos previos

        resp = RespuestaFuncs.get(
            session=session,
            aid=comentario["aid"])

        usuario = UsuarioFuncs.get_or_create(
            session=session,
            nombre=comentario["autor"])

        feedback = FeedBackFuncs.get(
            session=session,
            fname=comentario["feedback"])

        # Construccion de comentario

        comm:Comentario = Comentario(
            contenido=comentario["body"],
            autor=usuario,
            respuesta=resp,
            feedback=feedback
        ) 

        # Envio 

        res:Comentario = ComentarioFuncs.create(
            session=session,
            comment=comm
        )

        # Construccion de la respuesta

        comentario_dict:Dict = {
            "id":res.id_comentario,
            "aid":res.id_respuesta,
            "timestamp":res.fecha,
            "body":res.contenido,
            "owner":{"username":res.autor.nombre},
            "votes":3,
            "sentiment":res.feedback.descripcion
        }

        # Fianl

        schema.remove_session()
        return comentario_dict

    @staticmethod
    def set_report(schema:Schema,reporte:Dict) -> Dict:
        """ Construye un reporte para introducirlo en la bdd
            TODO: que exista al respuesta
        """
        session: Session = schema.new_session()

        # Obtencion de datos previos

        resp = RespuestaFuncs.get(
            session=session,
            aid=reporte["aid"])

        usuario = UsuarioFuncs.get_or_create(
            session=session,
            nombre=reporte["autor"])

        # Construccion de respuesta

        rep:ReporteRespuesta = ReporteRespuesta(
            respuesta=resp,
            razon_reporte=reporte["razon_reporte"],
            autor=usuario
        )

        # Se introduce el reporte en la bdd

        res:ReporteRespuesta = ReporteFuncs.create_rep(
            session=session,
            reporte=rep
        )

        reporte_dict:Dict = {
            "id":res.id_reporte,
            "aid":res.id_respuesta,
            "reason":res.razon_reporte,
            "status":res.estado.name,
            "owner":{"username":res.autor.nombre},
            "timestamp":res.fecha
        }

        schema.remove_session()
        return reporte_dict
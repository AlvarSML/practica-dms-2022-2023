""" RespuestasServicio class module.
"""

from typing import List, Dict, ClassVar
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db import Schema



from dms2223backend.data.db.Elemento import Pregunta, Respuesta, Comentario
from dms2223backend.data.db import ReporteRespuesta, Estado_moderacion


from dms2223backend.data.resultsets import RespuestaFuncs, FeedBackFuncs, \
    UsuarioFuncs, ReporteFuncs, ComentarioFuncs

from sqlalchemy import select

import sys

class RespuestasServicio():
    """ Clase "estatica" que permite el acceso a las operaciones de creacion o consulta
        derivados de respuesta
    """
    @staticmethod
    def build_dict_ans(ans:Respuesta) -> Dict:
        nans:Dict = {
            "id":ans.id_respuesta,
            "qid":ans.id_pregunta,
            "timestamp":ans.fecha,
            "body":ans.contenido,
            "owner":{"username":ans.autor.nombre},
            "votes":ans.votos.count()
        }

        return nans

    @staticmethod
    def build_report(raw:Dict) -> ReporteRespuesta:
        """ Crea un reporte desde un diccinario con las dependencias
        """
        rep:ReporteRespuesta = ReporteRespuesta(
            respuesta=raw["aid"],
            razon_reporte=raw["razon_reporte"],
            autor=raw["user"]
        )
        return rep
    
    @staticmethod
    def build_dict_report(reporte:ReporteRespuesta) -> Dict:
        """ Construye el diccionario de un reporte de respuesta
        """
        rep:Dict = {
            "id":reporte.id_reporte,
            "qid":reporte.id_respuesta,
            "reason":reporte.razon_reporte,
            "status":reporte.estado.name,
            "owner":{"username":reporte.autor.nombre},
            "timestamp":reporte.fecha
        }
        return rep

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
        
        if resp is None:
            return None

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

        # Obtencion de datos previos inyeccion, de depnendencias

        resp = RespuestaFuncs.get(
            session=session,
            aid=reporte["aid"])

        if resp is None:
            return None

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

    @staticmethod
    def get_reports(schema:Schema, estados:List[Estado_moderacion]) -> List[Dict]:
        """ Transforma los reportes en una lista
            ! Deprcado
        """
        session: Session = schema.new_session()
        reports:List = []

        res = ReporteFuncs.get_reps(
            session=session,
            tipo=ReporteRespuesta,
            estados=estados
            )

        for rep in res:
            reports.append(RespuestasServicio.build_dict_report(rep))
        
        session.flush()
        schema.remove_session()  
        return reports

    @staticmethod
    def set_estado(schema:Schema, reporte:Dict) -> Dict:
        """ Cambia el estado de un reporte a una respuesta
            ! Deprcado
        """
        session: Session = schema.new_session()

        # Se obtiene el reporte a modificar
        reporte_nuevo:ReporteRespuesta = ReporteFuncs.get_rep(
            session=session,
            tipo=ReporteRespuesta,
            rid=reporte["arid"]
        )

        # Se modifica el estado
        reporte_nuevo = ReporteFuncs.set_state(
            session=session,
            reporte=reporte_nuevo,
            estado=reporte["estado"]
        )

        # Se convierte el objeto a diccionario
        reporte_resp:Dict = RespuestasServicio.build_dict_report(reporte_nuevo)

        session.flush()
        schema.remove_session()  
        return reporte_resp

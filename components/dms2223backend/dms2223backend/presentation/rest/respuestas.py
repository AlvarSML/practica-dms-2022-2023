"""REST API controllers responsible of handling the server operations about answers
"""
from typing import Dict, Tuple, Optional, List
from http import HTTPStatus
from flask import current_app

from dms2223backend.service import RespuestasServicio, VotosServicio, ReportesServicio
from dms2223backend.data.db import Pregunta, Respuesta, Estado_moderacion,\
     ReporteRespuesta, Voto, Elemento

from flask import current_app

from dms2223backend.service import AuthService

import logging

def set_respuesta_comentario(aid:int, body: Dict, token_info: Dict) -> Tuple[Dict,Optional[int]]:
    """ Crea un comentario en una respuesta
    """
    with current_app.app_context():
        try:
            comm:Dict = {
                "body": body["body"],
                "feedback": body["sentiment"],
                "aid": aid,
                "autor":token_info["user_token"]["username"]
            }

            comment = RespuestasServicio.set_comment(
                schema=current_app.db,
                comentario=comm
            )
        except:
            logging.exception(f"No se ha podido obtener la respuesta {aid} por motivos desconocidos")
            return ({},HTTPStatus.INTERNAL_SERVER_ERROR)
        finally:
            if comment is None:
                reporte = f"The answer with aid {aid} does not exist."
                return (reporte, HTTPStatus.NOT_FOUND)
            else:
                return (comment, HTTPStatus.CREATED)

def set_respuesta_reporte(aid:int,body: Dict, token_info: Dict):
    """ Crea un reporte para una respuesta
    """
    with current_app.app_context():
        try:
            rep:Dict = {
                "razon_reporte":body["reason"],
                "aid":aid,
                "autor":token_info["user_token"]["username"]
            }

            rep = RespuestasServicio.set_report(
                schema=current_app.db,
                reporte=rep
            )
        except:
            logging.exception(f"No se ha podido obtener la respuesta {aid} por motivos desconocidos")
            return ({},HTTPStatus.INTERNAL_SERVER_ERROR)
        finally:
            if rep is None:
                reporte = f"The answer with aid {aid} does not exist."
                return (reporte, HTTPStatus.NOT_FOUND)
            return (rep, HTTPStatus.CREATED)

def get_reportes(**kwargs:Dict) -> Tuple[List[Dict], HTTPStatus]:
    """ Obtiene todos los reportes a todas las respuestas  
    """ 
    with current_app.app_context():
        status:List = []

        # Permite modificaciones de los estados de moderacion
        for estado in Estado_moderacion:
            if estado.name in kwargs and kwargs[estado.name]:
                status.append(estado.name)

        try:
            reportes:List[ReporteRespuesta] = ReportesServicio.get_reports(
                schema=current_app.db,
                rep_type=ReporteRespuesta,
                estados=status
            )
        except:
            logging.exception(f"No se han podido apbtener los reportes a respuestas\
                 por motivos desconocidos")
            return ({},HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            return (reportes, HTTPStatus.OK)
    

def cambia_estado_reporte(arid: int, body: Dict, token_info: Dict) -> Tuple[Dict, HTTPStatus]:
    """ Modifica el estado de un reporte
    """
    with current_app.app_context():
        try:
            reporte:Dict = ReportesServicio.set_estado(
                schema=current_app.db,
                reporte={
                    "rid":arid,
                    "autor":token_info["user_token"]["username"],
                    "estado":body["status"].lower()
                },
                tipo=ReporteRespuesta
            )
        except:
            logging.exception(f"No se han podido obtener el ReporteRespuesta {arid}")
            return ({},HTTPStatus.INTERNAL_SERVER_ERROR)
        else: 
            if reporte is None:
                reporte = f"The answer report with {arid} does not exist."
                return (reporte, HTTPStatus.NOT_FOUND)
            else:     
                return (reporte, HTTPStatus.NO_CONTENT)

def vota_respuesta(aid:int, token_info: Dict) -> Tuple[Dict, HTTPStatus]:
    """ Devuelve una lista de los votos a una respuesta
        TODO: todos los votos son positivos de momento
    """
    with current_app.app_context():
        try:
            votos:List = VotosServicio.set_voto(
                schema=current_app.db,
                id=aid,
                user=token_info["user_token"]["username"]
            )
        except:
            logging.exception(f"No se han podido votar la respuesta {aid}")
            return ({},HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            if votos is None:
                reporte = f"The answer with aid {aid} does not exist."
                return (reporte, HTTPStatus.NOT_FOUND)         
            return (votos, HTTPStatus.CREATED)

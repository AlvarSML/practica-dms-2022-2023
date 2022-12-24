"""REST API controllers responsible of handling the server operations about answers
"""
import sys
import json
import time
from typing import Dict, Tuple, Optional, List
from http import HTTPStatus
from flask import current_app

from sqlalchemy.orm.session import Session # type: ignore

from dms2223backend.data.resultsets import PreguntaFuncs, ReporteFuncs

from dms2223backend.service import RespuestasServicio, VotosServicio
from dms2223backend.data.db import Pregunta, Respuesta, Estado_moderacion,\
     ReporteRespuesta, Voto, Elemento

from flask import current_app

from dms2223backend.service import AuthService

import requests

def set_respuesta_comentario(aid:int, body: Dict, token_info: Dict) -> Tuple[Dict,Optional[int]]:
    """ Crea un comentario en una respuesta
    """
    with current_app.app_context():
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
    return (comment, HTTPStatus.CREATED)

def set_respuesta_reporte(aid:int,body: Dict, token_info: Dict):
    """ Crea un reporte para una respuesta
    """
    with current_app.app_context():
        rep:Dict = {
            "razon_reporte":body["reason"],
            "aid":aid,
            "autor":token_info["user_token"]["username"]
        }

        report = RespuestasServicio.set_report(
            schema=current_app.db,
            reporte=rep
        )
    return (report, HTTPStatus.CREATED)

def get_reportes(**kwargs:Dict) -> Tuple[List[Dict], HTTPStatus]:
    """ Obtiene todos los reportes a todas las respuestas  
    """ 
    with current_app.app_context():
        status:List = []

        # Permite modificaciones de los estados de moderacion
        for estado in Estado_moderacion:
            if estado.name in kwargs and kwargs[estado.name]:
                status.append(estado.name)

        reportes:List[ReporteRespuesta] = RespuestasServicio.get_reports(
            schema=current_app.db,
            estados=status
        )

    return (reportes, HTTPStatus.OK)

def cambia_estado_reporte(arid: int, body: Dict, token_info: Dict) -> Tuple[Dict, HTTPStatus]:
    """ Modifica el estado de un reporte
    """
    with current_app.app_context():
        reporte:Dict = RespuestasServicio.set_estado(
            schema=current_app.db,
            reporte={
                "arid":arid,
                "autor":token_info["user_token"]["username"],
                "estado":body["status"].lower()
            }
        )
    return (reporte, HTTPStatus.OK)

def vota_respuesta(aid:int, token_info: Dict) -> Tuple[Dict, HTTPStatus]:
    """ Devuelve una lista de los votos a una respuesta
        TODO: todos los votos son positivos de momento
    """
    with current_app.app_context():
        votos:List = VotosServicio.set_voto(
            schema=current_app.db,
            id=aid,
            user=token_info["user_token"]["username"]
        )
    return (votos, HTTPStatus.CREATED)

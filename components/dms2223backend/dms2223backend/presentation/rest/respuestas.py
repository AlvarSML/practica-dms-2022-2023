"""REST API controllers responsible of handling the server operations about answers
"""

import json
import time
from typing import Dict, Tuple, Optional, List
from http import HTTPStatus
from flask import current_app

from sqlalchemy.orm.session import Session # type: ignore

from dms2223backend.data.resultsets.pregunta_res import PreguntaRes, PreguntaFuncs
from dms2223backend.service import RespuestaServicio
from dms2223backend.data.db import Pregunta, Respuesta

from flask import current_app

from dms2223backend.service import AuthService

import requests

def vota_respuesta():
    """ Devuelve una lista de los votos a una respuesta
        TODO
    """
    pass

def set_respuesta_comentario(aid:int, body: Dict, token_info: Dict) -> Tuple[Dict,Optional[int]]:
    """ Crea un comentario en una respuesta
    """
    with current_app.app_context():
        comm:Dict = {
            "contenido": body["body"],
            "feedback": body["sentiment"],
            "aid": aid,
            "autor":token_info["user_token"]["username"]
        }
    pass

def set_respuesta_reporte(aid:int,body: Dict, token_info: Dict):
    """ Crea un reporte para una respuesta
        TODO
    """
    with current_app.app_context():
        rep:Dict = {
            "razon_reporte":body["reason"],
            "aid":aid,
            "autor":token_info["user_token"]["username"]
        }

        report = RespuestaServicio.set_report(
            schema=current_app.db,
            reporte=rep
        )
    pass

def get_reportes():
    """ Obtiene todos los reportes a todas las respuestas
        TODO
    """
    pass

def cambia_estado_reporte():
    """ Modifica el estado de un reporte
        TODO
    """
    pass

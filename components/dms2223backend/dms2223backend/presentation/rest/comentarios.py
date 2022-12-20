"""REST API controllers responsible of handling the server operations about comments
"""

import json
import time
from typing import Dict, Tuple, Optional, List
from http import HTTPStatus
from flask import current_app

from sqlalchemy.orm.session import Session # type: ignore

from dms2223backend.data.resultsets.pregunta_res import PreguntaRes, PreguntaFuncs
from dms2223backend.service.serviciopreguntas import PreguntasServicio
from dms2223backend.data.db import Pregunta, Respuesta

from flask import current_app

from dms2223backend.service import AuthService

import requests

def vota_comentario():
    """ Establece el voto en un comentario
    """
    pass

def reporta_comentario():
    """ Reporta un comentario
    """
    pass

def get_reportes(aid:int, body:Dict, token_info:Dict):
    """ Obtiene todos los reportes de todos los comentarios
    """
    return 0

def cambia_estado_reporte():
    """ Modifica el estado de un reporte a un comentario
    """
    pass
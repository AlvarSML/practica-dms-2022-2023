""" REST API controllers responsible of handling the server operations in the landing page
    They are special because they are accesible without auth, buecause they only provide
    Basic information
"""

import json
import time
from typing import Dict, Tuple, Optional, List
from http import HTTPStatus
from flask import current_app

from sqlalchemy.orm.session import Session # type: ignore

from dms2223backend.data.resultsets.pregunta_res import PreguntaRes, PreguntaFuncs
from dms2223backend.service.serviciopreguntas import PreguntasServicio
from dms2223backend.data.db import Pregunta

from flask import current_app

from dms2223backend.service import AuthService

import requests

def test_inicio() -> Tuple[str,Optional[int]]:
    with current_app.app_context():
        p = PreguntasServicio.get_pregunta(current_app.db,1)
    return ('Hola', HTTPStatus.OK)

def preguntas_usuario(idusu:int) -> Tuple[List[Pregunta],Optional[int]]:
    with current_app.app_context():
        preguntas = PreguntasServicio.get_preguntas_filtro(current_app.db,campo=Pregunta.autor,valor=idusu)
    return ('Hola', HTTPStatus.OK)


def list_preguntas() -> Tuple[List[Dict],Optional[int]]:
    """ No funciona
    """
    with current_app.app_context():
        list_quest:List = PreguntasServicio.get_preguntas(schema=current_app.db)
    return (list_quest,HTTPStatus.OK)
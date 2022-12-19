"""REST API controllers responsible of handling the server operations about questions
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

def create_preg(body: Dict, token_info: Dict) -> Tuple[str,Optional[int]]:
    """ Recoge los datos de la peticion y los manda al servicio de preguntas
    """
    with current_app.app_context():
        preg:Dict = {
            "titulo":body["title"],
            "contenido":body["body"],
            "autor":token_info["user_token"]["username"]
        }

        res:Pregunta = PreguntasServicio.create_pregunta(
            schema=current_app.db,datos=preg)
    return (res, HTTPStatus.OK)

def get_preg_id(qid:int) -> Tuple[Dict,Optional[int]]:
    """ Devuelve una pregunta sabiendo la id
    """
    with current_app.app_context():
        resp:Dict = PreguntasServicio.get_pregunta(
            schema=current_app.db,qid=qid)
    return (resp, HTTPStatus.OK)

def get_preg_answers(qid:int) -> Tuple[List[Dict],Optional[int]]:
    """ Devuelve una lista de respuestas a una pregunta
    """
    with current_app.app_context():
        resp:Dict = PreguntasServicio.get_answers(
            schema=current_app.db,qid=qid)
    return (resp, HTTPStatus.OK)

def set_preg_answer(qid:int,body: Dict, token_info: Dict) -> Tuple[Dict,Optional[int]]:
    """ Crea una respuesta a unn comentario
    """
    with current_app.app_context():
        ans:Dict = {
            "contenido":body["body"],
            "qid":body["qid"],
            "autor":token_info["user_token"]["username"]
        }

        asnw_reated:Dict = PreguntasServicio.create_respuesta(
            schema=current_app.db,
            respuesta=ans
        )
    return (asnw_reated, HTTPStatus.OK)

def set_preg_report(qid:int,body: Dict, token_info: Dict) -> Tuple[Dict,Optional[int]]:
    """ Crea un reporte para una pregunta
    """
    with current_app.app_context():
        rep:Dict = {
            "razon_reporte":body["reason"],
            "qid":qid,
            "autor":token_info["user_token"]["username"]
        }

        report = PreguntasServicio.set_report(
            schema=current_app.db,
            reporte=rep
        )
    return (report, HTTPStatus.OK)

def get_all_reports() -> Tuple[List[Dict],Optional[int]]:
    """ Devuelve todos los reportes que se han hecho a las preguntas
    """
    with current_app.app_context():
        resp:Dict = PreguntasServicio.get_all_reports(
            schema=current_app.db
        )
    return (resp, HTTPStatus.OK)

def put_preg_report(qid:int) -> Tuple[List[Dict],Optional[int]]:
    """ !TODO : generalizar    
        Modifica el estado de un reporte a una pregunta
    """
    with current_app.app_context():
        resp:Dict = PreguntasServicio.get_reporte_pregunta(qid)
    return (resp, HTTPStatus.OK)
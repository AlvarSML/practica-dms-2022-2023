"""REST API controllers responsible of handling the server operations about comments
"""

import json
import time
from typing import Dict, Tuple, Optional, List
from http import HTTPStatus
from flask import current_app

from sqlalchemy.orm.session import Session # type: ignore

from dms2223backend.service import VotosServicio, ReportesServicio
from dms2223backend.data.db import ReporteComentario, Estado_moderacion

from flask import current_app

from dms2223backend.service import AuthService

import requests

def vota_comentario(cid:int,token_info: Dict):
    """ Establece el voto en un comentario
    """
    with current_app.app_context():
        votos:List = VotosServicio.set_voto(
            schema=current_app.db,
            id=cid,
            user=token_info["user_token"]["username"]
        )
    return (votos, HTTPStatus.CREATED)

def reporta_comentario(cid:int, body:Dict, token_info:Dict):
    """ Reporta un comentario
    """
    with current_app.app_context():
        report:Dict = ReportesServicio.set_report_answer(
            schema=current_app.db,
            reporte={
                "cid":cid,
                "razon_reporte":body["reason"],
                "autor":token_info["user_token"]["username"]
            }
        )
    return (report, HTTPStatus.OK)

def get_reportes(**kwargs:Dict) -> Tuple[List[Dict], HTTPStatus]:
    """ Obtiene todos los reportes de todos los comentarios
    """
    with current_app.app_context():
        status:List = []

        # Permite modificaciones de los estados de moderacion
        for estado in Estado_moderacion:
            if estado.name in kwargs and kwargs[estado.name]:
                status.append(estado.name)

        reportes:List[ReporteComentario] = ReportesServicio.get_comm_reports(
            schema=current_app.db,
            estados=status
        )

    return (reportes, HTTPStatus.OK)

def cambia_estado_reporte():
    """ Modifica el estado de un reporte a un comentario
    """
    pass
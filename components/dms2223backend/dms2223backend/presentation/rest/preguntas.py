"""REST API controllers responsible of handling the server operations about questions
"""

import json
import time
from typing import Dict, Tuple, Optional, List
from http import HTTPStatus
from flask import current_app

from sqlalchemy.orm.session import Session # type: ignore

from dms2223backend.service import PreguntasServicio, ReportesServicio
from dms2223backend.data.db import Pregunta, ReportePregunta

from flask import current_app

import sys
import logging

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
        try:
            resp:Dict = PreguntasServicio.get_pregunta(
                schema=current_app.db,
                id=qid
                )
        except:
            logging.exception("No se ha podido obtener la pregunta")
            resp = {}
        finally:
            if resp is None:
                reporte = f"The question with qid {qid} does not exist."
                return (reporte,HTTPStatus.NOT_FOUND)
            else:
                return (resp, HTTPStatus.OK)    

def get_preg_answers(qid:int) -> Tuple[List[Dict],Optional[int]]:
    """ Devuelve una lista de respuestas a una pregunta
    """
    with current_app.app_context():
        try:
            resp:Dict = PreguntasServicio.get_answers(
                schema=current_app.db,qid=qid)
        except:
            logging.exception(f"No se ha podido obtener la pregunta {qid}")
            return ({},HTTPStatus.INTERNAL_SERVER_ERROR)
        finally:
            if resp is None:
                reporte = f"The question with qid {qid} does not exist."
                return (reporte, HTTPStatus.NOT_FOUND)
            else:
                return (resp, HTTPStatus.OK)

def set_preg_answer(qid:int,body: Dict, token_info: Dict) -> Tuple[Dict,Optional[int]]:
    """ Crea una respuesta a unn comentario
    """
    with current_app.app_context():
        try:
            ans:Dict = {
                "contenido":body["body"],
                "qid":qid,
                "autor":token_info["user_token"]["username"]
            }

            asnw_reated:Dict = PreguntasServicio.create_respuesta(
                schema=current_app.db,
                respuesta=ans
            )
        except:
            logging.exception(f"No se ha podido obtener la pregunta {qid}")
            return ({},HTTPStatus.INTERNAL_SERVER_ERROR)
        finally:
            if asnw_reated is None:
                reporte = f"The question with qid {qid} does not exist."
                return (reporte, HTTPStatus.NOT_FOUND)
            else:                
                return (asnw_reated, HTTPStatus.CREATED)

def set_preg_report(qid:int,body: Dict, token_info: Dict) -> Tuple[Dict,Optional[int]]:
    """ Crea un reporte para una pregunta
    """
    with current_app.app_context():
        try:
            rep:Dict = {
                "razon_reporte":body["reason"],
                "qid":qid,
                "autor":token_info["user_token"]["username"]
            }

            report:Dict = ReportesServicio.set_report_question(
                schema=current_app.db,
                reporte=rep
            )
        except:
            logging.exception(f"No se ha podido obtener la pregunta {qid}")
        finally:
            if report is None:
                reporte = f"The question with qid {qid} does not exist."
                return (reporte, HTTPStatus.NOT_FOUND)
            else:                
                return (report, HTTPStatus.CREATED)
    return (report, HTTPStatus.CREATED)

def get_all_reports() -> Tuple[List[Dict],Optional[int]]:
    """ Devuelve todos los reportes que se han hecho a las preguntas
    """
    with current_app.app_context():
        resp:Dict = PreguntasServicio.get_all_reports(
            schema=current_app.db
        )
    return (resp, HTTPStatus.OK)

def put_preg_report(qrid:int, body: Dict, token_info: Dict) -> Tuple[Dict,Optional[int]]:
    """    
        Modifica el estado de un reporte a una pregunta
    """
    with current_app.app_context():
        status:HTTPStatus = HTTPStatus.NO_CONTENT #204

        try:
            reporte:Dict = ReportesServicio.set_estado(
                schema=current_app.db,
                reporte={
                    "rid":qrid,
                    "autor":token_info["user_token"]["username"],
                    "estado":body["status"].lower()
                },
                tipo=ReportePregunta
            )

        except Exception as e:
            print("ERROR general de cambio de estatus",file=sys.stderr)
            logging.exception(e)
            status = HTTPStatus.INTERNAL_SERVER_ERROR
            reporte = {}
        finally:
            if reporte is None:
                status = HTTPStatus.NOT_FOUND #404
                reporte = f"The question report with qrid {qrid} does not exist."            
            
            return (reporte, status)

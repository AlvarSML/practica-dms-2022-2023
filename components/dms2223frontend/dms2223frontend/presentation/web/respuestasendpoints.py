""" RespuestasEndpoints class module.
"""

from dms2223frontend.data.clases.respuesta import Respuesta
from dms2223frontend.data.clases.comentario import Comentario
from typing import Text, Union
from flask import redirect, url_for, session, render_template
from werkzeug.wrappers import Response
from dms2223common.data import Role
from dms2223frontend.data.rest.authservice import AuthService
from .webauth import WebAuth
from datetime import datetime


class RespuestasEndpoints():
    @staticmethod
    def get_respuesta(auth_service: AuthService, id_respuesta: int) -> Union[Response, Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        resp = Respuesta(
            "1",
            "20",
            "Hoy es dia 10",
            datetime.now(),
            34,
            35,
            "Yo",
            15
        )

        comentarios = [
            Comentario("1","2","3","Me ha parecido bien",datetime.now(),13,2,"Usuario123","Positivo","verde"),
            Comentario("1","2","3","Me ha parecido mal",datetime.now(),13,2,"Usuario321","Negativo","rojo")
        ]
        return render_template('respuesta.html', respuesta_env=resp, comentarios_env=comentarios)
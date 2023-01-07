""" PreguntasEndpoints class module.
"""    

from dms2223frontend.data.clases.pregunta import Pregunta
from dms2223frontend.data.clases.respuesta import Respuesta
from dms2223frontend.data.rest.authservice import AuthService

from typing import Text, Union
from flask import redirect, url_for, session, render_template,current_app
from werkzeug.wrappers import Response
from dms2223common.data import Role
from .webauth import WebAuth
from datetime import datetime

from dms2223frontend.data.rest import BackendService

class PreguntasEndpoints():
    @staticmethod
    def get_pregunta(auth_service: AuthService, back_service:BackendService, id_preg: str) -> Union[Response, Text]:

        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.ADMINISTRATION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']

        preg = back_service.get_question(
            token = session.get('token'),
            qid=id_preg
        )

        resps = back_service.get_answers(
            token = session.get('token'),
            qid=id_preg
        )

        current_app.logger.info(preg.get_content())
        current_app.logger.info(resps.get_content())

        return render_template(
            'pregunta.html',
            name = name,
            pregunta_env = preg.get_content(), 
            respuestas_env = resps.get_content())
     
    """ Monostate class responsible of handling the session web endpoint requests.
    """
    @staticmethod
    def get_crear_preguntas(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the home endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.ADMINISTRATION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('preguntas/crear_preguntas.html', name=name, roles=session['roles'])


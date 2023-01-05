""" CommonEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, current_app
from werkzeug.wrappers import Response
from dms2223frontend.data.rest import AuthService, BackendService
from .webauth import WebAuth

from dms2223frontend.data.clases.pregunta import Pregunta
from datetime import datetime

class CommonEndpoints():
    """ Monostate class responsible of handling the common web endpoint requests.
    """
    @staticmethod
    def get_home(auth_service: AuthService, back_service:BackendService) -> Union[Response, Text]:
        """ Handles the GET requests to the home endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        # Editado por alvar el 4/11/2022 apra evitar la redireccion, linea 26, 27
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))

        name = session['user']

        #Lista de preguntas hardcodeada
        #Cambiar por una peticion que solicite la lista
        pregs=back_service.get_questions()

        return render_template('home.html', 
            name=name, 
            roles=session['roles'],
            preguntas=pregs)

    @staticmethod
    def get_inicio(back_service:BackendService):
        """ Genstiona el acceso a inicio sin ningun tipo de login necesario
        
        """

        pregs=back_service.get_questions(token=session.get('token'))
        current_app.logger.info(pregs.get_content())

        return render_template('inicio/inicio.html',
            preguntas=pregs.get_content())
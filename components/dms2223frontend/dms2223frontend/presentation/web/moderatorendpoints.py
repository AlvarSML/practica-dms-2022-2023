""" ModeratorEndpoints class module.
"""
    
from typing import Text, Union
from flask import redirect, url_for, session, render_template, current_app
from werkzeug.wrappers import Response
from dms2223common.data import Role
from dms2223frontend.data.rest.authservice import AuthService
from dms2223frontend.data.rest.backendservice import BackendService
from .webauth import WebAuth


class ModeratorEndpoints():
    """ Monostate class responsible of handing the moderator web endpoint requests.
    """
    @staticmethod
    def get_moderator(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the moderator root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('moderator.html', name=name, roles=session['roles'])

    def get_reportes(auth_service: AuthService, back_service:BackendService):
        """ Obtener todos los repores de preguntas
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']

        reps_preg = back_service.get_reps_preguntas(
            token=session.get('token')
        )

        reps_resp = back_service.get_reps_respuestas(
            token=session.get('token')
        )

        reps_comm = back_service.get_reps_comentarios(
            token=session.get('token')
        )


        return render_template(
            'reportes_preguntas.html',
            name = name,
            reportes_preguntas = reps_preg.get_content(),
            reportes_respuestas = reps_resp.get_content(),
            reportes_comentarios = reps_comm.get_content(),
            )

""" PreguntasEndpoints class module.
"""    

from dms2223frontend.data.clases.pregunta import Pregunta
from dms2223frontend.data.clases.respuesta import Respuesta
from dms2223frontend.data.rest.authservice import AuthService

from typing import Text, Union
from flask import (redirect, url_for, session, 
    render_template,current_app, request)
from werkzeug.wrappers import Response
from dms2223common.data import Role
from .webauth import WebAuth
from datetime import datetime

from dms2223frontend.data.rest import BackendService
from dms2223common.data.rest import ResponseData

class PreguntasEndpoints():
    @staticmethod
    def get_pregunta(auth_service: AuthService, back_service:BackendService, id_preg: str) -> Union[Response, Text]:

        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
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
    def get_crear_pregunta(auth_service: AuthService,  back_service:BackendService) -> Union[Response, Text]:
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

    @staticmethod
    def post_quest(back_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        title = request.form.get('qtitle')
        body = request.form.get('qbody')

        quest = back_service.post_question(
            token = session.get('token'),
            title=title, 
            body=body)

        current_app.logger.debug(quest.get_messages())
        current_app.logger.debug(quest.get_content())

        if not quest:
            return redirect(url_for('get_quest'))

        return redirect(url_for('get_home'))

    @staticmethod
    def get_crear_respuesta(back_service: BackendService, auth_service: AuthService, qid:int):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']

        preg: ResponseData = back_service.get_question(
            token = session.get('token'),
            qid=qid
        )


        current_app.logger.info(preg.get_content())


        return render_template(
            'preguntas/responder_pregunta.html',
            name = name,
            pregunta_env = preg.get_content())

    @staticmethod
    def post_new_answer(back_service: BackendService, auth_service: AuthService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        qid = request.form.get('qid')
        body = request.form.get('abody')

        ans: ResponseData = back_service.post_answer(
            token = session.get('token'),
            qid=qid, 
            body=body)
        
        if not ans:
            return redirect(url_for('get_quest'))

        return redirect(url_for('get_home'))

    @staticmethod
    def get_crear_comentario(
        back_service: BackendService, 
        auth_service: AuthService, 
        aid:int):

        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']


        return render_template(
            'preguntas/comentar_respuesta.html',
            name = name,
            respuesta_anterior=aid,
            sentiments = {
                "positive":"POSITIVE",
                "negative":"NEGATIVE",
                "neutral":"NEUTRAL"})

    @staticmethod
    def post_new_comment(
        back_service: BackendService,
        auth_service: AuthService,
        aid: str):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        body = request.form.get('cbody')
        sentiment = request.form.get('sentiment')

        comm: ResponseData = back_service.post_comment(
            token = session.get('token'),
            aid=aid, 
            body=body,
            sentiment=sentiment)
        
        current_app.logger.debug(comm.is_successful())
        current_app.logger.debug(comm.get_messages())


        if not comm.is_successful():
            return redirect(url_for('crear_comentario_get',id_resp=aid))

        return redirect(url_for('get_home'))
    
    def vota_elemento(
        auth_service: AuthService, 
        back_service:BackendService, 
        eid:int,
        pid:int,
        tipo:str):

        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        response: ResponseData = back_service.post_voto(
            token=session.get('token'),
            tipo=tipo,
            eid=eid)

        return PreguntasEndpoints.get_pregunta(
            auth_service=auth_service,
            back_service=back_service,
            id_preg=pid
        )
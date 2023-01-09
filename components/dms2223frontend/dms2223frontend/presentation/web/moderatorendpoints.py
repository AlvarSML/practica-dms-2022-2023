""" ModeratorEndpoints class module.
"""
    
from typing import Text, Union
from flask import redirect, url_for, session, render_template, current_app, request
from werkzeug.wrappers import Response
from dms2223common.data import Role
from dms2223frontend.data.rest.authservice import AuthService
from dms2223frontend.data.rest.backendservice import BackendService
from .webauth import WebAuth
from dms2223common.data.rest import ResponseData
from dms2223frontend.presentation.web.commonendpoints import CommonEndpoints

class ModeratorEndpoints():
    """ Monostate class responsible of handing the moderator web endpoint requests.
    """
    @staticmethod
    def get_moderator(auth_service: AuthService, back_service:BackendService):
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

        current_app.logger.debug(reps_preg.get_messages())

        return render_template(
            'moderator.html',
            name = name,
            reportes_preguntas = reps_preg.get_content(),
            reportes_respuestas = reps_resp.get_content(),
            reportes_comentarios = reps_comm.get_content(),
            statuses={
                "accepted":"ACCEPTED",
                "pending":"PENDING",                
                "rejected":"REJECTED"
            }
        )

    @staticmethod
    def put_estado_preg(auth_service: AuthService, back_service:BackendService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))

        rid = request.form.get('id')
        status = request.form.get('status')

        response: ResponseData = back_service.put_question_report(
            token=session.get('token'),
            qrid=rid, 
            status=status)
        
        current_app.logger.debug("cabio estado rpreg")
        current_app.logger.debug(response.get_messages())

        return ModeratorEndpoints.get_moderator(
            auth_service=auth_service,
            back_service=back_service
        )
    

    @staticmethod
    def put_estado_resp(auth_service: AuthService, back_service:BackendService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))

        rid = request.form.get('id')
        status = request.form.get('status')

        response: ResponseData = back_service.put_answer_report(
            token=session.get('token'),
            arid=rid, 
            status=status)

        current_app.logger.debug("cabio estado rresp")
        current_app.logger.debug(response.get_messages())

        return ModeratorEndpoints.get_moderator(
            auth_service=auth_service,
            back_service=back_service
        )

    @staticmethod
    def put_estado_comm(auth_service: AuthService, back_service:BackendService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))

        rid = request.form.get('id')
        status = request.form.get('status')

        response: ResponseData = back_service.put_comment_report(
            token=session.get('token'),
            crid=rid, 
            status=status)
        
        current_app.logger.debug("cabio estado rcomm")
        current_app.logger.debug(response.get_messages())

        return ModeratorEndpoints.get_moderator(
            auth_service=auth_service,
            back_service=back_service
        )

    @staticmethod
    def post_report(auth_service: AuthService, back_service:BackendService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        name = session['user']
        eid = request.form.get('eid')
        razon = request.form.get('razon')
        tipo = request.form.get('tipo')

        response: ResponseData = back_service.post_report(
            token=session.get('token'),
            reason=razon, 
            tipo=tipo,
            eid=eid)

        current_app.logger.debug("nuevo reporte")
        current_app.logger.debug(response.get_messages())

        return CommonEndpoints.get_home(
            auth_service=auth_service,
            back_service=back_service
        )




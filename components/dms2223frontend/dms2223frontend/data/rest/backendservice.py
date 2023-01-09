""" BackendService class module.
"""
from typing import Optional, Dict
import requests
from dms2223common.data import Role
from dms2223common.data.rest import ResponseData

from flask import current_app

class BackendService():
    """ REST client to connect to the backend service.
    """

    def __init__(self,
        host: str, port: int,
        api_base_path: str = '/api/v1',
        apikey_header: str = 'X-ApiKey-Backend',
        apikey_secret: str = '' # ! Solo para resarrollo
        ):
        """ Constructor method.

        Initializes the client.

        Args:
            - host (str): The backend service host string.
            - port (int): The backend service port number.
            - api_base_path (str): The base path that is prepended to every request's path.
            - apikey_header (str): Name of the header with the API key that identifies this client.
            - apikey_secret (str): The API key that identifies this client.
        """
        self.__host: str = host
        self.__port: int = port
        self.__api_base_path: str = api_base_path
        self.__apikey_header: str = apikey_header
        self.__apikey_secret: str = apikey_secret

    def __get_data(self,token:Optional[str],url:str) -> ResponseData:
        """ Funcion template para hacer consultas de un diccionario determindao
        """
        resp_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + url,
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )

        resp_data.set_successful(response.ok)
        if resp_data.is_successful():
            resp_data.set_content(response.json())
        else:
            resp_data.add_message(response.content.decode('ascii'))
            resp_data.set_content([])
        return resp_data
    
    def __post_data(self,token:Optional[str],url:str,json:dict) -> ResponseData:
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + url,
            json=json,
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )

        current_app.logger.debug(json)

        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data
    
    def __put_data(self,token:Optional[str],url:str,json:dict) -> ResponseData:
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.put(
            self.__base_url() + url,
            json=json,
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )

        current_app.logger.debug(json)
        current_app.logger.debug(response_data.is_successful())

        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content({"codigo":204})
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def __base_url(self) -> str:
        return f'http://{self.__host}:{self.__port}{self.__api_base_path}'

    def get_questions(self, token: Optional[str]):
        """ Obtiene una lista de todas las preguntas
            No es necesario introducir un token para ver solo las preguntas
        """
        return self.__get_data(token=token,url=f'/questions')
    
    def get_question(self, token: Optional[str], qid:int):
        """ Obtiene una sola pregunta con sus respuestas y comentarios
        """
        return self.__get_data(token=token,url=f'/questions/{qid}')

    def get_answers(self, token: Optional[str], qid:int):
        """ Obtiene las respuestas a una pregunta con los comentarios
        """
        return self.__get_data(token=token,url=f'/questions/{qid}/answers')
    
    def post_question(self, token: Optional[str], title:str, body:str):
        """ Manda la peticion para crear una pregutna nueva
        """
        json:Dict = {
            'title':title,
            'body':body
        }

        return self.__post_data(
            token=token,
            url=f'/questions',
            json=json
        )
    
    def post_answer(self, token: Optional[str], qid:int, body:str):
        """ Manda la peticion para crear una respuesta nueva
        """
        json:Dict = {
            'qid':qid,
            'body':body
        }

        return self.__post_data(
            token=token,
            url=f'/questions/{qid}/answers',
            json=json
        )
    
    def post_comment(self, token: Optional[str], aid:int, body:str, sentiment:str):
        """ Manda la peticion para crear un comentario nueva
        """
        json:Dict = {
            'aid':aid,
            'body':body,
            'sentiment':sentiment
        }

        return self.__post_data(
            token=token,
            url=f'/answers/{aid}/comments',
            json=json
        )
    
    def get_reps_preguntas(self, token: Optional[str]):
        return self.__get_data(token=token,url=f'/questions/reports?pending=true&accepted=false&rejected=false')

    def get_reps_respuestas(self, token: Optional[str]):
        return self.__get_data(token=token,url=f'/answers/reports?pending=true&accepted=false&rejected=false')

    def get_reps_comentarios(self, token: Optional[str]):
        return self.__get_data(token=token,url=f'/comments/reports?pending=true&accepted=false&rejected=false')

    def put_question_report(self, token: Optional[str], qrid:int, status:str):
        json:Dict = {
            'status':status
        }
        return self.__put_data(
            token=token,
            url=f"/questions/reports/{qrid}",
            json=json
        )
    
    def put_answer_report(self, token: Optional[str], arid:int, status:str):
        json:Dict = {
            'status':status
        }
        return self.__put_data(
            token=token,
            url=f"/answers/reports/{arid}",
            json=json
        )
    
    def put_comment_report(self, token: Optional[str], crid:int, status:str):
        json:Dict = {
            'status':status
        }
        return self.__put_data(
            token=token,
            url=f"/comments/reports/{crid}",
            json=json
        )

    def post_report(self, token: Optional[str],reason:str,tipo:str,eid:int):
        json:Dict = {
            'reason':reason
        }

        traduccion = {
            "pregunta":"questions",
            "respuesta":"answers",
            "comentario":"comments"
        }

        current_app.logger.debug(f"tipo {traduccion[tipo]} - eid {eid}")

        url = f'/{traduccion[tipo]}/{eid}/reports'
        current_app.logger.debug(url)

        return self.__post_data(
            token=token,
            url=url,
            json=json
        )
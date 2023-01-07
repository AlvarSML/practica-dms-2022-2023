""" BackendService class module.
"""
from typing import Optional
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

    def __base_url(self) -> str:
        return f'http://{self.__host}:{self.__port}{self.__api_base_path}'

    def get_questions(self, token: Optional[str]):
        """ Obtiene una lista de todas las preguntas
            No es necesario introducir un token para ver solo las preguntas
        """
        resp_data: ResponseData = ResponseData()

        current_app.logger.warning(self.__apikey_secret)
        current_app.logger.warning(self.__apikey_header)

        response: requests.Response = requests.get(
            self.__base_url() + f'/questions',
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
    
    def get_question(self, token: Optional[str], qid:int):
        """ Obtiene una sola pregunta con sus respuestas y comentarios
        """
        resp_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/questions/{qid}',
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


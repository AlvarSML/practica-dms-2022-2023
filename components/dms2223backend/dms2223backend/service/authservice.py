""" AuthService class module.
"""

from typing import List, Optional, Union
import requests
from dms2223common.data import Role
from dms2223common.data.rest import ResponseData


class AuthService():
    """ REST client to connect to the authentication service.
        ! Copiado de dms2223auth, hay partes que pueden no funcionar
    """

    def __init__(self,
                 host: str, port: int,
                 api_base_path: str = '/api/v1',
                 apikey_header: str = 'X-ApiKey-Auth',
                 apikey_secret: str = ''
                 ):
        """ Constructor method.

        Initializes the client.

        Args:
            - host (str): The authentication service host string.
            - port (int): The authentication service port number.
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
        """ Constructs the base URL for the requests.

        Returns:
            - str: The base URL.
        """
        return f'http://{self.__host}:{self.__port}{self.__api_base_path}'

    def auth(self, token: Optional[str]) -> ResponseData:
        """ Performs an authentication request to the authentication service.

        Args:
            - token (Optional[str]): The user session token to validate.

        Returns:
            - ResponseData: If successful, the contents hold a string with a new user session token.
              Otherwise, the session is rejected (e.g., timed out, was invalidated, was missing)
        """
        response_data: ResponseData = ResponseData()
        if not token:
            response_data.set_successful(False)
            return response_data

        response: requests.Response = requests.post(
            self.__base_url() + '/auth',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.content.decode('ascii'))
        else:
            response_data.add_message('Session expired')
        return response_data

    def list_users(self, token: Optional[str]) -> ResponseData:
        """ Requests a list of registered users.

        Args:
            token (Optional[str]): The user session token.

        Returns:
            - ResponseData: If successful, the contents hold a list of user data dictionaries.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + '/users',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def get_user_roles(self, token: Optional[str], username: str) -> ResponseData:
        """ Requests the list of roles assigned to a user.

        Args:
            - token (Optional[str]): The user session token.
            - username (str): The name of the queried user.

        Returns:
            - ResponseData: If successful, the contents hold a list of role names. Otherwise an
              empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/users/{username}/roles',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def get_user(self) -> str:
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + '/auth',
            headers={
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )

        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

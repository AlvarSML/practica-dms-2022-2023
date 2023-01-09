""" Puntos de entrada de las peticiones de usuarios
"""
from typing import Dict, Tuple, Optional, List
from http import HTTPStatus
from dms2223backend.service import UsuariosServicio

from flask import current_app

def get_allusers() -> Tuple[List[Dict],Optional[int]]:
    with current_app.app_context():
        usuarios = UsuariosServicio.get_all(current_app.db)
    return (usuarios, HTTPStatus.OK)

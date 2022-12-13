""" RespuestasServicio class module.
"""

from typing import List, Dict, ClassVar
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db import Schema

from dms2223backend.data.db.Elemento import Pregunta, Respuesta, Comentario
from dms2223backend.data.db import Usuario, Voto, ReportePregunta
from dms2223backend.data.resultsets.pregunta_res import PreguntaFuncs
from dms2223backend.data.resultsets import UsuarioFuncs, RespuestaFuncs, FeedBackFuncs

from sqlalchemy import select

from dms2223backend.data.resultsets import ReporteFuncs

from .authservice import AuthService

import sys

class RespuestasServicio():
    """ Clase "estatica" que permite el acceso a las operaciones de creacion o consulta
        derivados de respuesta
    """

    @staticmethod
    def set_comment(schema:Schema,comentario:Dict) -> Dict:
        """ Construye la instancia de comentario para insertar en la base de datos
        """
        session: Session = schema.new_session()

        resp = RespuestaFuncs.get(comentario["aid"])
        usuario = UsuarioFuncs.get_or_create(comentario["autor"])
        feedback = FeedBackFuncs.get(comentario["feedback"])

        comm:Comentario = Comentario(
            contenido=comentario["body"],
            autor=usuario,
            respuesta=resp,
            feedback=feedback
        ) 

        schema.remove_session()
        return comm
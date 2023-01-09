""" Modulo encargado de realizar las consultas de datos a
    la base de datos a traves del ORM
"""
from typing import Optional
from datetime import datetime
from dms2223backend.data.db import Elemento
from sqlalchemy.orm.session import Session  # type: ignore

class ElementoFuncs():
    """ funciones estaticas sobre elemento
    """
    @staticmethod
    def set_hidden(session:Session, elemento:Elemento):
        """ Cambia la visibilidad de un elemento a oculto
        """
        elemento.visibilidad = False
        session.commit()
        session.refresh(elemento)
        return elemento
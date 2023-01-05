""" Modulo encargado de realizar las consultas de datos a
    la base de datos a traves del ORM
"""

from typing import List, Dict, Optional
from datetime import datetime

from dms2223backend.data.db import Elemento

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select # type: ignore

class ElementoFuncs():

    @staticmethod
    def set_hidden(session:Session, elemento:Elemento):
        """ Cambia la visibilidad de un elemento a oculto
        """
        elemento.visibilidad = False
        session.commit()
        session.refresh(elemento)
        return elemento
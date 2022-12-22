from dms2223backend.data.db import Usuario,Elemento,Voto
from typing import List, Dict, Optional
from datetime import datetime

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import select, exists # type: ignore

import sys

class VotoFuncs():

    def get(session:Session,elemento:Elemento,usuario_nombre:str) -> Voto:
        """ Obtiene un voto de un usuario en un elemento si existe
        """
        voto:Voto = elemento.votos\
            .join(Voto.autor)\
            .filter(Usuario.nombre == usuario_nombre)\
            .first()

        return voto

    def create(session:Session, voto:Voto) -> Voto:
        """ Crea un voto nuevo
        """
        session.add(voto)
        session.commit()
        session.refresh(voto)
        return voto
    
    def exists(session:Session, elemento:Elemento, usuario_nombre:str) -> int:
        """ Compruueba si un voto existe
        """
        voto = elemento.votos.filter_by(autor=usuario_nombre).first()
        return voto.id_voto    
    
    def delete(session:Session, voto:Voto) -> int:
        """ Elimina un voto
        """
        session.delete(voto)
        session.commit()
        return 0
        
    def get_all(session:Session, elemento:Elemento) -> List[Voto]:
        """ Obtiene todos los votos de un elemento
        """
        return elemento.votos.filter().all()
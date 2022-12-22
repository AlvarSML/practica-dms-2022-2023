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
        elem:Elemento = elemento.votos\
            .join(Voto.autor)\
            .filter(Usuario.nombre == usuario_nombre)\
            .first()

        return elem
    
    def toggle_vote(session:Session,voto:Voto) -> Voto:
        """ cambia el estado de un voto
            TODO: Limpiar returns
        """
        # 1. se intenta conseguir el voto
        nvoto:Voto = VotoFuncs.get(
            session=session,
            elemento=voto.elemento,
            usuario_nombre=voto.autor.nombre)

        if nvoto:
            # 2a. Si ya existe el voto se elimina
            session.delete(nvoto)
            session.commit()
            return None
        else:
            # 2b. Si no existe se crea uno nuevo
            session.add(voto)
            session.commit()
            session.refresh(voto)
            return voto      
        
    def get_all(session:Session, elemento:Elemento) -> List[Voto]:
        """ Obtiene todos los votos de un elemento
        """
        return elemento.votos.all()
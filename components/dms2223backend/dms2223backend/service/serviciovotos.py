from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db import Schema, Elemento, Voto, Tipo_voto, Usuario
from dms2223backend.data.resultsets import UsuarioFuncs, VotoFuncs
from typing import List, Dict, ClassVar
from sqlalchemy import select

import sys

class VotosServicio():

    def build_vote_dict(voto:Voto) -> Dict:
        return {
            "id":voto.id_voto,
            "element":voto.id_elemento,
            "user":voto.autor.nombre,
            "type":voto.tipo
        }

    def set_voto(schema:Schema, id:int, user:str) -> List[Dict]:
        """ Intento de generalizar
            TODO: pasar a la nueva capa
            TODO: Crear elemento funcs
        """
        session: Session = schema.new_session()
        
        # Obtencion de la dependencia del elemento para obtener los votos
        # ! Crear ElementoFuncs.get(id)
        elem:Elemento = session.query(Elemento)\
                        .filter(Elemento.id_elemento==id)\
                        .first()
        
        # Se busca el usuario del token
        autor:Usuario = UsuarioFuncs.get_or_create(
            session=session,
            nombre=user
        )

        # Construccion del voto a emitir
        voto:Voto = Voto(
            elemento = elem,
            tipo=Tipo_voto.positivo,
            autor=autor
        )

        # Se busca si el voto se ha emitido ya
        res:Voto = VotoFuncs.toggle_vote(
            session=session,
            voto=voto
        )

        session.refresh(elem)
        votos:List[Voto] = VotoFuncs.get_all(
            session=session,
            elemento=elem
        )

        print("elemento",file=sys.stderr)
        print(elem,file=sys.stderr)

        votos:List[Dict] = [VotosServicio.build_vote_dict(v) for v in votos]

        session.flush()
        schema.remove_session()

        return votos
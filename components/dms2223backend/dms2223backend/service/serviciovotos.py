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
            "type":voto.tipo.name
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

        # Se busca si el voto se ha emitido ya
        voto_existente:Voto = VotoFuncs.get(
            session=session,
            elemento=elem,
            usuario_nombre=autor.nombre
        )

        print("# voto_existente",file=sys.stderr)
        print(voto_existente,file=sys.stderr)

        # Si existe se elimina
        
        if voto_existente:
            VotoFuncs.delete(
                session=session,
                voto=voto_existente
            )
        else:
            VotoFuncs.create(
                session=session,
                voto=Voto(
                    elemento = elem,
                    tipo=Tipo_voto.positivo,
                    autor=autor
                )
            )
        
        session.refresh(elem)
        votos:List[Voto] = VotoFuncs.get_all(
            session=session,
            elemento=elem
        )


        votos:List[Dict] = [VotosServicio.build_vote_dict(v) for v in votos]

        session.flush()
        schema.remove_session()

        return votos
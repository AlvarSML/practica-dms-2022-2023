from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db import Schema, Elemento, Voto, Tipo_voto, Usuario
from typing import List, Dict, ClassVar
from sqlalchemy import select

import sys

class VotosServicio():

    def set_voto(schema:Schema, id:int, user:str) -> List[Dict]:
        """ Intento de generalizar
            TODO: pasar a la nueva capa
        """
        session: Session = schema.new_session()

        elem:Elemento = session.query(Elemento).filter(Elemento.id_elemento==id).first()

        voto:Voto = elem.votos.join(Voto.autor).filter(Usuario.nombre == user).first()

        if voto:
            session.delete(voto)
        else:
            print(elem.votos, file=sys.stderr)
            voto = Voto(
                elemento = session.query(Elemento).filter(Elemento.id_elemento == id).first(),
                tipo = Tipo_voto.positivo,
                autor=session.query(Usuario).filter(Usuario.nombre == user).first()
            )

        session.refresh(elem)
        
        print(voto, file=sys.stderr)
        session.flush()
        schema.remove_session()

        return elem
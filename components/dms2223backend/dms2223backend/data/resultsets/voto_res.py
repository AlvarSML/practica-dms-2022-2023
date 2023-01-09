""" Modulo de funciones de alto nivel para votos
"""
from dms2223backend.data.db import Usuario,Elemento,Voto, Tipo_voto
from typing import List
from sqlalchemy.orm.session import Session  # type: ignore



class VotoFuncs():
    """ Funciones de acceso a la BDD
    """
    @staticmethod
    def get(session:Session,elemento:Elemento,usuario_nombre:str) -> Voto:
        """ Obtiene un voto de un usuario en un elemento si existe
        """
        voto:Voto = elemento.votos\
            .join(Voto.autor)\
            .filter(Usuario.nombre == usuario_nombre)\
            .first()

        return voto
    
    @staticmethod
    def create(session:Session, voto:Voto) -> Voto:
        """ Crea un voto nuevo
        """
        session.add(voto)
        session.commit()
        session.refresh(voto)
        return voto

    @staticmethod
    def exists(session:Session, elemento:Elemento, usuario_nombre:str) -> int:
        """ Compruueba si un voto existe
        """
        voto = elemento.votos.filter_by(autor=usuario_nombre).first()
        return voto.id_voto

    @staticmethod
    def delete(session:Session, voto:Voto) -> int:
        """ Elimina un voto
        """
        session.delete(voto)
        session.commit()
        return 0

    @staticmethod
    def get_all(session:Session, elemento:Elemento) -> List[Voto]:
        """ Obtiene todos los votos de un elemento
        """
        return elemento.votos.filter().all()

    @staticmethod
    def get_type(session:Session, elemento:Elemento, tipo_voto:Tipo_voto) -> List[Voto]:
        """ Obtiene el numero de votos de un tipo concreto
        """
        return elemento.votos.filter_by(tipo=tipo_voto).all()

    @staticmethod
    def get_type_count(session:Session, elemento:Elemento, tipo_voto:Tipo_voto) -> List[Voto]:
        """ Obtiene el numero de votos de un tipo concreto
        """
        return elemento.votos.filter_by(tipo=tipo_voto).count()

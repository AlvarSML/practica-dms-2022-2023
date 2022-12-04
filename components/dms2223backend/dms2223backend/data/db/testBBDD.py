#!/usr/bin/env python3

def testBBDD():
    """
    >>> from orm import Schema
    >>> from orm.results import User, UserSession
    >>> schema = Schema('sqlite:///:memory:')
    >>> elemento1 = Elemento('Elemento1', 'elemento1pass')
    >>> elemento2 = Elemento('Elemento2', 'elemento2pass')
    >>> reporte1 = Reporte('Reporte1', 'reporte1pass')
    >>> reporte2 = Reporte('Reporte2', 'reporte2pass')
    >>> usuario1 = Usuario('Usuario1', 'usuario1pass')
    >>> usuario2 = Usuario('Usuario2', 'usuario2pass')
    >>> voto1 = Voto('Voto1', 'voto1pass')
    >>> voto2 = Voto('Voto2', 'voto2pass')
    >>> comentario1 = Comentario('Comentario1', 'comentario1pass')
    >>> comentario2 = Comentario('Comentario2', 'comentario2pass')
    >>> respuesta1 = Respuesta('Respuesta1', 'respuesta1pass')
    >>> respuesta2 = Respuesta('Respuesta2', 'respuesta2pass')
    >>> pregunta1 = Pregunta('Pregunta1', 'pregunta1pass')
    >>> pregunta2 = Pregunta('Pregunta2', 'pregunta2pass')
    >>> feedback1 = Feedback('Feedback1', 'feedback1pass')
    >>> feedback2 = Feedback('Feedback2', 'feedback2pass')




    >>> session1_1 = UserSession('12345678-1234-1234-1234-123456789012', 'User1')
    >>> db_session = schema.new_session()
    >>> db_session.add_all([usr1, usr2, session1_1])
    >>> db_session.commit()
    >>> for instance in db_session.query(User).order_by(User.username):
    ... print (instance.username, instance.password)
    
    
    User1 usr1pass
    User2 usr2pass
    Elemento1 elemento1pass
    Elemento2 elemento2pass
    Reporte1 reporte1pass
    Reporte2 reporte2pass
    Usuario1 usuario1pass
    Usuario2 usuario2pass
    Voto1 voto1pass
    Voto2 voto2pass
    Comentario1 comentario1pass
    Comentario2 comentario2pass
    Respuesta1 respuesta1pass
    Respuesta2 respuesta2pass
    Pregunta1 pregunta1pass
    Pregunta2 pregunta2pass
    Feedback1 feedback1pass
    Feedback2 feedback2pass
    """
    pass
if __name__ == "__main__":
    import doctest
    doctest.testmod()

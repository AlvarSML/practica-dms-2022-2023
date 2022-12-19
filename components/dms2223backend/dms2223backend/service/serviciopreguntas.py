""" UserServices class module.
"""

from typing import List, Dict, ClassVar
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db import Schema

from dms2223backend.data.db.Elemento import Pregunta, Respuesta, Comentario
from dms2223backend.data.db import Usuario, Voto
from dms2223backend.data.resultsets.pregunta_res import PreguntaFuncs
from dms2223backend.data.resultsets.usuario_res import UsuarioFuncs


from sqlalchemy import select

from dms2223backend.data.resultsets.reporte_res import ReporteFuncs

class PreguntasServicio():
    """ Clase "estatica" que permite el acceso a las operaciones de creacion o consulta
        derivados de pregunta
    """
##SINGLE RESPONSABILITY PRINCIPLE   
    @staticmethod
    def get_pregunta(schema:Schema, qid:int) -> Dict:
        """Obtiene los datos de una pregunta se debe usar para la visualizacion
            en lista de pregunta, no contiene los votos de las respuestas 
        """
        session: Session = schema.new_session()
        preg: Pregunta = PreguntaFuncs.get_pregunta(session, qid)
        
        resp:Dict = {
            "qid":preg.id_pregunta,
            "title":preg.titulo,
            "timestamp":preg.fecha
        }

        schema.remove_session()
        return resp

    @staticmethod
    def get_preguntas(schema:Schema) -> List[Pregunta]:
        """ Devuleve una lista de todas las preguntas
        """
        session: Session = schema.new_session()
        preguntas = PreguntaFuncs.list_all(10,session)
        schema.remove_session()
        return preguntas
    
    def get_preguntas_filtro(schema:Schema,campo:type,valor:str) -> List[Pregunta]:
        session: Session = schema.new_session()
        stmt = select(Pregunta).where(campo == valor)
        preguntas = session.execute(stmt).all()
        schema.remove_session()
        return preguntas

    @staticmethod
    def create_pregunta(schema:Schema,datos:Dict) -> Dict:
        """ Construye el objeto Pregunta que se insertara en la BDD
        """
        session: Session = schema.new_session()

        usu = UsuarioFuncs.get_or_create(
            session=session,
            nombre=datos["autor"])
        session.refresh(usu)

        preg:Pregunta = Pregunta(
            titulo=datos["titulo"],
            contenido=datos["contenido"],
            autor=usu
        )
        

        res = PreguntaFuncs.create(session,preg)
        resp:Dict = {
            "qid":res.id_pregunta,
            "title":res.titulo,
            "tiemstamp":res.fecha,
            "pos_votes":-1,
            "neg_votes":-1,
            "body":res.contenido,
            "owner":{"username":res.autor.nombre}
        }
        schema.remove_session()
        return resp

    @staticmethod
    def get_answers(schema:Schema,qid:int) -> List[Dict]:
        """ Construye la lista de respuestas (y comentarios) a una pregunta
        """
        session: Session = schema.new_session()
        res = PreguntaFuncs.get(session=session,qid=qid)
        
        session.refresh(res)

        answers:List[Dict] = []

        for answer in res.respuestas:
            session.refresh(answer)

            comentarios:List = []
            for comm in answer.comentarios:
                comentarios.append({
                    "id":comm.id_comentario,
                    "aid":answer.id_respuesta,
                    "timestamp":comm.fecha,
                    "body":comm.contenido,
                    "owner":{"username":comm.autor.nombre},
                    "votes":3,
                    "sentiment":"POSITIVE"
                })

            answers.append({
                "id":answer.id_respuesta,
                "qid":qid,
                "timestamp":answer.fecha,
                "body":answer.contenido,
                "owner":{"username":answer.autor.nombre},
                "comments":comentarios
            })

        schema.remove_session()    
        return answers

    def get_all_reports(schema:Schema) -> list:
        """ Transforma los reportes en una lista
        """
        session: Session = schema.new_session()
        reports:List = []
        res = ReporteFuncs.get_question_reps(session)
        for rep in res:
            reports.append({
                "id":rep.id_reporte,
                "qid":rep.id_pregunta,
                "reason":rep.razon_reporte,
                "status":rep.estado.name,
                "owner":{"username":rep.autor.nombre},
                "timestamp":rep.fecha
            })
        schema.remove_session()  
        return reports

    def set_report(schema:Schema,reporte:Dict) -> Dict:
        session: Session = schema.new_session()

        p = PreguntaFuncs.get(session,reporte["qid"])
        usu = UsuarioFuncs.get_or_create(
            session=session,
            nombre=reporte["autor"])
        session.refresh(usu)

        rep:ReportePregunta = ReportePregunta(
            pregunta=p,
            razon_reporte=reporte["razon_reporte"],
            autor=usu
        )

        rep = ReporteFuncs.create_question_reps(session,rep)
        resp:Dict = {
            "id":rep.id_reporte,
            "qid":rep.id_pregunta,
            "reason":rep.razon_reporte,
            "status":rep.estado.name,
            "owner":{"username":rep.autor.nombre},
            "timestamp":rep.fecha
        }
        schema.remove_session()
        return resp
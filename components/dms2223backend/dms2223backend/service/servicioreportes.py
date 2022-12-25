from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db import Reporte, Schema

from dms2223backend.data.db import ReporteRespuesta, Reporte, ReportePregunta,\
     ReporteComentario, Estado_moderacion

from dms2223backend.data.resultsets import UsuarioFuncs, RespuestaFuncs, ReporteFuncs,\
     ComentarioFuncs, PreguntaFuncs

from typing import List, Dict, ClassVar
from sqlalchemy import select, inspect

import sys



class ReportesServicio():

    # Tablas de traduccion para automatizar los reportes
    # se añaden porque los id de las clases son distintos 
    # a los que queremos devolver.
    # En caso de añadir un nuevo tipo de reporte se deberia
    # modificar

    dict_fk_equiv:Dict = {
        ReporteComentario:"cid",
        ReporteRespuesta:"aid",
        ReportePregunta:"qid"
    }

    dict_id_equiv:Dict = {
        ReporteComentario:"comentario",
        ReporteRespuesta:"respuesta",
        ReportePregunta:"pregunta"
    }

    @staticmethod
    def build_dict_report(reporte:Reporte, id_type:str, id_elem_type:str) -> Dict:
        """ Genera un diccionario generico de reporte
        """
        return  {
            "id":reporte.id_reporte,
            id_type:getattr(reporte, id_elem_type).id_elemento,
            "reason":reporte.razon_reporte,
            "status":reporte.estado.name,
            "owner":{"username":reporte.autor.nombre},
            "timestamp":reporte.fecha
        }
    
    @staticmethod
    def get_reports(schema:Schema, rep_type:type ,estados:List[Estado_moderacion]):
        """ Funcion generica para obtener una lista de reportes
            Nescisita saber el tipo de reporte que se quiere y la equivalencia de id,
            que esta *hardcodeado*
        """
        session:Session = schema.new_session()

        # se usan tablas de traduccion para obtener los ids equivalentes
        fk:str = ReportesServicio.dict_fk_equiv[rep_type]
        attr:str = ReportesServicio.dict_id_equiv[rep_type]
        reports:List = []

        res = ReporteFuncs.get_reps(
            session=session,
            tipo=rep_type,
            estados=estados
            )

        for rep in res:
            reports.append(ReportesServicio.build_dict_report(
                reporte=rep,
                id_type=fk,
                id_elem_type=attr
                ))
        
        session.flush()
        schema.remove_session()  
        return reports
        


    @staticmethod
    def get_quest_reports(schema:Schema, estados:List[Estado_moderacion]) -> List[Dict]:
        """ Transforma los reportes en una lista
        """ 
        return ReportesServicio.get_reports(
            schema=schema,
            rep_type=ReportePregunta,
            estados=estados
        )
    
    @staticmethod
    def get_ans_reports(schema:Schema, estados:List[Estado_moderacion]) -> List[Dict]:
        """ Transforma los reportes en una lista
        """
        return ReportesServicio.get_reports(
            schema=schema,
            rep_type=ReporteRespuesta,
            estados=estados
        )

    @staticmethod
    def get_comm_reports(schema:Schema, estados:List[Estado_moderacion]) -> List[Dict]:
        """ Transforma los reportes en una lista
        """
        return ReportesServicio.get_reports(
            schema=schema,
            rep_type=ReporteComentario,
            estados=estados
        )

    @staticmethod
    def set_report_answer(schema:Schema,reporte:Dict) -> Dict:
        """ Construye un reporte para introducirlo en la bdd
            TODO: que exista al respuesta
        """
        session: Session = schema.new_session()

        # Obtencion de datos previos inyeccion, de depnendencias

        resp = RespuestaFuncs.get(
            session=session,
            aid=reporte["aid"])

        usuario = UsuarioFuncs.get_or_create(
            session=session,
            nombre=reporte["autor"])

        # Construccion de respuesta

        rep:ReporteRespuesta = ReporteRespuesta(
            respuesta=resp,
            razon_reporte=reporte["razon_reporte"],
            autor=usuario
        )

        # Se introduce el reporte en la bdd

        res:ReporteRespuesta = ReporteFuncs.create_rep(
            session=session,
            reporte=rep
        )

        reporte_dict:Dict = {
            "id":res.id_reporte,
            "aid":res.id_respuesta,
            "reason":res.razon_reporte,
            "status":res.estado.name,
            "owner":{"username":res.autor.nombre},
            "timestamp":res.fecha
        }

        schema.remove_session()
        return reporte_dict

    @staticmethod
    def set_report_comment(schema:Schema,reporte:Dict) -> Dict:
        """ Construye un reporte para introducirlo en la bdd
            TODO: que exista el comentario
        """
        session: Session = schema.new_session()

        # Obtencion de datos previos inyeccion, de depnendencias

        comm = ComentarioFuncs.get(
            session=session,
            cid=reporte["cid"])

        usuario = UsuarioFuncs.get_or_create(
            session=session,
            nombre=reporte["autor"])

        # Construccion de respuesta

        rep:ReporteComentario = ReporteComentario(
            comentario=comm,
            razon_reporte=reporte["razon_reporte"],
            autor=usuario
        )

        # Se introduce el reporte en la bdd

        res:ReporteComentario = ReporteFuncs.create_rep(
            session=session,
            reporte=rep
        )

        reporte_dict:Dict = {
            "id":res.id_reporte,
            "cid":res.id_comentario,
            "reason":res.razon_reporte,
            "status":res.estado.name,
            "owner":{"username":res.autor.nombre},
            "timestamp":res.fecha
        }

        schema.remove_session()
        return reporte_dict

    @staticmethod
    def set_report_question(schema:Schema,reporte:Dict) -> Dict:
        """ Construye un reporte para introducirlo en la bdd
            TODO: que exista el comentario
        """
        session: Session = schema.new_session()

        # Obtencion de datos previos inyeccion, de depnendencias

        quest = PreguntaFuncs.get(
            session=session,
            qid=reporte["qid"])

        usuario = UsuarioFuncs.get_or_create(
            session=session,
            nombre=reporte["autor"])

        # Construccion de respuesta

        rep:ReportePregunta = ReportePregunta(
            pregunta=quest,
            razon_reporte=reporte["razon_reporte"],
            autor=usuario
        )

        # Se introduce el reporte en la bdd

        res:ReportePregunta = ReporteFuncs.create_rep(
            session=session,
            reporte=rep
        )

        reporte_dict:Dict = {
            "id":res.id_reporte,
            "qid":res.id_pregunta,
            "reason":res.razon_reporte,
            "status":res.estado.name,
            "owner":{"username":res.autor.nombre},
            "timestamp":res.fecha
        }

        schema.remove_session()
        return reporte_dict

    @staticmethod
    def set_estado(schema:Schema, reporte:Dict) -> Dict:
        """ Cambia el estado de un reporte a una respuesta
        """
        session: Session = schema.new_session()

        # Se obtiene el reporte a modificar
        reporte_nuevo:Reporte = ReporteFuncs.get_rep(
            session=session,
            tipo=Reporte,
            rid=reporte["rid"]
        )

        print(reporte_nuevo,file=sys.stderr)

        # Se modifica el estado
        reporte_nuevo = ReporteFuncs.set_state(
            session=session,
            reporte=reporte_nuevo,
            estado=reporte["estado"]
        )

        # Se convierte el objeto a diccionario
        reporte_resp:Dict = ReportesServicio.build_dict_report(
            reporte=reporte_nuevo, 
            id_type="cid", 
            id_elem_type="comentario")

        session.flush()
        schema.remove_session()  
        return reporte_resp
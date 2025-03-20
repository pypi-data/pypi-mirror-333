
from typing import Any as Cualquiera, Callable as Llamable, Optional as Opcional, Type as Tipo, Union, Iterator as Iterador, Generator as Generador
import flask.globals
from werkzeug.wrappers.request import Request as Solicitud
from werkzeug.wrappers.response import  Response as Respuesta
from functools import cache

class VistaNoExiste(Exception):...

@cache
def obtenerFuncionVistaPorRegla(regla : str, metodo :str ="GET") -> Cualquiera:
    from flask import current_app as aplicacion
    """
    Levanta:  
        `VistaNoExiste`
    """
    for entrada_regla in aplicacion.url_map.iter_rules():
        if entrada_regla.rule == regla\
            and metodo in (entrada_regla.methods, "GET"):
            return aplicacion.view_functions[entrada_regla.endpoint]
    raise VistaNoExiste(f"No se pudo encontrar la vista asociada a {regla}, con el método {metodo}.")

Condicion : AliasDeTipo = Llamable[[Opcional[Flask], Opcional[flask.globals._AppCtxGlobals], Opcional[Solicitud]],bool]

def registarCondicion(condicion : Llamable[[Opcional[Flask], Opcional[flask.globals._AppCtxGlobals], Opcional[Solicitud],...],Cualquiera],*posicionales,**nominales) -> Condicion:
    def condicion(aplicacion : Opcional[Flask], g : Opcional[flask.globals._AppCtxGlobals] = None, solicitud : Opcional[Solicitud] = None) -> bool: 
        return bool(f(aplicacion,g,solicitud*posicionales,**nominales))
    return condicion

def registrarRedireccionCondicional(condicion : Condicion, g : Opcional[flask.globals._AppCtxGlobals] = None, solicitud : Opcional[Solicitud] = None, crearRespuesta : Opcional[Llamable[...,Respuesta]] = None, redireccionar : Opcional[Llamable[[str,int, Opcional[type[Respuesta]]],Respuesta]]=None) -> Llamable[[str,str,str,bool],Llamable]:
    import flask
    if g is None : g = flask.g 
    if solicitud is None : solicitud = flask.request
    if crearRespuesta is None : crearRespuesta = flask.make_response
    if redireccionar is None : redireccionar = flask.redirect
    from flask import current_app as aplicacion

    from functools import wraps
    def redireccionCondicional(redireccion : str ="/",HX_Retarget : str ="body", HX_Reswap : str ="outerHTML", HX_Push_Url: Union[bool, str] = True, admin : bool =False) -> Llamable:
        def decorador(vista: Llamable) -> Llamable:
            @wraps(vista)
            def vistaDecorada(*args, **kwargs):
                if not condicion(aplicacion,g,solicitud):
                    if solicitud.headers.get("Hx-Request",None) or solicitud.headers.get("HX-Request",None):
                        with aplicacion.app_context(), aplicacion.test_request_context(
                            environ_overrides=solicitud.environ
                        ):
                            _ = g
                            for func in aplicacion.before_request_funcs.get(None, []):
                                func()
                            respuesta = crearRespuesta(obtenerFuncionVistaPorRegla(redireccion)())
                            respuesta.headers['HX-Retarget'] = HX_Retarget
                            respuesta.headers['HX-Reswap'] = HX_Reswap
                            if HX_Push_Url:                    
                                respuesta.headers['HX-Replace-Url'] = HX_Push_Url if isinstance(HX_Push_Url,str) else redireccion
                                respuesta.headers['HX-Push-Url'] = HX_Push_Url if isinstance(HX_Push_Url,str) else redireccion
                        return respuesta
                    else:   
                        return redireccionar(redireccion,303)
                return vista(*args, **kwargs)
            return vistaDecorada
        return decorador
    return redireccionCondicional

def registrarRequiereUsuario(tipo_usuario : Tipo = object, tipo_admin: Tipo = object, g : Opcional[flask.globals._AppCtxGlobals] = None, solicitud : Opcional[Solicitud] = None, crearRespuesta : Opcional[Llamable[...,Respuesta]] = None, redireccionar : Opcional[Llamable[[str,int, Opcional[type[Respuesta]]],Respuesta]]=None) -> Llamable[[str,str,str,bool],Llamable]:
    import flask
    if g is None : g = flask.g 
    if solicitud is None : solicitud = flask.request
    if crearRespuesta is None : crearRespuesta = flask.make_response
    if redireccionar is None : redireccionar = flask.redirect
    from flask import current_app as aplicacion

    from functools import wraps
    def requiereUsuario(redireccion : str ="/",HX_Retarget : str ="body", HX_Reswap : str ="outerHTML", HX_Push_Url: Union[bool, str] = True, admin : bool =False) -> Llamable:
        def decorador(vista: Llamable) -> Llamable:
            @wraps(vista)
            def vistaDecorada(*args, **kwargs):
                if "este_usuario" not in g\
                or not isinstance(g.este_usuario, tipo_usuario)\
                or not g.este_usuario or ((not (isinstance(g.este_usuario, tipo_admin) and admin)) if admin else False):
                    if solicitud.headers.get("Hx-Request",None) or solicitud.headers.get("HX-Request",None):
                        with aplicacion.app_context(), aplicacion.test_request_context(
                            environ_overrides=solicitud.environ
                        ):
                            _ = g
                            for func in aplicacion.before_request_funcs.get(None, []):
                                func()
                            respuesta = crearRespuesta(obtenerFuncionVistaPorRegla(redireccion)())
                            respuesta.headers['HX-Retarget'] = HX_Retarget
                            respuesta.headers['HX-Reswap'] = HX_Reswap
                            if HX_Push_Url:                    
                                respuesta.headers['HX-Replace-Url'] = HX_Push_Url if isinstance(HX_Push_Url,str) else redireccion
                                respuesta.headers['HX-Push-Url'] = HX_Push_Url if isinstance(HX_Push_Url,str) else redireccion
                        return respuesta
                    else:   
                        return redireccionar(redireccion,303)
                return vista(*args, **kwargs)
            return vistaDecorada
        return decorador
    return requiereUsuario



CuerpoRespuesta : AliasDeTipo = Union[str, bytes, dict, list, Iterator, Generator]
CodigoRespuesta : AliasDeTipo = Union[str,int]
EncabezadosRespuesta : AliasDeTipo = Union[dict[str,str],list[tuple[str,str]]]
TuplaRespuesta : AliasDeTipo = Union[tuple[CuerpoRespuesta,CodigoRespuesta,EncabezadosRespuesta],tuple[CuerpoRespuesta,CodigoRespuesta],tuple[CuerpoRespuesta,EncabezadosRespuesta]]
Union[
    tuple[
        cuerpoRespuesta,
        Union[str,int]
    ],
    tuple[
        Union[str, bytes, dict, list],
        Union[str,int]
    ],
]
def crearRespuesta(s: Solicitud, r: Union[Respuesta,CuerpoRespuesta, TuplaRespuesta]): ...

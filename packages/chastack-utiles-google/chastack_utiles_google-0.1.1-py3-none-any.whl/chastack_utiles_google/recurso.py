from googleapiclient.errors import HttpError as ErrorHttp
from googleapiclient.http import HttpRequest as SolicitudHttp
from googleapiclient.discovery import build as construirRecurso, Resource as Recurso
from google.oauth2.service_account import Credentials as Credenciales
from enum import Enum

import json
import base64

from solteron import Solteron

class TipoServicioGoogleApi(Enum):
    _invalido = 0,
    DRIVE = 1,
    DOCS = 2,
    SHEETS = 3,
    GMAIL = 4,
    CALENDAR = 5

INFO_GOOGLE_APIS : dict  = {
    TipoServicioGoogleApi.DRIVE : {
        'nombre' : 'drive',
        'version' : 'v3',
        'alcances' : [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive'
        ]
    },
    TipoServicioGoogleApi.DOCS : {        
        'nombre' : 'docs',
        'version' : 'v1',
        'alcances' : [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive'
        ]
    },
    TipoServicioGoogleApi.SHEETS : {
        'nombre' : 'sheets',
        'version' : 'v4',
        'alcances' : [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
    },
    TipoServicioGoogleApi.GMAIL : {
        'nombre' : 'gmail',
        'version' : 'v1',
        'alcances' : [
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.send',
            'https://mail.google.com'
        ]
    },        
    TipoServicioGoogleApi.CALENDAR : {
        'nombre' : 'calendar',
        'version' : 'v3',
        'alcances' : [
            'https://www.googleapis.com/auth/calendar'
        ]
    }
}

class Recurso(metaclass=Solteron):
    __slots__ = ('__recursoSubyacente',)
    __recursoSubyacente : Recurso

    def __init__(self, credencialesJSON : Mapping[str,str], servicio : TipoServicioGoogleApi,**nominales) -> None: 
        SERVICIO = INFO_GOOGLE_APIS.get(servicio)
        ENDPOINTS_HABILITADOS = SERVICIO.get('alcances')
        INFO_CUENTA_DE_SERVICIO = credencialesJSON

        credenciales_montadas : Credenciales = Credenciales.from_service_account_info(INFO_CUENTA_DE_SERVICIO, scopes=ENDPOINTS_HABILITADOS, **nominales)
        try:
            recurso_autorizado = construirRecurso(SERVICIO.get('nombres'), SERVICIO.get('version'), credentials=credenciales_montadas)
        except ErrorHttp as error:
            recurso_autorizado = None
            raise error
        self.__recursoSubyacente = recurso_autorizado

    def __del__(self):
        self.__recursoSubyacente.close()
    
        return enviarMensaje 


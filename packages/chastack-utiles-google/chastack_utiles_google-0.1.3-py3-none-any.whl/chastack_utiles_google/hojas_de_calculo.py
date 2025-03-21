from googleapiclient.errors import HttpError as ErrorHttp
from googleapiclient.http import HttpRequest as SolicitudHttp
from googleapiclient.discovery import build as construirRecurso, Resource as Recurso
from google.oauth2.service_account import Credentials as Credenciales
from enum import Enum

from typing import Optional as Opcional, List as Lista, Any as Cualquiera, TypeAlias as AliasDeTipo
from typing import Optional, List, Any, TypeAlias as AliasDeTipo, Mapping, Self, Dict, Iterable

import json
import base64

from sobrecargar import sobrecargar
from solteron import Solteron
from chastack_utiles_google.recurso import Recurso, TipoServicioGoogleApi

Matriz : AliasDeTipo = Lista[Lista[Cualquiera]]

class HojaDeCalculo:
    __slots__ = ('__servicio','id')
    __servicio : 'gSheets'
    id : str

    class ModoEscribir(Enum):
        _invalido = 0
        ACTUALIZAR = 1
        AGREGAR = 2

    @sobrecargar
    def __init__(self, servicio : 'gSheets', titulo : str):
        """Crea una nueva hoja"""
        self.__servicio = servicio
        self.id = self.__servicio.crear(titulo).get('spreadsheetId')

    @sobrecargar
    def __init__(self, servicio : 'gSheets', data_hoja : dict):
        self.__servicio = servicio
        self.id = data_hoja.get('spreadsheetId')

    def escribir(self, rango_celdas : str, data_a_escribir : Matriz,modo : HojaDeCalculo.ModoEscribir = HojaDeCalculo.ModoEscribir.ACTUALIZAR):
        return self.__servicio.escribir(self.id, rango_celdas, data_a_escribir, modo)

    def leer(self, rango_celdas:str) -> Opcional[Matriz]:
        return self.__servicio.leer(self.id,rango_celdas)

    def borrar(self, rango_celdas:str) -> Opcional[Matriz]:
        return self.__servicio.borrar(self.id,rango_celdas)

    def eliminar(self):
        return self.__servicio.eliminar(self.id)

class gSheets(Recurso):
    __slots__ = ('__recursoSubyacente',)
    __recursoSubyacente : Recurso

    def __init__(self, credencialesJSON : Mapping[str,str], remitente : str):
        super().__init__(
            credencialesJSON=credencialesJSON,
            servicio=TipoServicioGoogleApi.SHEETS
        )

    def crear(self, titulo_nueva_hoja : str) -> HojaDeCalculo:
        metadata = {
            'properties': {
                'title': titulo_nueva_hoja
            }
        }
        try:
            nueva_hoja = self.__recursoSubyacente   \
                            .spreadsheets()         \
                            .create(
                                body=metadata,
                                fields='spreadsheetId'
                            )

            return HojaDeCalculo(
                self,
                nueva_hoja
            ) 
        except HttpError as error:
            print(f"[ERROR] Ocurrió un error al tratar de crear la hoja {titulo_nueva_hoja}: {error}\n")
            raise
    
    def leer(self, id_hoja : str, rango_celdas : str) -> Opcional[Matriz]:
        try:
            resultado = self.__recursoSubyacente \
                            .spreadsheets()       \
                            .values()              \
                            .get(
                                spreadsheetId = id_hoja,
                                range = rango_celdas
                            ).execute()

            valores = resultado.get('values', [])
            if not valores:
                valores = False 
            return valores    
        except HttpError as error:
            print(f"[ERROR] Ocurrió un error al tratar de leer los valores del rango {rango_celdas}, de la hoja de ID {id_hoja}: {error}\n")
            raise
    
    def escribir(self, id_hoja : str, rango_celdas : str, data_a_escribir : Matriz, modo : HojaDeCalculo.ModoEscribir = HojaDeCalculo.ModoEscribir.ACTUALIZAR):
        try:
            solicitud = self.__recursoSubyacente.spreadsheets().values()
            parametros : dict = dict(
                spreadsheetId = id_hoja, 
                range = rango_celdas, 
                valueInputOption = "USER_ENTERED", 
                body = { "values" : data_a_escribir }
            )
            match modo:
                case HojaDeCalculo.ModoEscribir.AGREGAR:
                    solicitud = solicitud.append(**parametros)
                case HojaDeCalculo.ModoEscribir.ACTUALIZAR | _:
                    solicitud = solicitud.update(**parametros)
            resultado = solicitud.execute()
            return resultado

        except HttpError as error:
            print(f"[ERROR] Ocurrió un error al tratar de escribir en la hoja de ID {id_hoja}: {error}\n")
            raise


    def borrar(self, id_hoja: str, rango_celdas : str):
        try:
            
            resultado = self.__recursoSubyacente.spreadsheets().values().clear(spreadsheetId=id_hoja, range=rango_celdas).execute()
            print(f'Se borraron los valores del rango indicado satisfactoriamente: \n{json.dumps(resultado, indent=4,sort_keys=True)}\n')
        except HttpError as error:
            print(f"Ocurrió un error al tratar de borrar los valores del rango {rango_celdas}, de la hoja de ID {id_hoja}: {error}\n")
            resultado = None
        return resultado

    def eliminar(self,id_hoja : str): 
        try:
            resultado =self.__recursoSubyacente.spreadsheets().delete(spreadsheetId=id_hoja)
            print(f'Se eliminó la hoja satisfactoriamente: \n{json.dumps(resultado, indent=4,sort_keys=True)}\n')

        except HttpError as error:
            print(f"Ocurrió un error al tratar de eliminar la hoja de ID {id_hoja}: {error}\n")
            resultado = None
        print()
        return resultado
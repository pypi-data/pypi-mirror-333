from googleapiclient.errors import HttpError as ErrorHttp
from googleapiclient.http import HttpRequest as SolicitudHttp
from googleapiclient.discovery import build as construirRecurso, Resource as Recurso
from google.oauth2.service_account import Credentials as Credenciales

from typing import Optional as Opcional
from typing import Optional, List, Any, TypeAlias as AliasDeTipo, Mapping, Self, Dict, Iterable
from typing import IO
from mimetypes import guess_type as adivinarTipoMIME 
from email.message import EmailMessage as CorreoElectronico
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage as MIMEImagen
from email.mime.text import MIMEText as MIMETexto

import json
import base64

from solteron import Solteron
from chastack_utiles_google.recurso import Recurso, TipoServicioGoogleApi

class Correo():
    __slots__ = ('__correoBase','__correoCodificado')
    __correoBase : CorreoElectronico 
    __correoCodificado : Opcional[dict[str,str]]

    def __init__(self, correoBase : CorreoElectronico):
        self.__correoBase : CorreoElectronico  = correoBase
        self.__correoCodificado : Opcional[dict[str,str]] = None

    @classmethod
    def crear(cls,remitente:str,destinatario: Iterable[str] | str,asunto:str,cuerpo:str) -> 'Correo':
        mensaje = CorreoElectronico()

        mensaje['To'] = destinatario if isinstance(destinatario,str) else ", ".join(destinatario) if isinstance(destinatario, Iterable) else ''
        mensaje['From'] = remitente
        mensaje['Subject'] = asunto
        mensaje.set_content(cuerpo)
        return cls(mensaje)

    def anadirAdjunto(self, adjunto: IO[Any] | bytes |str)-> Self:
        tipoSubtipo, _ = adivinarTipoMIME(adjunto)
        tipoAdjunto, subtipoAdjunto = tipoSubtipo.split('/')

        if isinstance(adjunto,str):
            with open(adjunto, 'rb') as f:
                dataAdjunto = f.read()
        elif isinstance(adjunto, IO) or isinstance(adjunto, bytes):
            dataAdjunto = adjunto
        else:
            raise TypeError(f'Adjunto debe ser IO, bytes o bien una str con la ruta al archivo. En cambio es {type(adjunto)}.')

        self.__correoBase.add_attachment(dataAdjunto, tipoAdjunto, subtipoAdjunto,filename=adjunto)
        return self

    def codificar(self) -> Self:
        self.__correoCodificado = {'raw': base64.urlsafe_b64encode(self.__correoBase.as_bytes()).decode()}
        return self
    
    def mensajeCodificado(self) -> Dict[str,str]:
        if self.__correoCodificado is None:
            self.codificar()
        return self.__correoCodificado

class CorreoHTML():
    __slots__ = ('__correoBase','__correoCodificado')
    __correoBase : CorreoElectronico 
    __correoCodificado : Opcional[dict[str,str]]

    def __init__(self, correoBase : CorreoElectronico):
        self.__correoBase : CorreoElectronico  = correoBase
        self.__correoCodificado : Opcional[dict[str,str]] = None

    @classmethod
    def crear(cls,remitente:str,destinatario: Iterable[str] | str,asunto:str,html:str) -> 'CorreoHTML':
        mensaje = MIMETexto(html,'html')

        mensaje['To'] = destinatario if isinstance(destinatario,str) else ", ".join(destinatario) if isinstance(destinatario, Iterable) else ''
        mensaje['From'] = remitente
        mensaje['Subject'] = asunto
        return cls(mensaje)

    def codificar(self) -> Self:
        self.__correoCodificado = {'raw': base64.urlsafe_b64encode(self.__correoBase.as_bytes()).decode()}
        return self
    
    def mensajeCodificado(self) -> Dict[str,str]:
        if self.__correoCodificado is None:
            self.codificar()
        return self.__correoCodificado

class gMail(Recurso):
    __slots__ = ('__recursoSubyacente',)
    __recursoSubyacente : Recurso

    def __init__(self, credencialesJSON : Mapping[str,str], remitente : str):
        super().__init__(
            credencialesJSON=credencialesJSON,
            servicio=TipoServicioGoogleApi.GMAIL,
            subject=remitente
        )

    def enviarCorreo(self, correo : Correo | CorreoHTML):
        try:
            enviarMensaje = self.__recursoSubyacente \
                            .users()                  \
                            .messages()                \
                            .send(
                                userId="me",
                                body=correo.mensajeCodificado()
                            ).execute()
        except ErrorHttp as error: 
            enviarMensaje = None
            raise(error)

        return enviarMensaje 



if __name__ == '__main__':
    print(__doc__)

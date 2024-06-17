from pydantic import BaseModel
from .person import PersonInterface, ContactInterface, AddressInterface


class CorreoMensaje(BaseModel):
    person: PersonInterface
    contact: ContactInterface
    message: str


class Mensaje(BaseModel):
    subject: str
    messaje: str


class CorreoCotizacion(BaseModel):
    person: PersonInterface
    contact: ContactInterface
    address: AddressInterface
    objectCotizacion: str

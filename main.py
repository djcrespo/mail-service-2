import json

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.models import cotizaciones as cotiModels
from app.models import messages as messagesModels

from app.interfaces.person import *
from app.interfaces.mail import *

from app.services.services import *

from db import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os
import resend

app = FastAPI()

resend.api_key = os.environ["RESEND_API_KEY"]

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://example.com",
    # Agrega aquí los dominios que desees permitir
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ["ORIGINS"].split(" "),  # Permitir estos orígenes
    allow_credentials=True,  # Permitir el envío de cookies
    allow_methods=["*"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir estos headers
)


# Coneccion con la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


messagesModels.Base.metadata.create_all(bind=engine)
cotiModels.Base.metadata.create_all(bind=engine)


@app.post('/enviar-cotizacion')
def enviar_cotizacion(correoCotizacion: CorreoCotizacion, db: Session = Depends(get_db)):
    contact = correoCotizacion.contact
    person = correoCotizacion.person
    address = correoCotizacion.address
    object_cotizacion = json.loads(correoCotizacion.objectCotizacion)
    # print(object_cotizacion)
    typeOption = object_cotizacion['type']
    object_selectOption = json.loads(object_cotizacion['selectOption'])
    extra_info = json.loads(object_cotizacion['object'])

    # Guardar cotización
    db_coti = cotiModels.Cotizacion(
        type=object_cotizacion['type'],
        objeto_cotizado=object_selectOption,
        info_add=extra_info,
        person=json.loads(person.model_dump_json()),
        address=json.loads(address.model_dump_json()),
        contact=json.loads(contact.model_dump_json())
    )

    db.add(db_coti)
    db.commit()

    # Generar el contenido dinámico para extra_info
    extra_info_html = ''.join([f'<p><strong>{key}:</strong> {value}</p>' for key, value in extra_info.items()])

    template = f"""
                <h2>Información de contacto</h2>
                <p><strong>Nombre:</strong> {person.first_name} {person.last_name} </p>
                <p><strong>Correo electrónico:</strong> {contact.mail}</p>
                <p><strong>Teléfono:</strong> {contact.phone}</p>
                <br>
                <h3>Dirección de envío:</h3>
                <p><strong>Calle:</strong> {address.street}</p>
                <p><strong>Código postal:</strong> {address.postal_code}</p>
                <br>
                <h2>Solicitud de cotización de un {typeOption}:</h2>
                <p><strong>{object_selectOption['producto'] if 'producto' in object_selectOption else object_selectOption['servicio']} - {object_selectOption['tipo_producto'] if 'tipo_producto' in object_selectOption else object_selectOption['tipoDeServicio']}</strong></p>
                <p><strong>Condición de adquisición: </strong>{object_selectOption['condiciones_adquisicion'] if 'condiciones_adquisicion' in object_selectOption else ''}</p>
                <h3>Información extra:</h3>
                <p>{extra_info_html}</p>
                """

    send_cotizacion(template)


@app.post('/enviar-mensaje')
def enviar_msj(correoMensaje: CorreoMensaje, db: Session = Depends(get_db)):
    person_data = correoMensaje.person
    contact = correoMensaje.contact
    message = correoMensaje.message

    # Guardar mensaje
    db_mail = messagesModels.Mensajes(
        subject=contact.subject,
        message=message,
        person=json.loads(person_data.model_dump_json()),
        contact=json.loads(contact.model_dump_json())
    )

    db.add(db_mail)
    db.commit()

    # Template del correo
    template = f"""
            <h2>Información de contacto</h2>
            <p><strong>Nombre:</strong> {person_data.first_name} {person_data.last_name}</p>
            <p><strong>Correo electrónico:</strong> {contact.mail}</p>
            <p><strong>Teléfono:</strong> {contact.phone}</p>
            <h2>Mensaje</h2>
            <p>{message}</p>
            """

    send_message(template)

import threading
import time
from flask_mail import Message
from datetime import datetime, timedelta
from app import create_mail

mail = create_mail()

def mailRegister(email, username):
    msg = Message('Correo Registrado con exito', sender='mq583680@mail.com', recipients=[email])
    msg.body = f'su correo se ha registrado exitosamente en todo list, gracias por su preferencia {username}'
    mail.send(msg)
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


#instancia el controlador de la base de datos
db = SQLAlchemy()

#crea los parametros de la app
def create_app():
    #instancia flask
    app = Flask(__name__)
    
    #indica las configuraciones basicas de la app
    app.config.from_mapping(
        #para un debug automatico y no tener que reiniciar el servidor al realiazr un cambio
        DEBUG = True,
        #llave secreta para poder realizar peticiones, debe ser mas secreta, modularizada y protegida pero este es un ejemplo
        SECRET_KEY = 'xd',
        #concecta el controlador de la base de datos con la base de datos
        SQLALCHEMY_DATABASE_URI="sqlite:///todolist.db"
    )
    
    #inicializa la base de datos
    db.init_app(app)
    
    #inicializa los blueprint
    from . import todo
    app.register_blueprint(todo.bp)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    #crea la ruta inicial y le manda un archivo HTML de como debe ser
    @app.route('/')
    def index():
        return render_template('index.html')
    
    mail = Mail(app)
    
    #crea lo necesario para la base
    with app.app_context():
        db.create_all()
        
    #retorna la app para poder tabajar con ella
    return app


def create_mail():
    app = Flask(__name__)
    
    app.config.from_mapping(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = 'mq583680@gmail.com',
        MAIL_PASSWORD = '',
        MAIL_DEFAULT_SENDER = 'mq583680@gmail.com'
    )
    
    mail = Mail(app)
    
    return mail
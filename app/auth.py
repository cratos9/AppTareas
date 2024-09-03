from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from .models import User
from app import db
from .emails import mailRegister
from werkzeug.security import generate_password_hash, check_password_hash

#crea el bp 
bp = Blueprint('auth',__name__,url_prefix='/auth')

#crea una ruta y permite peticiones POST y GET
@bp.route('/register', methods = ('GET', 'POST'))
def register():
    #verifica que el motodo usado sea POST
    if request.method == 'POST':
        #obtiene datos del formulario del render
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        #crea un objeto usuario y cifra la contrasena
        user = User(username,generate_password_hash(password),email)
        #crea una variable error en caso que se ocurra uno
        error = None
        #busca las coincidencias del usuario
        user_name = User.query.filter_by(username = username).first()
        #si el usuario no existe
        if user_name == None:
            mailRegister(email,username)
            #crea el usuario y lo redirecciona al login
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            #indica que error es que ya existe un usuario
            error = f'El usuario {username} ya esta registrado'
        #muestra el error en caso de que alla uno
        flash(error)
    return render_template('auth/register.html')

#crea ua ruta y permite peticiones POST y GET
@bp.route('/login', methods = ('GET', 'POST'))
def login():
    #si el metodo usado es POST
    if request.method == 'POST':
        #obtiene los datos del formulario en el render
        username = request.form['username']
        password = request.form['password']
        
        #crea una variable error en caso de que alla uno
        error = None
        #busca el usuario
        user = User.query.filter_by(username = username).first()
        
        #si el usuario no existe
        if user == None:
            #indica a la varible error que el usuario no existe
            error = 'Nombre de usuario incorrecto'
        #o si no coincide la contrasena
        elif not check_password_hash(user.password, password):
            #indica a la varible eror que la contrasena es incorrecta
            error = 'Contrasena incorrecta'
        #si no hay errores
        if error == None:
            #borra la sesion anterior
            session.clear()
            #guarda el id del usuario
            session['user_id'] = user.id
            #nos redirecciona al index de la tareas
            return redirect(url_for('todo.index'))
        #muestra el error en caso de que alla
        flash(error)
    return render_template('auth/login.html')

@bp.route('/presentacion')
def presentacion():
    return render_template('auth/presentacion.html')

#con bp crea un decorador para despues de cada peticion
@bp.before_app_request
def load_logged_in_user():
    #obtiene el id del usuario
    user_id = session.get('user_id')
    #si el id es nada
    if user_id is None:
        #usuario es nada para todo
        g.user = None
    #si no
    else:
        #usuario es su id para todo
        g.user = User.query.get_or_404(user_id)
        
#crea una ruta para cuando se cierre la sesion
@bp.route('/logout')
def logout():
    #limpia la session y te manda al index
    session.clear()
    return redirect(url_for('index'))

import functools

#crea una funcion para que el usuario este loggeado obligatoriamente y si no lo esta te mande al login
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def get_user(id):
    user = User.query.get_or_404(id)
    return user

@bp.route('/actualizar', methods = ['POST','GET'])
@login_required
def actuaizar(id):
    user = get_user(id)
    
    #if request.method == 'POST':
    #user.username = request.form
    #user.email
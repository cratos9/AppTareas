from flask import Blueprint, render_template, request, redirect, url_for, g
from app.auth import login_required
from .models import Todo, User
from app import db

#inicia el blueprint, con su nombre y como se ve en el buscador
bp = Blueprint('todo',__name__,url_prefix='/todo')

#crea una ruta con el bp donde estara la lista de tareas
@bp.route('/list')
#verifica que el usuario este loggeado para entrar
@login_required
def index():
    #muestra todas las tareas del usuario
    todos = Todo.query.all()
    return render_template('todo/index.html', todos = todos)

#crea una pagina para la creacion de una nueva tarea y permite peticiones GET y POST con el bp
@bp.route('/create', methods=('GET','POST'))
#vefirica si esta loggeado al acceder el usuario
@login_required
def create():
    #verifica que el metodo utilizado sea POST
    if request.method == 'POST':
        #recupera la informacion enviada por el render 
        title = request.form['title']
        desc = request.form['desc']
        
        #crea un objeto con el id del usuario y lo obtenido de el formulario del render
        todo = Todo(g.user.id, title, desc)
        #guarda los cambios y los envia
        db.session.add(todo)
        db.session.commit()
        #retorna al index si todo salio bien
        return redirect(url_for('todo.index'))
    return render_template('todo/create.html')

#obtiene el id de la tarea
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo

#crea una tuta con peticiones POST y GRT
@bp.route('/update/<int:id>', methods=('GET','POST'))
#Se requiere un login para acceder
@login_required
def update(id):
    #obtiene el id del todo
    todo = get_todo(id)
    #verifica que el metodo utilizado sea POST
    if request.method == 'POST':
        #recupera la informacion enviada por el render 
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.state = True if request.form.get('state') == 'on' else False
        #envia los datos
        db.session.commit()
        #retorna al index si todo salio bien
        return redirect(url_for('todo.index'))
        
    return render_template('todo/update.html', todo = todo)

#crea una tuta con peticiones POST y GRT
@bp.route('/delete/<int:id>', methods=('GET','POST'))
#Se requiere un login para acceder
@login_required
def delete(id):
    #elimina la tarea en base en el ID
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))

@bp.route('/notificar/<int:id>', methods=['GET','POST'])
@login_required
def notificar(id):
    todo = get_todo(id)
    if request.method == 'POST':
        fecha = request.form['notificacion']
        correo = request.form['correo']
        print(fecha)
        #notificacion(todo, fecha, correo)
    return render_template('todo/notificar.html', todo = todo)
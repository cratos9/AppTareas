from app import db

#crea una clase que hereda lo requerido para mmenejas el controlador
class User(db.Model):
    #crea columnas con lo que tendra esa tabla y pasa sus configuraciones
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text,nullable = False, unique = True)
    
    #crea un constructor de la clase
    def __init__(self, username, password,email):
        self.username = username
        self.password = password
        self.email = email
        
    #crea como se debe reprenstar la clase
    def __repr__(self):
        return f'<User: {self.username}>'

#crea una clase que hereda lo requerido para manejar el controlador
class Todo(db.Model):
    #crea columnas con lo que tendra esa tabla y pasa sus configuraciones
    id = db.Column(db.Integer, primary_key = True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    title= db.Column(db.String(100), nullable = False)
    desc = db.Column(db.Text)
    state = db.Column(db.Boolean, default = False)
    
    #crea un contructor de la clase
    def __init__(self, create_by, title, desc, state=False):
        self.created_by = create_by
        self.title = title
        self.desc = desc
        self.state = state
        
    #crea como se debe reprenstar la clase
    def __repr__(self):
        return f'<Todo: {self.title}>'
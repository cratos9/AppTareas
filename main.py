from app import create_app

app = create_app()
#inicializa la aplicacion y la crea segun los parrametros pasados por el modulo importado
if __name__ == '__main__':
    app.run()
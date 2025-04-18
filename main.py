from flask import Flask, render_template
from models.database import db, User
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
from routes.auth import auth  # Importación correcta
from routes.dashboard import dashboard  # Importar el nuevo blueprint
from routes.memory import memory  # Importamos el blueprint
from routes.attention import attention
from routes.reasoning import reasoning




app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)  # Inicializar bcrypt

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@app.route('/')
def home():
    return render_template('index.html')  # Ruta para la página de inicio

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Cargar usuario desde la base de datos

app.register_blueprint(auth)  # Registro del Blueprint de autenticación
app.register_blueprint(dashboard)  # Registro del Blueprint del dashboard
app.register_blueprint(memory)  # Registramos los ejercicios de memoria
app.register_blueprint(attention) # Registramos los ejercicios de atencion
app.register_blueprint(reasoning) # Registramos los ejercicios de razonamiento




if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crear la base de datos si no existe
    app.run(debug=True)
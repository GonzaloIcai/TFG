from flask import Flask, render_template
from models.database import db, User
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
from routes.auth import auth  
from routes.dashboard import dashboard  
from routes.memory import memory  
from routes.attention import attention
from routes.reasoning import reasoning
from routes.memory_digits import memory_digits
from routes.attention_stroop import attention_stroop
from routes.reasoning_raven import reasoning_raven
from routes.analysis import analysis
from routes.perfil import perfil
from routes.graficos import graficos
from routes.historial import historial

from routes.analysis_simulados import analysis_simulados

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)  

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.logout_view = "home"

@app.route('/')
def home():
    return render_template('index.html')  # Ruta para la página de inicio

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Cargar usuario desde la base de datos

app.register_blueprint(auth)                # Registro del Blueprint de autenticación
app.register_blueprint(dashboard)           # Registro del Blueprint del dashboard
app.register_blueprint(analysis)            # Registro del Blueprint del analysis
app.register_blueprint(memory)              # Registramos los ejercicios de memoria
app.register_blueprint(attention)           # Registramos los ejercicios de atencion
app.register_blueprint(reasoning)           # Registramos los ejercicios de razonamiento
app.register_blueprint(memory_digits)       # Registramos los ejercicios de memoria  
app.register_blueprint(attention_stroop)    # Registramos los ejercicios de atencion
app.register_blueprint(reasoning_raven)   # Registramos los ejercicios de atencion
app.register_blueprint(perfil)
app.register_blueprint(graficos)
app.register_blueprint(historial)

app.register_blueprint(analysis_simulados)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creo la base de datos si no existe
    app.run(debug=True)





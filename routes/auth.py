from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from models.database import db, User

bcrypt = Bcrypt()

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Verificar si ya existe un usuario con ese email
        user_existente = User.query.filter_by(email=email).first()
        if user_existente:
            flash("⚠️ El correo electrónico ya está registrado. Prueba con otro.", "danger")
            return redirect(url_for('auth.register'))

        # Verificar que la contraseña tenga mínimo 6 caracteres
        if len(password) < 6:
            flash("⚠️ La contraseña debe tener al menos 6 caracteres.", "danger")
            return redirect(url_for('auth.register'))

        # Si todo está correcto, crear el nuevo usuario
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("✅ Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard.user_dashboard'))

        flash("Usuario o contraseña incorrectos", "auth_error")

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

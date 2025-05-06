from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_bcrypt import check_password_hash, generate_password_hash
from models.database import db

perfil = Blueprint('perfil', __name__)

@perfil.route('/perfil')
@login_required
def ver_perfil():
    return render_template('perfil.html', user=current_user)

@perfil.route('/editar-nombre', methods=['POST'])
@login_required
def editar_nombre():
    nuevo_nombre = request.form['new_username']
    if nuevo_nombre:
        current_user.username = nuevo_nombre
        db.session.commit()
        flash("Nombre de usuario actualizado.", "perfil_success")
    return redirect(url_for('perfil.ver_perfil'))

@perfil.route('/cambiar-password', methods=['POST'])
@login_required
def cambiar_password():
    actual = request.form['current_password']
    nueva = request.form['new_password']
    confirmar = request.form['confirm_password']

    # Verificar la contraseña actual
    if not check_password_hash(current_user.password, actual):
        flash("❌ La contraseña actual es incorrecta.", "perfil_error")
        return redirect(url_for('perfil.ver_perfil'))

    # Verificar que la nueva y confirmación sean iguales
    if nueva != confirmar:
        flash("⚠️ La nueva contraseña y la confirmación no coinciden.", "perfil_warning")
        return redirect(url_for('perfil.ver_perfil'))

    # (opcional) Verificar que no esté vacía o sea demasiado corta
    if len(nueva) < 6:
        flash("⚠️ La nueva contraseña debe tener al menos 6 caracteres.", "perfil_warning")
        return redirect(url_for('perfil.ver_perfil'))

    # Actualizar contraseña
    current_user.password = generate_password_hash(nueva).decode('utf-8')
    db.session.commit()
    flash("✅ Contraseña actualizada correctamente.", "perfil_success")
    return redirect(url_for('perfil.ver_perfil'))

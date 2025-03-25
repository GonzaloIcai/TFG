from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.database import MemoryResult  # Importamos el modelo de resultados

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def user_dashboard():
    results = MemoryResult.query.filter_by(user_id=current_user.id).order_by(MemoryResult.timestamp.desc()).limit(5).all()
    return render_template('dashboard.html', user=current_user, results=results)

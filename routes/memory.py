from flask import Blueprint, render_template
from flask_login import login_required

memory = Blueprint('memory', __name__)

@memory.route('/memory')
@login_required
def memory_game():
    return render_template('memory.html')

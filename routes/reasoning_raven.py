from flask import Blueprint, render_template
from flask_login import login_required

reasoning_raven = Blueprint('reasoning_raven', __name__)

@reasoning_raven.route('/reasoning/raven')
@login_required
def raven_game():
    return render_template('reasoning/reasoning_raven.html')

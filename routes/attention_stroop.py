from flask import Blueprint, render_template
from flask_login import login_required

attention_stroop = Blueprint('attention_stroop', __name__)

@attention_stroop.route('/attention/stroop')
@login_required
def stroop_game():
    return render_template('attention_stroop.html')

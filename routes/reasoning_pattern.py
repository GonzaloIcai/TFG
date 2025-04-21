from flask import Blueprint, render_template
from flask_login import login_required

reasoning_pattern = Blueprint('reasoning_pattern', __name__)

@reasoning_pattern.route('/reasoning/pattern')
@login_required
def pattern_game():
    return render_template('reasoning_pattern.html')

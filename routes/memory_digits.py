from flask import Blueprint, render_template
from flask_login import login_required

memory_digits = Blueprint('memory_digits', __name__)

@memory_digits.route('/memory/digits')
@login_required
def digits_game():
    return render_template("memory/memory_digits.html")

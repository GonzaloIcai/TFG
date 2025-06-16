from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.database import MemoryResult, db

memory_digits = Blueprint('memory_digits', __name__)

@memory_digits.route('/memory/digits')
@login_required
def digits_game():
    return render_template("memory/memory_digits.html")

@memory_digits.route('/memory/save', methods=['POST'])
@login_required
def save_digits_result():
    data = request.get_json()
    time_spent = data.get('time_spent')
    attempts = data.get('attempts')

    if time_spent is None or attempts is None:
        return jsonify({"status": "error", "message": "Datos incompletos"}), 400

    result = MemoryResult(
        user_id=current_user.id,
        time_spent=time_spent,
        attempts=attempts
    )
    db.session.add(result)
    db.session.commit()
    return jsonify({"status": "success"})

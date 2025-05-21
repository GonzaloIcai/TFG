from flask import Blueprint, render_template
from flask_login import login_required
from flask import request, jsonify
from models.database import MemoryResult, db
from flask_login import current_user

memory = Blueprint('memory', __name__)

@memory.route('/memory')
@login_required
def memory_game():
    return render_template('memory/memory.html')


@memory.route('/memory/save', methods=['POST'])
@login_required
def save_memory_result():
    data = request.get_json()
    time_spent = data.get('time_spent')
    attempts = data.get('attempts')

    result = MemoryResult(
        user_id=current_user.id,
        time_spent=time_spent,
        attempts=attempts
    )
    db.session.add(result)
    db.session.commit()
    return jsonify({"status": "success"})
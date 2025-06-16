from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.database import ReasoningResult, db
from datetime import datetime

reasoning_raven = Blueprint('reasoning_raven', __name__)

@reasoning_raven.route('/reasoning/raven')
@login_required
def raven_game():
    return render_template('reasoning/reasoning_raven.html')

@reasoning_raven.route('/reasoning/raven/save', methods=['POST'])
@login_required
def save_raven_result():
    data = request.get_json()
    correct = data.get('correct')
    incorrect = data.get('incorrect')
    time_spent = data.get('time_spent')

    result = ReasoningResult(
        user_id=current_user.id,
        correct=correct,
        incorrect=incorrect,
        time_spent=time_spent,
        timestamp=datetime.utcnow()
    )
    db.session.add(result)
    db.session.commit()
    return jsonify({"status": "success"})

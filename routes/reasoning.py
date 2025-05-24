from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.database import ReasoningResult, db

reasoning = Blueprint('reasoning', __name__)

@reasoning.route('/reasoning')
@login_required
def reasoning_game():
    return render_template('reasoning/reasoning.html')

@reasoning.route('/reasoning/save', methods=['POST'])
@login_required
def save_reasoning_result():
    data = request.get_json()
    correct = data.get('correct')
    incorrect = data.get('incorrect')
    time_spent = data.get('time_spent')

    result = ReasoningResult(
        user_id=current_user.id,
        correct=correct,
        incorrect=incorrect,
        time_spent=time_spent
    )
    db.session.add(result)
    db.session.commit()
    return jsonify({"status": "success"})

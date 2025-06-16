from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.database import AttentionResult, db

attention_stroop = Blueprint('attention_stroop', __name__)

@attention_stroop.route('/attention/stroop')
@login_required
def stroop_game():
    return render_template('attention/attention_stroop.html')

@attention_stroop.route('/attention/stroop/save', methods=['POST'])
@login_required
def save_stroop_result():
    data = request.get_json()
    average_time = data.get('average_time')
    errors = data.get('errors')
    rounds_completed = data.get('rounds_completed')

    result = AttentionResult(
        user_id=current_user.id,
        average_time=average_time,
        errors=errors,
        rounds_completed=rounds_completed
    )
    db.session.add(result)
    db.session.commit()
    return jsonify({"status": "success"})

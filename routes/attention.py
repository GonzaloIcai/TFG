from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.database import AttentionResult, db

attention = Blueprint('attention', __name__)  # ✅ Definimos el blueprint

@attention.route('/attention')
@login_required
def attention_game():
    return render_template('attention/attention.html')

@attention.route('/attention/save', methods=['POST'])
@login_required
def save_attention_result():
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

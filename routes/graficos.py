from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.database import db, MemoryResult, AttentionResult, ReasoningResult
from sqlalchemy import func
from datetime import datetime

graficos = Blueprint('graficos', __name__)

@graficos.route('/graficos')
@login_required
def ver_graficos():
    user_id = current_user.id

    # === MEMORIA ===
    memoria_data = db.session.query(
        func.date(MemoryResult.timestamp),
        func.avg(MemoryResult.attempts)
    ).filter_by(user_id=user_id).group_by(func.date(MemoryResult.timestamp)).all()

    memoria_labels = [datetime.strptime(row[0], "%Y-%m-%d").strftime("%d-%b") for row in memoria_data]
    memoria_errores = [round(row[1], 2) for row in memoria_data]

    # === ATENCIÓN ===
    atencion_data = db.session.query(
        func.date(AttentionResult.timestamp),
        func.avg(AttentionResult.errors)
    ).filter_by(user_id=user_id).group_by(func.date(AttentionResult.timestamp)).all()

    atencion_labels = [datetime.strptime(row[0], "%Y-%m-%d").strftime("%d-%b") for row in atencion_data]
    atencion_errores = [round(row[1], 2) for row in atencion_data]

    # === RAZONAMIENTO ===
    razonamiento_data = db.session.query(
        func.date(ReasoningResult.timestamp),
        func.avg(ReasoningResult.incorrect)
    ).filter_by(user_id=user_id).group_by(func.date(ReasoningResult.timestamp)).all()

    razonamiento_labels = [datetime.strptime(row[0], "%Y-%m-%d").strftime("%d-%b") for row in razonamiento_data]
    razonamiento_errores = [round(row[1], 2) for row in razonamiento_data]

    return render_template(
        'graficos.html',
        memoria_labels=memoria_labels,
        memoria_errores=memoria_errores,
        atencion_labels=atencion_labels,
        atencion_errores=atencion_errores,
        razonamiento_labels=razonamiento_labels,
        razonamiento_errores=razonamiento_errores
    )

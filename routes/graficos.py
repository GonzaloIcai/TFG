from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.database import db, MemoryResult, AttentionResult, ReasoningResult
from sqlalchemy import func

graficos = Blueprint('graficos', __name__)

@graficos.route('/graficos')
@login_required
def ver_graficos():
    user_id = current_user.id

    # MEMORIA
    memoria_data = db.session.query(
        func.date(MemoryResult.timestamp),
        func.avg(MemoryResult.attempts),
        func.avg(MemoryResult.time_spent)
    ).filter_by(user_id=user_id).group_by(func.date(MemoryResult.timestamp)).all()

    memoria_labels = [str(row[0]) for row in memoria_data]
    memoria_intentos = [round(row[1], 2) for row in memoria_data]
    memoria_tiempo = [round(row[2], 2) for row in memoria_data]

    # ATENCION
    atencion_data = db.session.query(
        func.date(AttentionResult.timestamp),
        func.avg(AttentionResult.errors),
        func.avg(AttentionResult.average_time),
        func.avg(AttentionResult.rounds_completed)
    ).filter_by(user_id=user_id).group_by(func.date(AttentionResult.timestamp)).all()

    atencion_labels = [str(row[0]) for row in atencion_data]
    atencion_errores = [round(row[1], 2) for row in atencion_data]
    atencion_promedio = [round(row[2], 2) for row in atencion_data]
    atencion_rondas = [round(row[3], 2) for row in atencion_data]

    # RAZONAMIENTO
    razonamiento_data = db.session.query(
        func.date(ReasoningResult.timestamp),
        func.avg(ReasoningResult.correct),
        func.avg(ReasoningResult.incorrect),
        func.avg(ReasoningResult.time_spent)
    ).filter_by(user_id=user_id).group_by(func.date(ReasoningResult.timestamp)).all()

    razonamiento_labels = [str(row[0]) for row in razonamiento_data]
    razonamiento_correctas = [round(row[1], 2) for row in razonamiento_data]
    razonamiento_incorrectas = [round(row[2], 2) for row in razonamiento_data]
    razonamiento_tiempo = [round(row[3], 2) for row in razonamiento_data]

    return render_template(
        'graficos.html',
        memoria_labels=memoria_labels,
        memoria_intentos=memoria_intentos,
        memoria_tiempo=memoria_tiempo,
        atencion_labels=atencion_labels,
        atencion_errores=atencion_errores,
        atencion_promedio=atencion_promedio,
        atencion_rondas=atencion_rondas,
        razonamiento_labels=razonamiento_labels,
        razonamiento_correctas=razonamiento_correctas,
        razonamiento_incorrectas=razonamiento_incorrectas,
        razonamiento_tiempo=razonamiento_tiempo
    )

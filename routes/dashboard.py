from flask import Blueprint, render_template, redirect, url_for, session, jsonify
from flask_login import login_required, current_user
from models.database import MemoryResult, AttentionResult, ReasoningResult, db
from datetime import datetime, date
import itertools

dashboard = Blueprint('dashboard', __name__)

# Generadores rotativos para cada categoría
memoria_juegos = itertools.cycle([
    ('memory.memory_game', "Juego de Memoria"),
    ('memory_digits.digits_game', "Series de Dígitos")
])

atencion_juegos = itertools.cycle([
    ('attention.attention_game', "Encuentra el Diferente"),
    ('attention_stroop.stroop_game', "Stroop Simplificado")
])

razonamiento_juegos = itertools.cycle([
    ('reasoning.reasoning_game', "Serie Numérica"),
    ('reasoning_raven.raven_game', "Adivina el Patrón Visual")
])

@dashboard.route('/dashboard')
@login_required
def user_dashboard():
    user_id = current_user.id
    today = date.today()

    # ✅ Comprobar si el usuario ya jugó hoy en cada categoría
    memoria_jugada = MemoryResult.query.filter_by(user_id=user_id).filter(db.func.date(MemoryResult.timestamp) == today).count() > 0
    atencion_jugada = AttentionResult.query.filter_by(user_id=user_id).filter(db.func.date(AttentionResult.timestamp) == today).count() > 0
    razonamiento_jugada = ReasoningResult.query.filter_by(user_id=user_id).filter(db.func.date(ReasoningResult.timestamp) == today).count() > 0

    completados_hoy = memoria_jugada and atencion_jugada and razonamiento_jugada

    return render_template('dashboard.html',
                           user=current_user,
                           memoria_jugada=memoria_jugada,
                           atencion_jugada=atencion_jugada,
                           razonamiento_jugada=razonamiento_jugada,
                           completados_hoy=completados_hoy)

@dashboard.route('/jugar/memoria')
@login_required
def jugar_memoria():
    ruta, _ = next(memoria_juegos)
    return redirect(url_for(ruta))

@dashboard.route('/jugar/atencion')
@login_required
def jugar_atencion():
    ruta, _ = next(atencion_juegos)
    return redirect(url_for(ruta))

@dashboard.route('/jugar/razonamiento')
@login_required
def jugar_razonamiento():
    ruta, _ = next(razonamiento_juegos)
    return redirect(url_for(ruta))

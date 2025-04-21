from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required, current_user
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
    ('reasoning_pattern.pattern_game', "Adivina el Patrón Visual")
])

@dashboard.route('/dashboard')
@login_required
def user_dashboard():
    return render_template('dashboard.html', user=current_user)

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

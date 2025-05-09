from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from models.database import db, MemoryResult, AttentionResult, ReasoningResult, Informe
from datetime import datetime, timedelta
import openai
import os

analysis = Blueprint('analysis', __name__)

# ✅ Configuración segura de la API Key desde variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI()

# Función para construir el prompt a partir del JSON generado
def construir_prompt(json_data):
    prompt = f"""
Eres un neuropsicólogo experto en detección temprana de deterioro cognitivo.
Analiza los resultados semanales de ejercicios cognitivos de un usuario mayor.

Debes:
1. Evaluar el rendimiento general en memoria, atención y razonamiento
2. Detectar patrones de mejora o empeoramiento
3. Sugerir ajustes de dificultad para cada tipo de ejercicio
4. Indicar si hay señales tempranas de deterioro cognitivo leve (sin diagnosticar)

Datos del usuario del {json_data['semana_del']} al {json_data['semana_hasta']}:

Memoria:
{json_data['memoria']}

Atención:
{json_data['atencion']}

Razonamiento:
{json_data['razonamiento']}

Redacta un informe empático, directo y claro. Usa lenguaje entendible para familiares o cuidadores.
"""
    return prompt.strip()

# Función para consultar la API de OpenAI con el prompt generado
def generar_analisis_gpt(prompt):
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un neuropsicólogo experto en evaluación cognitiva."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return respuesta.choices[0].message.content

# Ruta que genera el JSON de resultados + análisis GPT (semana actual)
@analysis.route('/generar_informe')
@login_required
def generar_informe_semanal():
    usuario_id = current_user.id
    hoy = datetime.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    domingo = lunes + timedelta(days=6)

    memoria = MemoryResult.query.filter(
        MemoryResult.user_id == usuario_id,
        MemoryResult.timestamp >= lunes,
        MemoryResult.timestamp <= domingo
    ).all()

    atencion = AttentionResult.query.filter(
        AttentionResult.user_id == usuario_id,
        AttentionResult.timestamp >= lunes,
        AttentionResult.timestamp <= domingo
    ).all()

    razonamiento = ReasoningResult.query.filter(
        ReasoningResult.user_id == usuario_id,
        ReasoningResult.timestamp >= lunes,
        ReasoningResult.timestamp <= domingo
    ).all()

    informe = {
        "usuario_id": usuario_id,
        "semana_del": lunes.strftime("%Y-%m-%d"),
        "semana_hasta": domingo.strftime("%Y-%m-%d"),
        "memoria": [
            {"fecha": r.timestamp.strftime("%Y-%m-%d"), "intentos": r.attempts, "tiempo": r.time_spent} for r in memoria
        ],
        "atencion": [
            {"fecha": r.timestamp.strftime("%Y-%m-%d"), "errores": r.errors, "promedio_tiempo": r.average_time, "rondas": r.rounds_completed} for r in atencion
        ],
        "razonamiento": [
            {"fecha": r.timestamp.strftime("%Y-%m-%d"), "correctas": r.correct, "incorrectas": r.incorrect, "tiempo": r.time_spent} for r in razonamiento
        ]
    }

    prompt = construir_prompt(informe)
    informe_gpt = generar_analisis_gpt(prompt)

    # Guardar en la base de datos
    nuevo_informe = Informe(
        user_id=current_user.id,
        contenido=informe_gpt,
        fecha=datetime.now()
    )
    db.session.add(nuevo_informe)
    db.session.commit()

    return jsonify({
        "datos": informe,
        "informe": informe_gpt
    })

# Generar informe desde el último
@analysis.route('/generar_informe_desde_ultimo')
@login_required
def generar_informe_desde_ultimo():
    usuario = current_user
    desde_fecha = usuario.last_report or datetime(2000, 1, 1)
    hasta_fecha = datetime.now()

    memoria = MemoryResult.query.filter(
        MemoryResult.user_id == usuario.id,
        MemoryResult.timestamp >= desde_fecha,
        MemoryResult.timestamp <= hasta_fecha
    ).all()

    atencion = AttentionResult.query.filter(
        AttentionResult.user_id == usuario.id,
        AttentionResult.timestamp >= desde_fecha,
        AttentionResult.timestamp <= hasta_fecha
    ).all()

    razonamiento = ReasoningResult.query.filter(
        ReasoningResult.user_id == usuario.id,
        ReasoningResult.timestamp >= desde_fecha,
        ReasoningResult.timestamp <= hasta_fecha
    ).all()

    informe = {
        "usuario_id": usuario.id,
        "semana_del": desde_fecha.strftime("%Y-%m-%d %H:%M"),
        "semana_hasta": hasta_fecha.strftime("%Y-%m-%d %H:%M"),
        "memoria": [
            {"fecha": r.timestamp.strftime("%Y-%m-%d"), "intentos": r.attempts, "tiempo": r.time_spent} for r in memoria
        ],
        "atencion": [
            {"fecha": r.timestamp.strftime("%Y-%m-%d"), "errores": r.errors, "promedio_tiempo": r.average_time, "rondas": r.rounds_completed} for r in atencion
        ],
        "razonamiento": [
            {"fecha": r.timestamp.strftime("%Y-%m-%d"), "correctas": r.correct, "incorrectas": r.incorrect, "tiempo": r.time_spent} for r in razonamiento
        ]
    }

    prompt = construir_prompt(informe)
    analisis = generar_analisis_gpt(prompt)

    # Guardar en la base de datos
    nuevo_informe = Informe(
        user_id=current_user.id,
        contenido=analisis,
        fecha=datetime.now()
    )
    db.session.add(nuevo_informe)
    db.session.commit()

    usuario.last_report = hasta_fecha
    db.session.commit()

    return jsonify({
        "datos": informe,
        "informe": analisis
    })

@analysis.route('/informe-vista')
@login_required
def informe_en_pantalla():
    usuario = current_user
    desde_fecha = usuario.last_report or datetime(2000, 1, 1)
    hasta_fecha = datetime.now()

    memoria = MemoryResult.query.filter(
        MemoryResult.user_id == usuario.id,
        MemoryResult.timestamp >= desde_fecha,
        MemoryResult.timestamp <= hasta_fecha
    ).all()

    atencion = AttentionResult.query.filter(
        AttentionResult.user_id == usuario.id,
        AttentionResult.timestamp >= desde_fecha,
        AttentionResult.timestamp <= hasta_fecha
    ).all()

    razonamiento = ReasoningResult.query.filter(
        ReasoningResult.user_id == usuario.id,
        ReasoningResult.timestamp >= desde_fecha,
        ReasoningResult.timestamp <= hasta_fecha
    ).all()

    informe = {
        "usuario_id": usuario.id,
        "semana_del": desde_fecha.strftime("%Y-%m-%d %H:%M"),
        "semana_hasta": hasta_fecha.strftime("%Y-%m-%d %H:%M"),
        "memoria": [
            {"fecha": r.timestamp.strftime("%Y-%m-%d"), "intentos": r.attempts, "tiempo": r.time_spent} for r in memoria
        ],
        "atencion": [
            {"fecha": r.timestamp.strftime("%Y-%m-%d"), "errores": r.errors, "promedio_tiempo": r.average_time, "rondas": r.rounds_completed} for r in atencion
        ],
        "razonamiento": [
            {"fecha": r.timestamp.strftime("%Y-%m-%d"), "correctas": r.correct, "incorrectas": r.incorrect, "tiempo": r.time_spent} for r in razonamiento
        ]
    }

    prompt = construir_prompt(informe)
    analisis = generar_analisis_gpt(prompt)

    # Guardar en la base de datos
    nuevo_informe = Informe(
        user_id=current_user.id,
        contenido=analisis,
        fecha=datetime.now()
    )
    db.session.add(nuevo_informe)
    db.session.commit()

    usuario.last_report = hasta_fecha
    db.session.commit()

    return render_template("informe.html", informe=analisis, desde=desde_fecha, hasta=hasta_fecha)

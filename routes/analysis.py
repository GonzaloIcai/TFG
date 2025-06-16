from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from models.database import db, MemoryResult, AttentionResult, ReasoningResult, Informe
from datetime import datetime, timedelta
import openai
import os
import markdown

analysis = Blueprint('analysis', __name__)

# Configuración segura de la API Key desde variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI()

# Función para construir el prompt a partir del JSON generado
def construir_prompt(json_data):
    prompt = f"""
Eres un neuropsicólogo especializado en envejecimiento cognitivo y desarrollo de planes personalizados de estimulación. Tu tarea es analizar los resultados de un usuario mayor que ha estado realizando ejercicios cognitivos en tres áreas: memoria, atención y razonamiento.

Usa los datos semanales proporcionados a continuación para:

1. Evaluar la evolución del rendimiento del usuario en cada tipo de ejercicio (memoria, atención y razonamiento), observando tendencias positivas, negativas o estancamiento.
2. Detectar si hay alguna diferencia significativa entre áreas (por ejemplo, si mejora en memoria pero empeora en atención).
3. Comentar si se observan días especialmente buenos o malos, inestabilidad o progresión constante.
4. Emitir una conclusión general sobre el rendimiento cognitivo del usuario durante esta semana.
5. Redactar recomendaciones personalizadas para continuar con el progreso o corregir retrocesos. Estas recomendaciones pueden incluir:
   - ajustes de dificultad
   - ejercicios complementarios
   - hábitos saludables que favorezcan el rendimiento cognitivo
6. (Opcional) Si observas un patrón que sugiera deterioro cognitivo leve (por ejemplo, empeoramiento sostenido en más de una área), indícalo con tacto, sin alarmismo.

**Tono del informe:** claro, empático y profesional. El texto debe ser entendible para un familiar o cuidador, sin tecnicismos. Evita frases genéricas: haz que el informe parezca redactado para este usuario en concreto.

Resultados del usuario del {json_data['semana_del']} al {json_data['semana_hasta']}:

🧠 Memoria:
{json_data['memoria']}

👁 Atención:
{json_data['atencion']}

🔍 Razonamiento:
{json_data['razonamiento']}
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
    lunes = datetime(2025, 5, 1)
    domingo = datetime(2025, 5, 31, 23, 59, 59)

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
    informe_html = markdown.markdown(informe_gpt)

    nuevo_informe = Informe(
        user_id=current_user.id,
        contenido=informe_html,
        fecha=datetime.now()
    )
    db.session.add(nuevo_informe)
    db.session.commit()

    return jsonify({
        "datos": informe,
        "informe": informe_html
    })

# Generar informe desde el último
@analysis.route('/generar_informe_desde_ultimo')
@login_required
def generar_informe_desde_ultimo():
    usuario = current_user
    desde_fecha = datetime(2025, 5, 1)
    hasta_fecha = datetime(2025, 5, 31, 23, 59, 59)

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
    analisis_html = markdown.markdown(analisis)

    nuevo_informe = Informe(
        user_id=current_user.id,
        contenido=analisis_html,
        fecha=datetime.now()
    )
    db.session.add(nuevo_informe)
    db.session.commit()

    usuario.last_report = hasta_fecha
    db.session.commit()

    return jsonify({
        "datos": informe,
        "informe": analisis_html
    })

@analysis.route('/informe-vista')
@login_required
def informe_en_pantalla():
    usuario = current_user
    desde_fecha = datetime(2025, 5, 1)
    hasta_fecha = datetime(2025, 5, 31, 23, 59, 59)

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
    analisis_html = markdown.markdown(analisis)

    nuevo_informe = Informe(
        user_id=current_user.id,
        contenido=analisis_html,
        fecha=datetime.now()
    )
    db.session.add(nuevo_informe)
    db.session.commit()

    usuario.last_report = hasta_fecha
    db.session.commit()

    return render_template("informe.html", informe=analisis_html, desde=desde_fecha, hasta=hasta_fecha)

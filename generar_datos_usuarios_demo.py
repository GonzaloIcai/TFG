from models.database import db, User, MemoryResult, AttentionResult, ReasoningResult
from datetime import datetime
from random import randint, uniform
from main import app

def generar_datos_fake(user_email, patron):
    patrones_validos = [
        'mejora', 
        'empeora', 
        'neutro', 
        'empeora_memoria_solo', 
        'empeora_atencion_solo', 
        'empeora_razonamiento_solo'
    ]
    if patron not in patrones_validos:
        print(f"❌ Patrón inválido. Usa uno de: {patrones_validos}")
        return

    with app.app_context():
        usuario = User.query.filter_by(email=user_email).first()
        if not usuario:
            print(f"❌ Usuario {user_email} no encontrado. Skipping.")
            return

        # Limpiar datos del 1 al 31 de mayo
        inicio = datetime(2025, 5, 1)
        fin = datetime(2025, 5, 31, 23, 59, 59)

        MemoryResult.query.filter(MemoryResult.user_id == usuario.id, MemoryResult.timestamp.between(inicio, fin)).delete()
        AttentionResult.query.filter(AttentionResult.user_id == usuario.id, AttentionResult.timestamp.between(inicio, fin)).delete()
        ReasoningResult.query.filter(ReasoningResult.user_id == usuario.id, ReasoningResult.timestamp.between(inicio, fin)).delete()

        for dia in range(1, 32):
            fecha = datetime(2025, 5, dia)
            i = dia - 1

            if patron == 'mejora':
                base_attempts = max(1, 12 - i * 0.3)
                attempts = int(base_attempts + uniform(-1, 1))

                base_attention = max(0, 8 - i * 0.2)
                attention_errors = int(max(0, base_attention + uniform(-1, 1)))

                base_reasoning = max(0, 5 - i * 0.2)
                reasoning_wrong = int(max(0, base_reasoning + uniform(-1, 1)))

                time_spent = round(90 - i * 1.3 + uniform(-5, 5), 2)
                average_time = round(5 - i * 0.08 + uniform(-0.3, 0.3), 2)
                rounds_completed = min(5, max(3, 3 + i // 10 + randint(-1, 1)))

            elif patron == 'empeora':
                base_attempts = min(20, 5 + i * 0.4)
                attempts = int(base_attempts + uniform(-1, 1))

                base_attention = min(10, 2 + i * 0.25)
                attention_errors = int(min(10, base_attention + uniform(-1, 1)))

                base_reasoning = min(4, 1 + i * 0.15)
                reasoning_wrong = int(min(4, base_reasoning + uniform(-1, 1)))

                time_spent = round(60 + i * 2.2 + uniform(-5, 5), 2)
                average_time = round(2 + i * 0.08 + uniform(-0.3, 0.3), 2)
                rounds_completed = max(1, 5 - i // 10 + randint(-1, 0))

            elif patron == 'neutro':
                attempts = randint(8, 12)

                attention_errors = randint(2, 4)

                reasoning_wrong = randint(1, 2)

                time_spent = round(uniform(75, 85), 2)
                average_time = round(uniform(3.0, 3.5), 2)
                rounds_completed = randint(3, 5)


            elif patron == 'empeora_memoria_solo':
                base_attempts = min(20, 5 + i * 0.4)
                attempts = int(base_attempts + uniform(-1, 1))

                attention_errors = 3

                reasoning_wrong = 1

                time_spent = round(60 + i * 2.2 + uniform(-5, 5), 2)
                average_time = 3
                rounds_completed = 5
                

            elif patron == 'empeora_atencion_solo':
                attempts = randint(8, 11)
               
                base_attention = min(10, 2 + i * 0.25)
                attention_errors = int(min(10, base_attention + uniform(-1, 1)))

                reasoning_wrong = 1

                time_spent = round(uniform(70, 85), 2)
                average_time = round(2 + i * 0.08 + uniform(-0.3, 0.3), 2)
                rounds_completed = max(1, 5 - i // 10 + randint(-1, 0))
                

            elif patron == 'empeora_razonamiento_solo':
                attempts = randint(8, 11)

                attention_errors = 3

                base_reasoning = min(4, 1 + i * 0.15)
                reasoning_wrong = int(min(4, base_reasoning + uniform(-0.5, 0.5)))

                time_spent = round(uniform(70, 85), 2)
                average_time = 3
                rounds_completed = 5

            db.session.add(MemoryResult(
                user_id=usuario.id,
                time_spent=time_spent,
                attempts=attempts,
                timestamp=fecha
            ))

            db.session.add(AttentionResult(
                user_id=usuario.id,
                average_time=average_time,
                errors=attention_errors,
                rounds_completed=rounds_completed,
                timestamp=fecha
            ))

            db.session.add(ReasoningResult(
                user_id=usuario.id,
                correct=4 - reasoning_wrong,
                incorrect=reasoning_wrong,
                time_spent=round(uniform(15, 40), 2),
                timestamp=fecha
            ))

        db.session.commit()
        print(f"✅ {user_email} - patrón '{patron}' generado correctamente.")

# ==== EJECUCIÓN DE LOS CASOS CLAVE DEL TFG ====
if __name__ == "__main__":
    usuarios_y_patrones = [
        ("caso_mejora_global@test.com", "mejora"),
        ("caso_empeora_global@test.com", "empeora"),
        ("caso_neutro@test.com", "neutro"),
        ("caso_empeora_memoria@test.com", "empeora_memoria_solo"),
        ("caso_empeora_atencion@test.com", "empeora_atencion_solo"),
        ("caso_empeora_razonamiento@test.com", "empeora_razonamiento_solo")
    ]

    for email, patron in usuarios_y_patrones:
        generar_datos_fake(email, patron)

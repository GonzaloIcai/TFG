from main import app, db
from models.database import Informe
from datetime import datetime

# ID del usuario que tendrá estos informes (ajústalo si no es 1)
user_id = 1

fechas = [
    datetime(2025, 1, 1),
    datetime(2025, 2, 1),
    datetime(2025, 3, 1),
    datetime(2025, 4, 1),
    datetime(2025, 5, 1),
    datetime(2025, 6, 1),
]

contenido = "Informe generado automáticamente para mostrar en el historial del usuario."

with app.app_context():
    for fecha in fechas:
        informe = Informe(user_id=user_id, contenido=contenido, fecha=fecha)
        db.session.add(informe)
    db.session.commit()
    print("✅ Informes simulados creados correctamente.")



if __name__ == "__main__":
    usuarios_y_patrones = [
        ("caso_mejora_global@test.com", "mejora"),
        ("caso_empeora_global@test.com", "empeora"),
        ("caso_empeora_atencion@test.com", "empeora_atencion_solo"),
    ]
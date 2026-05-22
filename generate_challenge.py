import firebase_admin
from firebase_admin import credentials, firestore
import random
import json
import os
from datetime import datetime, timedelta

# Cargar credenciales desde variable de entorno
service_account = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
cred = credentials.Certificate(service_account)
firebase_admin.initialize_app(cred)
db = firestore.client()

def generar_colores():
    colores = []
    tonos_usados = []
    for _ in range(5):
        while True:
            tono = random.randint(0, 360)
            if all(abs(tono - t) >= 40 for t in tonos_usados):
                break
        tonos_usados.append(tono)
        colores.append({
            "hue": tono,
            "saturation": random.randint(55, 95),
            "brightness": random.randint(60, 90)
        })
    return colores

# Generar reto para mañana
manana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
colores = generar_colores()

db.collection("daily_challenges").document(manana).set({
    "id": manana,
    "date": manana,
    "colors": colores,
    "createdAt": firestore.SERVER_TIMESTAMP
})

print(f"Reto generado para {manana}: {colores}")

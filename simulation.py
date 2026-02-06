import requests
import time
import random
from faker import Faker

fake = Faker("en_IN")

API = "http://127.0.0.1:8000"

DEPTS = ["Cardiology","Oncology","Orthopedics","Pediatrics","Emergency","General Medicine"]

while True:

    # 1️⃣ ADMISSION
    payload = {
        "name": fake.name(),
        "dept": random.choice(DEPTS),
        "vitals": random.randint(20, 100)
    }

    r = requests.post(f"{API}/ingest", json=payload)

    admission_id = r.json()["admission_id"]

    print("Admitted:", admission_id)

    # 2️⃣ AFTER SOME TIME → DISCHARGE
    if random.random() < 0.5:

        time.sleep(2)

        d = requests.post(f"{API}/discharge/{admission_id}")

        print("Discharged:", d.json())

    time.sleep(3)

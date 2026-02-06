import psycopg2
import random
import time
from datetime import datetime, timedelta

# ---------------- DB CONNECTION ----------------

def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="Hospital_Resource_utilization",
        user="postgres",
        password="Abdur1379",      # <-- CHANGE IF YOUR PASSWORD DIFFERENT
        port="5432"
    )

# ------------- GET RANDOM DOCTOR & DEPARTMENT -------------

def get_random_doctor_department():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT doctor_id, department_id 
        FROM dim_doctor 
        ORDER BY random() 
        LIMIT 1
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row[0], row[1]
    else:
        return None, None

# ------------- GET AVAILABLE BED -------------

def get_available_bed():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT bed_id FROM dim_bed
        WHERE bed_id NOT IN (
            SELECT bed_id 
            FROM admission_fact
            WHERE discharge_datetime IS NULL
        )
        LIMIT 1
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row[0]
    else:
        return None


# ------------- CREATE PATIENT -------------

def create_patient():
    conn = get_conn()
    cur = conn.cursor()

    name = "Patient " + str(random.randint(1000, 9999))
    age = random.randint(18, 80)
    gender = random.choice(["Male", "Female"])
    insurance = random.choice(["Private", "Govt", "None"])

    cur.execute("""
        INSERT INTO dim_patient(patient_name, age, gender, insurance_type)
        VALUES(%s, %s, %s, %s)
        RETURNING patient_id
    """, (name, age, gender, insurance))

    patient_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return patient_id


# ------------- CREATE ADMISSION (MAIN LOGIC) -------------

def create_admission():

    patient_id = create_patient()
    doctor_id, department_id = get_random_doctor_department()
    bed_id = get_available_bed()


    if doctor_id is None:
        print("No doctor data available")
        return
    if bed_id is None:
    	print("No beds available")
    	return

    admission_datetime = datetime.now()

    # --------- OUTCOME DECISION ---------
    outcome = random.choice([
        "Recovered",
        "Improved",
        "Transferred",
        "Deceased",
        "Admitted"
    ])

    # ============ ONLY LOGIC YOU ASKED ============

    if outcome == "Admitted":
        discharge_datetime = None
        billing_amount = 0
        procedure_cost = 0

    else:
        discharge_datetime = admission_datetime + timedelta(
            hours=random.randint(6, 72)
        )

        billing_amount = random.randint(2000, 6000)
        procedure_cost = random.randint(8000, 20000)

    # ==============================================

    is_emergency = random.choice([True, False])

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO admission_fact(
            patient_id,
            doctor_id,
            department_id,
	    bed_id,
            admission_datetime,
            discharge_datetime,
            outcome,
            is_emergency,
            billing_amount,
            procedure_cost,
            created_at
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        patient_id,
        doctor_id,
        department_id,
	bed_id,
        admission_datetime,
        discharge_datetime,
        outcome,
        is_emergency,
        billing_amount,
        procedure_cost,
        datetime.now()
    ))

    conn.commit()
    cur.close()
    conn.close()

    print("Inserted:", outcome, discharge_datetime)


# ------------- RUN EVERY 5 MINUTES -------------

print("Starting 5 minute patient generator...")

while True:
    try:
        create_admission()
        time.sleep(300)     # 5 minutes

    except Exception as e:
        print("Error:", e)
        time.sleep(10)

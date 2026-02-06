import psycopg2
import time
import random

conn = psycopg2.connect(
    dbname="Hospital_Resource_utilization",
    user="postgres",
    password="Abdur1379",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

print("🏥 Discharge + Billing Simulation Started...")

while True:
    cur.execute("""
        UPDATE admission_fact
        SET
            discharge_datetime = admission_datetime + INTERVAL '2 hours',
            billing_amount = ROUND(random() * 45000 + 5000),
            procedure_cost = ROUND(random() * 30000 + 3000),
            outcome = CASE
                WHEN random() < 0.7 THEN 'Recovered'
                WHEN random() < 0.85 THEN 'Improved'
                WHEN random() < 0.95 THEN 'Transferred'
                ELSE 'Deceased'
            END
        WHERE discharge_datetime IS NULL
        AND random() < 0.4;
    """)
    conn.commit()
    print("✔ Patients discharged with billing & outcome")
    time.sleep(60)

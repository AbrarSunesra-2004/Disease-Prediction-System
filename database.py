import sqlite3
from datetime import datetime
import os

class PatientDatabase:
    def __init__(self):
        # Delete existing database if exists
        if os.path.exists('patients.db'):
            os.remove('patients.db')
        
        self.conn = sqlite3.connect('patients.db')
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                disease TEXT,
                confidence FLOAT,
                symptoms TEXT,
                patient_info TEXT
            )
        ''')
        self.conn.commit()
    
    def add_prediction(self, disease, confidence, symptoms, patient_info):
        cursor = self.conn.cursor()
        timestamp = datetime.now()
        symptoms_str = ','.join(symptoms)
        patient_info_str = str(patient_info)
        
        cursor.execute('''
            INSERT INTO predictions (timestamp, disease, confidence, symptoms, patient_info)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, disease, confidence, symptoms_str, patient_info_str))
        self.conn.commit()
    
    def get_all_predictions(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC')
        return cursor.fetchall()
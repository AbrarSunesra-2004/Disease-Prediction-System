import pickle
import numpy as np
import pandas as pd
from database import PatientDatabase
from datetime import datetime

class DiseasePredictor:
    def __init__(self):
        self.db = PatientDatabase()
        self.model = None
        self.label_encoder = None
        self.symptoms = None
        self.descriptions = None
        self.precautions = None
        self.load_model()
        self.load_descriptions()
    
    def load_model(self):
        try:
            with open('disease_model.pkl', 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.label_encoder = data['label_encoder']
                self.symptoms = data['symptoms']
            return True
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
    
    def load_descriptions(self):
        try:
            self.descriptions = pd.read_csv('symptom_Description.csv')
            self.precautions = pd.read_csv('symptom_precaution.csv')
            return True
        except Exception as e:
            print(f"Error loading descriptions: {str(e)}")
            return False
    
    def predict_disease(self, selected_symptoms):
        if not selected_symptoms:
            return None, None
        
        X = np.zeros(len(self.symptoms))
        for symptom in selected_symptoms:
            idx = self.symptoms.index(symptom)
            X[idx] = 1
        
        try:
            prediction = self.model.predict([X])
            probability = self.model.predict_proba([X]).max()
            disease = self.label_encoder.inverse_transform(prediction)[0]
            return disease, probability
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return None, None
    
    def get_disease_info(self, disease):
        description = ""
        precautions = []
        
        if self.descriptions is not None:
            desc = self.descriptions[self.descriptions['Disease'] == disease]['Description'].values
            if len(desc) > 0:
                description = desc[0]
        
        if self.precautions is not None:
            prec_row = self.precautions[self.precautions['Disease'] == disease]
            if not prec_row.empty:
                precautions = [
                    prec_row[f'Precaution_{i+1}'].values[0]
                    for i in range(4)
                ]
        
        return description, precautions
    
    def save_prediction(self, disease, probability, symptoms, patient_info):
        return self.db.add_prediction(disease, probability, symptoms, patient_info)
    
    def get_prediction_history(self):
        return self.db.get_all_predictions()
    
    def get_all_symptoms(self):
        return self.symptoms
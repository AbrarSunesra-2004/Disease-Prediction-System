import pandas as pd
import numpy as np
from itertools import combinations

def create_training_dataset():
    # Disease-Symptom mapping with primary and secondary symptoms
    disease_data = {
        'Heart Disease': {
            'primary': ['chest pain', 'shortness of breath', 'irregular heartbeat'],
            'secondary': ['fatigue', 'dizziness', 'nausea', 'sweating', 'arm pain', 'jaw pain']
        },
        'COVID-19': {
            'primary': ['fever', 'dry cough', 'loss of taste', 'loss of smell'],
            'secondary': ['fatigue', 'difficulty breathing', 'body aches', 'headache', 'sore throat']
        },
        'Diabetes': {
            'primary': ['excessive thirst', 'frequent urination', 'extreme hunger'],
            'secondary': ['unexplained weight loss', 'fatigue', 'blurred vision', 'slow healing sores', 'frequent infections']
        },
        'Asthma': {
            'primary': ['wheezing', 'shortness of breath', 'chest tightness'],
            'secondary': ['coughing', 'difficulty breathing', 'rapid breathing', 'anxiety']
        },
        'Migraine': {
            'primary': ['severe headache', 'light sensitivity', 'sound sensitivity'],
            'secondary': ['nausea', 'vomiting', 'vision changes', 'dizziness']
        },
        'Hypertension': {
            'primary': ['headache', 'chest pain', 'irregular heartbeat'],
            'secondary': ['shortness of breath', 'nosebleeds', 'dizziness', 'vision problems']
        },
        'Arthritis': {
            'primary': ['joint pain', 'joint stiffness', 'swelling'],
            'secondary': ['reduced mobility', 'weakness', 'fatigue', 'inflammation']
        },
        'Pneumonia': {
            'primary': ['chest pain', 'fever', 'cough with phlegm'],
            'secondary': ['shortness of breath', 'fatigue', 'chills', 'rapid breathing', 'sweating']
        }
    }
    
    # Create dataset with multiple entries per disease
    dataset = []
    for disease, symptoms in disease_data.items():
        primary = symptoms['primary']
        secondary = symptoms['secondary']
        
        # Always include all primary symptoms
        dataset.append({
            'Disease': disease,
            'Symptoms': ','.join(primary)
        })
        
        # Include primary symptoms with combinations of secondary symptoms
        for i in range(1, len(secondary) + 1):
            for sec_combo in combinations(secondary, i):
                symptom_set = primary + list(sec_combo)
                dataset.append({
                    'Disease': disease,
                    'Symptoms': ','.join(symptom_set)
                })
    
    df = pd.DataFrame(dataset)
    df.to_csv('dataset.csv', index=False)
    
    # Create severity scores
    all_symptoms = set()
    for symptoms in disease_data.values():
        all_symptoms.update(symptoms['primary'])
        all_symptoms.update(symptoms['secondary'])
    
    severity_data = []
    for symptom in all_symptoms:
        # Higher weights for primary symptoms
        is_primary = any(symptom in s['primary'] for s in disease_data.values())
        weight = np.random.randint(4, 7) if is_primary else np.random.randint(1, 4)
        severity_data.append({
            'Symptom': symptom,
            'weight': weight
        })
    
    severity_df = pd.DataFrame(severity_data)
    severity_df.to_csv('Symptom-severity.csv', index=False)
    
    # Create disease descriptions with more detailed information
    descriptions = []
    for disease, symptoms in disease_data.items():
        desc = f"{disease} is characterized primarily by {', '.join(symptoms['primary'])}. "
        desc += f"Additional symptoms may include {', '.join(symptoms['secondary'])}."
        descriptions.append({
            'Disease': disease,
            'Description': desc
        })
    
    desc_df = pd.DataFrame(descriptions)
    desc_df.to_csv('symptom_Description.csv', index=False)
    
    # Create specific precautions for each disease
    precautions = []
    for disease in disease_data.keys():
        prec = get_disease_precautions(disease)
        precautions.append({
            'Disease': disease,
            **prec
        })
    
    prec_df = pd.DataFrame(precautions)
    prec_df.to_csv('symptom_precaution.csv', index=False)
    print("Dataset created successfully!")

def get_disease_precautions(disease):
    precautions_map = {
        'Heart Disease': {
            'Precaution_1': 'Monitor blood pressure regularly',
            'Precaution_2': 'Maintain healthy diet and exercise',
            'Precaution_3': 'Avoid smoking and limit alcohol',
            'Precaution_4': 'Take prescribed medications regularly'
        },
        'COVID-19': {
            'Precaution_1': 'Wear masks in public places',
            'Precaution_2': 'Maintain social distancing',
            'Precaution_3': 'Practice good hand hygiene',
            'Precaution_4': 'Get vaccinated and boosters'
        }
    }
    return precautions_map.get(disease, {
        'Precaution_1': 'Consult a healthcare professional',
        'Precaution_2': 'Follow prescribed medication',
        'Precaution_3': 'Maintain healthy lifestyle',
        'Precaution_4': 'Regular health checkups'
    })

if __name__ == "__main__":
    create_training_dataset()
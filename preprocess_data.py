import pandas as pd
import numpy as np

def preprocess_dataset():
    # Load the dataset files
    symptom_severity = pd.read_csv('Symptom-severity.csv')
    disease_description = pd.read_csv('symptom_Description.csv')
    disease_precaution = pd.read_csv('symptom_precaution.csv')
    
    # Process symptom severity data
    symptoms = symptom_severity['Symptom'].tolist()
    severity = symptom_severity['weight'].tolist()
    
    # Create processed data dictionary
    processed_data = {
        'symptoms': symptoms,
        'severity': severity,
        'descriptions': disease_description,
        'precautions': disease_precaution
    }
    
    return processed_data
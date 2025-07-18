import pandas as pd

def prepare_dataset():
    # Read the Kaggle dataset files
    severity = pd.read_csv('Symptom-severity.csv')
    description = pd.read_csv('symptom_Description.csv')
    
    # Create a sample dataset with diseases and their symptoms
    data = []
    for _, row in description.iterrows():
        disease = row['Disease']
        # Get related symptoms from severity dataset
        symptoms = severity['Symptom'].sample(n=min(5, len(severity))).tolist()
        data.append({
            'Disease': disease,
            'Symptoms': ','.join(symptoms)
        })
    
    # Save as CSV
    df = pd.DataFrame(data)
    df.to_csv('dataset.csv', index=False)

if __name__ == "__main__":
    prepare_dataset()
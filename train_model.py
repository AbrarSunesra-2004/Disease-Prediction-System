import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

def train_model():
    try:
        # Load dataset and severity information
        df = pd.read_csv('dataset.csv')
        severity_df = pd.read_csv('Symptom-severity.csv')
        
        # Extract unique symptoms from severity data
        symptoms = severity_df['Symptom'].unique().tolist()
        
        # Create feature matrix (symptoms x patients)
        X = np.zeros((len(df), len(symptoms)))
        for i, row in df.iterrows():
            for symptom in row['Symptoms'].split(','):
                if symptom.strip() in symptoms:
                    symptom_idx = symptoms.index(symptom.strip())
                    X[i, symptom_idx] = 1
        
        # Encode disease labels
        le = LabelEncoder()
        y = le.fit_transform(df['Disease'])
        
        # Initialize improved Random Forest model
        model = RandomForestClassifier(
            n_estimators=300,          # More trees for better learning
            max_depth=12,              # Deeper trees for complex patterns
            min_samples_split=4,       # Minimum samples for splitting
            min_samples_leaf=2,        # Minimum samples in leaf nodes
            class_weight='balanced',   # Handle imbalanced disease classes
            criterion='entropy',       # Use entropy for splits
            random_state=42           # For reproducibility
        )
        
        # Train the model
        model.fit(X, y)
        
        # Save model and related data
        model_data = {
            'model': model,
            'label_encoder': le,
            'symptoms': symptoms
        }
        with open('disease_model.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        print("Model trained successfully!")
        
        # Calculate and return accuracy
        accuracy = model.score(X, y)
        return accuracy
        
    except Exception as e:
        print(f"Error training model: {str(e)}")
        return 0.0

if __name__ == "__main__":
    print("Training disease prediction model...")
    accuracy = train_model()
    print(f"Model accuracy: {accuracy:.2f}")
    print("\nModel saved as 'disease_model.pkl'")
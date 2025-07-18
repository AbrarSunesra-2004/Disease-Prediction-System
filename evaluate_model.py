import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def evaluate_model(test_data_path='Testing.csv'):
    # Load the trained model
    with open('disease_model.pkl', 'rb') as f:
        data = pickle.load(f)
        model = data['model']
        label_encoder = data['label_encoder']
        symptoms = data['symptoms']
    
    # Load test data
    test_df = pd.read_csv(test_data_path)
    
    # Prepare features and target
    X_test = test_df[symptoms]
    y_test = label_encoder.transform(test_df['prognosis'])
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Generate classification report
    print("\nClassification Report:")
    print(classification_report(
        y_test, 
        y_pred, 
        target_names=label_encoder.classes_
    ))
    
    # Create confusion matrix visualization
    plt.figure(figsize=(15, 10))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig('confusion_matrix.png')
    plt.close()
    
    # Feature importance analysis
    feature_importance = pd.DataFrame({
        'symptom': symptoms,
        'importance': model.feature_importances_
    })
    feature_importance = feature_importance.sort_values(
        'importance', ascending=False
    )
    
    # Plot feature importance
    plt.figure(figsize=(15, 8))
    sns.barplot(
        data=feature_importance.head(20),
        x='importance',
        y='symptom'
    )
    plt.title('Top 20 Most Important Symptoms')
    plt.xlabel('Importance Score')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    plt.close()
    
    return feature_importance

if __name__ == "__main__":
    evaluate_model()
"""
Train and save disease prediction models for the Disease Predictor page.
Run this script once to pre-train all models and save them to disk.
"""
import pandas as pd
import os
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn import tree, svm
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

def train_and_save_models():
    """Train all disease prediction models and save them to disk."""
    
    # Get base path
    BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages')
    MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    
    # Create models directory if it doesn't exist
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    print("Loading datasets...")
    # Load datasets
    dis_sym_data = pd.read_csv(os.path.join(BASE_DIR, "Original_Dataset.csv"))
    
    # Prepare symptom columns
    columns_to_check = [col for col in dis_sym_data.columns if col != 'Disease']
    symptoms_list = list(set(dis_sym_data.iloc[:, 1:].values.flatten()))
    symptoms_list = [s for s in symptoms_list if pd.notna(s)]
    
    print(f"Processing {len(symptoms_list)} symptoms...")
    for symptom in symptoms_list:
        dis_sym_data[symptom] = dis_sym_data.iloc[:, 1:].apply(lambda row: int(symptom in row.values), axis=1)
    
    dis_sym_data_v1 = dis_sym_data.drop(columns=columns_to_check)
    dis_sym_data_v1 = dis_sym_data_v1.loc[:, dis_sym_data_v1.columns.notna()]
    dis_sym_data_v1.columns = dis_sym_data_v1.columns.str.strip()
    
    # Encode labels
    print("Encoding labels...")
    le = LabelEncoder()
    dis_sym_data_v1['Disease'] = le.fit_transform(dis_sym_data_v1['Disease'])
    X = dis_sym_data_v1.drop(columns="Disease")
    y = dis_sym_data_v1['Disease']
    
    # Save the label encoder
    print("Saving label encoder...")
    joblib.dump(le, os.path.join(MODELS_DIR, 'label_encoder.joblib'))
    
    # Save feature columns
    print("Saving feature columns...")
    joblib.dump(X.columns.tolist(), os.path.join(MODELS_DIR, 'feature_columns.joblib'))
    
    # Train and save models
    algorithms = {
        'logistic_regression': LogisticRegression(max_iter=1000),
        'decision_tree': tree.DecisionTreeClassifier(),
        'random_forest': RandomForestClassifier(n_estimators=100),
        'svm': svm.SVC(probability=True),
        'naive_bayes': GaussianNB(),
        'knn': KNeighborsClassifier(),
    }
    
    for model_name, model in algorithms.items():
        print(f"Training {model_name}...")
        model.fit(X, y)
        
        model_path = os.path.join(MODELS_DIR, f'{model_name}.joblib')
        joblib.dump(model, model_path)
        print(f"✓ Saved {model_name} to {model_path}")
    
    print("\n✅ All models trained and saved successfully!")
    print(f"Models directory: {MODELS_DIR}")
    print(f"Total models saved: {len(algorithms)}")

if __name__ == "__main__":
    train_and_save_models()

import pyttsx3
def speak_result(name, age, disease):
    engine = pyttsx3.init()
    text = f"Hello {name}. Your age is {age}. Based on symptoms, possible condition is {disease}. Please consult a doctor."
    engine.say(text)
    engine.runAndWait()

from flask import Flask, request, render_template, flash, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import joblib
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'x7k9p2m4q8r5t1n3j6h0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///symptom_checker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Simple Patient model - NO USER LOGIN
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.String(10))
    symptoms = db.Column(db.String(500))
    prediction = db.Column(db.String(200))

# Load model, encoder, and CSV
def get_model_path(filename):
    """Handle path - work from current dir or AI-Symptom-Checker dir"""
    paths = [filename, f"AI-Symptom-Checker/{filename}"]
    for path in paths:
        if os.path.exists(path):
            return path
    return filename

model = joblib.load(get_model_path("symptom_checker_model.pkl"))
mlb = joblib.load(get_model_path("mlb_encoder.pkl"))
df = pd.read_csv(get_model_path("DiseaseAndSymptoms.csv"))

# Symptom columns and extraction
symptom_columns = [f"Symptom_{i}" for i in range(1, 18)]
# Clean symptoms: strip whitespace and normalize underscores
all_symptoms = sorted(set([symptom.strip().replace(" ", "_") for col in symptom_columns for symptom in df[col].dropna().unique()]))

# Symptom categories
symptom_categories = {
    "Skin": [s for s in all_symptoms if any(kw in s for kw in ["skin", "rash", "itch", "patch", "eruption"])],
    "Respiratory": [s for s in all_symptoms if any(kw in s for kw in ["cough", "breath", "sputum", "chest", "phlegm"])],
    "Digestive": [s for s in all_symptoms if any(kw in s for kw in ["vomit", "nausea", "abdominal", "diarrhoea", "constipation", "ulcer", "acidity"])],
    "General": [s for s in all_symptoms if any(kw in s for kw in ["fever", "fatigue", "chill", "sweat", "malaise", "weight", "thirst"])],
    "Neurological": [s for s in all_symptoms if any(kw in s for kw in ["headache", "dizz", "balance", "confusion", "numb"])]
}
symptom_categories["Other"] = [s for s in all_symptoms if s not in sum(symptom_categories.values(), [])]

# ============== MAIN ROUTES ==============

@app.route("/", methods=["GET", "POST"])
def index():
    """Home page - symptom selection"""
    selected_symptoms = []
    feedback_submitted = session.get('feedback_submitted', False)
    feedback_error = session.get('feedback_error', False)

    if request.method == "POST" and 'symptom-form' in request.form:
        name = request.form.get("name")
        age = request.form.get("age")
        session['name'] = name
        session['age'] = age
        selected_symptoms = []
        for category in symptom_categories:
            selected_symptoms.extend(request.form.getlist(category))
        
        if len(selected_symptoms) < 3:
            return render_template("index.html", categories=symptom_categories, 
                                 selected_symptoms=selected_symptoms, 
                                 error="Please select at least 3 symptoms",
                                 feedback_submitted=feedback_submitted,
                                 feedback_error=feedback_error)
        
        # Create binary vector
        input_vector = np.zeros(len(mlb.classes_))
        recognized_count = 0
        unrecognized = []
        
        for symptom in selected_symptoms:
            if symptom in mlb.classes_:
                input_vector[np.where(mlb.classes_ == symptom)] = 1
                recognized_count += 1
            else:
                unrecognized.append(symptom)
        
        # Debug: Print recognition status
        print(f"\n📊 Prediction Debug:")
        print(f"   Selected symptoms: {len(selected_symptoms)}")
        print(f"   Recognized: {recognized_count}")
        print(f"   Unrecognized: {len(unrecognized)}")
        if unrecognized:
            print(f"   Unrecognized symptoms: {unrecognized[:3]}")  # Show first 3

        # Predict with probabilities
        probabilities = model.predict_proba([input_vector])[0]
        top_preds = sorted(zip(model.classes_, probabilities), key=lambda x: x[1], reverse=True)[:3]
        prediction = top_preds[0][0]
        others = [f"{p[0]} ({p[1] * 100:.0f}%)" for p in top_preds[1:]]
        
        print(f"\n✅ PATIENT DIAGNOSIS")
        print(f"   Name: {name}")
        print(f"   Age: {age}")
        print(f"   Predicted Disease: {prediction} ({top_preds[0][1]*100:.1f}%)\n")
        
        # Store in database (no user linking)
        patient = Patient(
            name=name,
            age=age,
            symptoms=", ".join(selected_symptoms),
            prediction=prediction)
        db.session.add(patient)
        db.session.commit()
        
        # Store in session
        session['prediction'] = prediction
        session['others'] = others
        session['selected_symptoms'] = selected_symptoms
        
        return redirect(url_for('result'))
    
    # Feedback form handling
    if request.method == "POST" and 'feedback-form' in request.form:
        name = request.form.get('name')
        email = request.form.get('email')
        feedback = request.form.get('feedback')
        
        if not name or not email or not feedback:
            session['feedback_error'] = True
            return redirect(url_for('index'))
        else:
            submit_time = datetime.now().strftime("%d/%m/%y %H:%M:%S")
            with open("feedback.txt", "a") as f:
                f.write(f"Date: {submit_time}, Name: {name}, Email: {email}, Feedback: {feedback}\n")
            session['feedback_submitted'] = True
            print(f"Feedback received - Date: {submit_time}, Name: {name}, Email: {email}, Feedback: {feedback}")
            return redirect(url_for('index'))
    
    # Reset feedback flags on GET
    if request.method == "GET":
        if 'feedback_submitted' in session:
            session.pop('feedback_submitted')
        if 'feedback_error' in session:
            session.pop('feedback_error')

    return render_template("index.html", categories=symptom_categories, 
                         selected_symptoms=selected_symptoms, 
                         feedback_submitted=feedback_submitted,
                         feedback_error=feedback_error)


@app.route("/result")
def result():
    """Display diagnosis result"""
    prediction = session.get('prediction')
    others = session.get('others', [])
    name = session.get('name')
    age = session.get('age')

    if not prediction:
        return redirect(url_for('index'))
    
    return render_template("result.html", 
                         prediction=prediction, 
                         others=others, 
                         name=name, 
                         age=age)


@app.route("/patients")
def view_patients():
    """Display patient records page"""
    return render_template("patients.html")


@app.route("/api/patients", methods=["GET"])
def api_get_patients():
    """API endpoint to get all patient records"""
    patients = Patient.query.order_by(Patient.id.desc()).all()
    
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'age': p.age,
            'symptoms': p.symptoms,
            'prediction': p.prediction
        } for p in patients
    ])


@app.route("/api/patients/<int:patient_id>", methods=["DELETE"])
def api_delete_patient(patient_id):
    """Delete a specific patient record"""
    patient = Patient.query.get(patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Patient deleted'})
    return jsonify({'success': False, 'message': 'Patient not found'}), 404


@app.route("/api/patients/clear-all", methods=["DELETE"])
def api_clear_all_patients():
    """Delete all patient records"""
    db.session.query(Patient).delete()
    db.session.commit()
    return jsonify({'success': True, 'message': 'All patient records cleared'})


@app.route("/model-info")
def model_info():
    """Display ML model information"""
    all_symptoms_list = sorted(mlb.classes_)
    all_diseases_list = sorted(model.classes_)
    
    data = {
        'model_info': {
            'model_type': 'RandomForestClassifier',
            'n_estimators': 100,
            'accuracy': '100%'
        },
        'all_symptoms': all_symptoms_list,
        'all_diseases': all_diseases_list,
        'symptom_count': len(all_symptoms_list),
        'disease_count': len(all_diseases_list),
    }
    
    return render_template("model_info.html", **data)


if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)

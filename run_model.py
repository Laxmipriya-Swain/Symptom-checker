import joblib
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load model and encoder
model = joblib.load(os.path.join(script_dir, "symptom_checker_model.pkl"))
mlb = joblib.load(os.path.join(script_dir, "mlb_encoder.pkl"))

print("\n" + "="*80)
print("📊 PKL FILES DATA")
print("="*80)

print("\n🔹 MODEL INFORMATION:")
print(f"   Type: {type(model).__name__}")
print(f"   Details: {model}")
print(f"   Total Diseases: {len(model.classes_)}")

print("\n🔹 ALL DISEASES:")
for i, disease in enumerate(sorted(model.classes_), 1):
    print(f"   {i}. {disease}")

print("\n🔹 ENCODER INFORMATION:")
print(f"   Type: {type(mlb).__name__}")
print(f"   Total Symptoms: {len(mlb.classes_)}")

print("\n🔹 ALL SYMPTOMS:")
for i, symptom in enumerate(sorted(mlb.classes_), 1):
    print(f"   {i}. {symptom}")

print("\n" + "="*80 + "\n")

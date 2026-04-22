# 🚀 AI: Intelligent Symptom Checker

**Predict diseases with AI-powered accuracy!** 🌐 An intelligent symptom analysis tool powered by machine learning to help users identify potential diseases based on their symptoms.

## 📋 About This Project

The **AI Symptom Checker** is a web-based application that leverages machine learning to provide intelligent disease predictions based on user-reported symptoms. This tool uses a trained RandomForest classifier to analyze symptom patterns and suggest the most probable diseases with confidence scores.

**Purpose**: To provide an interactive, AI-powered tool that helps users understand potential health conditions based on their symptoms. This is for educational and informational purposes and should not replace professional medical advice.

**Key Highlights**:
- Real-time disease predictions using machine learning
- User-friendly interface with symptom categorization
- Confidence scores for each prediction
- Feedback system to continuously improve model accuracy

- **Smart Symptom Analysis**: Instant disease predictions based on selected symptoms  
- **Organized Categories**: Symptoms grouped into Skin, Respiratory, Digestive, General, Neurological, and Other  
- **Multiple Predictions**: Top 3 probable diseases with confidence scores  
- **User Feedback System**: Share feedback to improve model performance  
- **Secure & Private**: No permanent storage of personal data  

---

## 💻 Tech Stack

| Category           | Technology                           |
|--------------------|--------------------------------------|
| **Backend**        | Python (Flask)                       |
| **Machine Learning** | Scikit-learn (RandomForestClassifier) |
| **Data Processing** | Pandas, NumPy                        |
| **Frontend**       | HTML, CSS, JavaScript (Bootstrap)    |
| **Model Persistence** | Joblib                             |

---

## 🧠 Technical Details

### Machine Learning Model

- **Algorithm**: RandomForestClassifier (Scikit-learn)  
- **Why Random Forest?**  
  - Handles high-dimensional, sparse binary data efficiently  
  - Robust to noise and imbalanced datasets  
  - Provides probability scores for multi-class classification  
- **Training Data**: `DiseaseAndSymptoms.csv`  
  - Maps diseases to up to 17 symptoms per disease  
  - Symptoms encoded as binary features using MultiLabelBinarizer (MLB)  
- **Preprocessing**:  
  - Symptoms categorized into Skin, Respiratory, Digestive, General, Neurological, and Other  
  - Binary input vector created for model inference  
- **Model Serialization**:  
  - Model saved as `symptom_checker_model.pkl` using Joblib  
  - MultiLabelBinarizer saved as `mlb_encoder.pkl`  
- **Prediction Output**:  
  - Top 3 disease predictions with probability scores (e.g., "Disease X (85%)")  
  - Probabilities computed using `predict_proba`  

### Backend

- **Framework**: Flask (lightweight Python web framework)  
- **Functionality**:  
  - Handles GET/POST requests for symptom input and feedback submission  
  - Session management for storing prediction results  
  - Renders `index.html` and `result.html` templates  
- **Security**:  
  - Secret key for session management and flash messages  
  - No permanent storage of sensitive user data  

### Frontend

- **Templates**:  
  - `index.html`: Symptom selection form with categorized checkboxes  
  - `result.html`: Displays primary and secondary predictions  
- **Styling**: Bootstrap for responsive, modern UI  
- **Interactivity**: JavaScript for dynamic form handling  

### Feedback System

- Stores feedback in `feedback.txt` with timestamp, name, email, and comments  
- Uses session flags to prevent duplicate submissions  

---

## 🛠 Quick Setup

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8 or higher**: Core programming language for the application
- **pip**: Python package manager (comes with Python)
- **Virtual Environment**: Recommended for isolated Python dependencies (venv module comes built-in with Python)
- **Git**: For cloning the repository (optional if you download as ZIP)

**System Requirements**:
- Windows, macOS, or Linux
- At least 2GB RAM
- 100MB disk space for the project and dependencies

### Clone & Install

```bash
git clone https://github.com/Laxmipriya-Swain/Symptom-checker.git
cd Symptom-checker
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Required Files

Ensure the following files are present in your project directory before running the application:

- **`DiseaseAndSymptoms.csv`**: Dataset containing disease-symptom mappings (required for model training/inference)
- **`symptom_checker_model.pkl`**: Pre-trained RandomForest model (required for predictions)
- **`mlb_encoder.pkl`**: Pre-trained MultiLabelBinarizer encoder (required for encoding symptoms)

### Python Dependencies

All required Python packages are listed in `requirements.txt` and will be automatically installed via pip:

- **Flask**: Web framework for the application backend
- **Scikit-learn**: Machine learning library for the RandomForest classifier
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Joblib**: Model serialization and persistence

Install all dependencies using:
```bash
pip install -r requirements.txt
```

### Run the App

```bash
python app.py
```

🔗 **Open in browser**: [http://localhost:5000](http://localhost:5000)  

---

## 📂 Project Structure

AI-Symptom-Checker/
├── .git/                          # Git repository
├── .gitignore                     # Git ignore rules (NEW)
├── app.py                         # Flask backend
├── run_model.py                   # Model training
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── DiseaseAndSymptoms.csv         # Dataset
├── symptom_checker_model.pkl      # Trained model
├── mlb_encoder.pkl               # Encoder file
├── feedback.txt                   # User feedback
└── templates/                     # HTML templates
    ├── index.html
    ├── result.html
    ├── model_info.html
    └── patients.html

**File Descriptions**:
- **app.py**: Flask backend handling routes, form submissions, and session management
- **run_model.py**: Script to train the model or initialize pre-trained models
- **DiseaseAndSymptoms.csv**: Contains disease names and their associated symptoms (up to 17 per disease)
- **requirements.txt**: List of all Python packages needed (Flask, scikit-learn, pandas, joblib, numpy)
- **feedback.txt**: Stores timestamped user feedback with name, email, and comments
- **instance/**: Flask configuration directory for sensitive settings
- **templates/**: HTML files for the web interface using Bootstrap framework

---

## 🔍 How It Works

### Step-by-Step Process

1. **Select Symptoms**: 
   - Visit the application and browse symptoms organized by categories (Skin, Respiratory, Digestive, General, Neurological, Other)
   - Select at least 3 symptoms that match your condition
   - Click "Analyze Symptoms" to proceed

2. **AI Analysis**:
   - The selected symptoms are converted into a binary feature vector
   - The trained RandomForestClassifier analyzes the symptom pattern
   - The model predicts the top 3 most probable diseases using `predict_proba`

3. **View Results**:
   - Primary prediction: The most likely disease
   - Secondary predictions: Two additional likely diseases
   - Each disease is displayed with a confidence score (e.g., "Disease X (85%)")

4. **Give Feedback** (Optional):
   - Users can submit feedback to indicate if the prediction was helpful
   - Feedback is stored for future model improvement
   - Help make the system more accurate for other users!

### Behind the Scenes

- **Input Processing**: Symptoms are encoded as binary features (0 or 1) for each possible symptom
- **Model Inference**: RandomForest evaluates feature importance and probability distribution
- **Prediction Output**: Top 3 diseases ranked by prediction confidence score
- **Session Management**: Prediction results are stored in user sessions for reference

---

## 📈 Why Use This?

- **Fast & Accurate**: Powered by RandomForest machine learning trained on real symptom-disease data for reliable predictions
- **User-Friendly Interface**: Intuitive design with categorized symptoms and clear, easy-to-understand results
- **Privacy-First Approach**: No permanent storage of personal medical data; user privacy is our priority
- **Instant Analysis**: Get disease predictions in seconds without waiting for appointments
- **Educational Value**: Learn about potential diseases and their symptom relationships
- **Continuous Improvement**: Feedback system helps improve model accuracy over time

**Disclaimer**: This tool is for educational and informational purposes only. Always consult with a qualified healthcare professional for actual medical diagnosis and treatment.

---

## 🚀 Future Enhancements

- **Doctor Consultation Integration**: Connect users with verified medical professionals for consultations
- **Multi-Language Support**: Expand accessibility to global audience with multiple language options
- **Mobile App Versions**: Native iOS and Android applications for better mobile experience
- **Symptom Severity Analysis**: Incorporate symptom intensity and duration for more refined predictions
- **Advanced Analytics**: Dashboard to visualize prediction trends and common symptoms
- **API Development**: RESTful API for integration with other healthcare platforms
- **Real-time Model Updates**: Automatic model retraining with new feedback data

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: ModuleNotFoundError: No module named 'flask'
- **Solution**: Ensure you've activated your virtual environment and run `pip install -r requirements.txt`

**Issue**: FileNotFoundError: 'symptom_checker_model.pkl' not found
- **Solution**: Run `python run_model.py` to train and generate the model file

**Issue**: Port 5000 already in use
- **Solution**: Change the port in `app.py` (e.g., `app.run(debug=True, port=5001)`) or kill the process using port 5000

**Issue**: CSV file not found
- **Solution**: Ensure `DiseaseAndSymptoms.csv` is in the project root directory

For more help, open an issue on GitHub or check the Flask documentation.

---

## 💬 Contributing & Support

### Report Issues
Found a bug? Have suggestions? We'd love to hear from you!
- **GitHub Issues**: Open an issue on the GitHub repository
- **Pull Requests**: Contribute improvements by submitting a pull request
- **Feedback**: Use the in-app feedback form to help improve the model

### Ways to Contribute
- Report bugs and issues
- Suggest new features or improvements
- Improve documentation
- Add more diseases and symptoms to the dataset
- Optimize the machine learning model
- Improve the user interface

**Show Your Support**: If you find this project helpful, please give it a ⭐ on GitHub!

---

## 📜 License

MIT License - Free for personal and commercial use

**Copyright © 2025 Symptom Checker Project**

You are free to use, modify, and distribute this project for any purpose, as long as you include the license notice.

---

## 🔗 Get Started Now!

👉 `git clone https://github.com/Laxmipriya-Swain/Symptom-checker.git`  

Navigate to the project folder and follow the Quick Setup instructions above to get started!

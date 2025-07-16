
# 🛡️ Insider Threat Detection Web App

This is a full-stack Machine Learning project that detects **insider threats** in an organization using employee behavioral data. It uses an **Isolation Forest algorithm** trained on engineered features from raw logon, file, email, and psychometric logs. The system is built using **Streamlit** and deployed as a **web app**.

---

## 🚀 Live Demo

🔗 [Launch App](https://your-app-link.streamlit.app) *(Replace with your actual deployment URL)*

---

## 💡 Key Features

- 📂 Upload raw logs directly (CSV): `logon`, `file`, `email`, `psychometric`
- ⚙️ Automated backend feature engineering (40+ features)
- 🤖 Anomaly detection using trained Isolation Forest model
- 📊 Anomaly scores + classification per user
- 📈 Beautiful visualizations (line charts)
- 🧠 Psychometric data modeling via PRI Score
- 🌐 Streamlit frontend (clean, responsive UI)

---

## 🧠 Model Info

- **Algorithm**: Isolation Forest (unsupervised anomaly detection)
- **Training Platform**: Google Colab
- **Trained On**: 25–40 behavioral + psychometric features
- **Scaler Used**: `StandardScaler` (fitted on training set)
- **Prediction**: Binary output (Anomalous = 1, Normal = -1) + score

---

## 📂 File Structure

```
insider-threat-detection/
├── app.py                     # Streamlit frontend
├── feature_engineering.py     # Backend pipeline for feature extraction
├── model.pkl                  # Trained Isolation Forest model
├── scaler.pkl                 # Trained StandardScaler
├── requirements.txt           # All Python dependencies
├── sample_logon.csv           # Sample test data
├── sample_file.csv
├── sample_email.csv
├── sample_psychometric.csv
├── screenshots/               # Folder for images used in README
└── README.md                  # You're here!
```

---

## 📷 Screenshots

### 🏠 App UI: Upload Logs
![Upload UI](screenshots/upload.png)

### 📋 Prediction Table
![Prediction Table](screenshots/predictions.png)

### 📈 Anomaly Score Line Chart
![Line Chart](screenshots/chart.png)

### ✅ Success Notification
![Success](screenshots/success.png)

> 💡 Make sure to create a `screenshots/` folder and add these image files.

---

## ⚙️ How to Run Locally

1. **Clone the repo**
```bash
git clone https://github.com/your-username/insider-threat-detection.git
cd insider-threat-detection
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Launch the app**
```bash
streamlit run app.py
```

4. **Upload your raw CSVs** (or use the sample files):
   - `sample_logon.csv`
   - `sample_file.csv`
   - `sample_email.csv`
   - `sample_psychometric.csv`

---

## 🛠️ Deployment Instructions

You can deploy it for free using:

### ✅ **Streamlit Cloud**
1. Push code to GitHub repo  
2. Go to [Streamlit Cloud](https://share.streamlit.io/)  
3. Connect your repo  
4. Set `app.py` as the entry point  
5. Upload your `model.pkl`, `scaler.pkl`, and `requirements.txt`

---

## 📦 `requirements.txt` (Basic)

```txt
streamlit
pandas
numpy
scikit-learn
joblib
```

---

## 🎓 Resume Summary

> Built and deployed a full-stack Insider Threat Detection system using Isolation Forest and behavioral data logs. Designed an end-to-end ML pipeline from feature engineering to model training and deployment using Streamlit.

---

## 👤 Author

**[Your Name]** – Final Year B.Tech Computer Engineering  
📧 your.email@example.com  
🔗 [LinkedIn](https://linkedin.com/in/yourusername)  
🔗 [GitHub](https://github.com/yourusername)

---

## ⭐ If you like this project, give it a ⭐ and share it!


# 🛡️ Insider Threat Detection Web App

This is a full-stack Machine Learning project that detects **insider threats** in an organization using employee behavioral data. It uses an **Isolation Forest algorithm** trained on engineered features from raw logon, file, email, and psychometric logs. The system is built using **Streamlit** and deployed as a **web app**.

---

## 🚀 Live Demo

🔗 [Launch App](https://insider-threat-detection-ehhntauxcm5agx2ozentzd.streamlit.app/) 

---

## 💡 Key Features

- Upload raw logs directly (CSV): `logon`, `file`, `email`, `psychometric`
- Automated backend feature engineering (20+ features)
- Anomaly detection using trained Isolation Forest model
- Anomaly scores + classification per user
- Psychometric data modeling via PRI Score
- Streamlit frontend 

---

## 🧠 Model Info

- **Algorithm**: Isolation Forest (unsupervised anomaly detection)
- **Training Platform**: Google Colab
- **Trained On**: 20 -25 behavioral + psychometric features
- **Scaler Used**: `StandardScaler` (fitted on training set)
- **Prediction**: Binary output (Anomalous = 1, Normal = -1) + score

---

### 🏠 App UI: Upload Logs
![s1](https://github.com/user-attachments/assets/283abf79-0ec1-44f5-bbdb-5f81d9e1dcc7)
![s2](https://github.com/user-attachments/assets/733ad8fc-1bdf-4768-a05d-d4138dbf25e7)
![s3](https://github.com/user-attachments/assets/f714d08c-7dea-490b-8dbf-751003d8ab9c)
![s4](https://github.com/user-attachments/assets/5ee5ada1-77c1-4dae-ba42-485ef4ada45e)





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

4. **Upload your raw CSVs** (or use the sample files)
  use _sample files for no threats result
  use _anomalous files for threat detection

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






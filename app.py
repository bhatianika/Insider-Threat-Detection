import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from feature_engineering import engineer_features
from predict import predict

st.set_page_config(page_title="Insider Threat Detection", layout="wide")

# Top Banner with Image
st.markdown(
    """
    <div style="background-color:#1f2937; padding:20px; border-radius:10px; text-align:center;">
        <img src="logo.png" width="150" style="display:block; margin:auto;" />
        <h1 style="color:#60a5fa;">Grey Trace</h1>
        <p style="color:#d1d5db;">An Insider Threat Detection Tool</p>
        <p style="color:#d1d5db;">Upload activity logs to detect anomalies and insider threats automatically.</p>
    </div>
    """,
    unsafe_allow_html=True
)


# Custom Styles
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    .upload-section {
        background-color: #f9fafb;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    .upload-section:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.08);
    }
    .section-title {
        font-size: 22px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 12px;
    }
    .center-button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    .stButton button {
        background-color: #2563eb;
        color: white;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.15);
        transition: background-color 0.3s ease, transform 0.2s ease;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #1d4ed8;
        transform: scale(1.03);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Upload Sections
st.markdown("### 📂 Upload Activity Log Files:")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="upload-section"><div class="section-title">🔑 Logon Logs (CSV)</div>', unsafe_allow_html=True)
        logon_file = st.file_uploader("", type=["csv"], key="logon")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="upload-section"><div class="section-title">📁 File Access Logs (CSV)</div>', unsafe_allow_html=True)
        file_file = st.file_uploader("", type=["csv"], key="file")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="upload-section"><div class="section-title">📧 Email Logs (CSV)</div>', unsafe_allow_html=True)
        email_file = st.file_uploader("", type=["csv"], key="email")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="upload-section"><div class="section-title">🧠 Psychometric Scores (CSV)</div>', unsafe_allow_html=True)
        psychometric_file = st.file_uploader("", type=["csv"], key="psycho")
        st.markdown('</div>', unsafe_allow_html=True)

# Predict Button
st.markdown('<div class="center-button-container">', unsafe_allow_html=True)
run_button = st.button("🚨 Run Prediction")
st.markdown('</div>', unsafe_allow_html=True)

# Prediction Logic
if run_button:
    if not all([logon_file, file_file, email_file, psychometric_file]):
        st.error("❌ Please upload all 4 required files before running the prediction.")
    else:
        try:
            with st.spinner("🔄 Engineering Features..."):
                features = engineer_features(logon_file, file_file, email_file, psychometric_file)

            with st.spinner("🔍 Running Prediction..."):
                predictions, scores = predict(features)

            results_df = pd.DataFrame({
                "User": features.index,
                "Anomaly Score": scores,
                "Is Anomaly": predictions
            }).reset_index(drop=True)

            results_df = results_df.sort_values(by="Anomaly Score", ascending=False)
            anomalies = results_df[results_df["Is Anomaly"] == -1]

            # Always Show Detailed Analysis Section
            
            with st.expander("📊 Detailed Analysis", expanded=True):
                if anomalies.empty:
                    st.success("✅ No insider threats detected. All clear!")
                else:
                    st.warning("🚨 Insider Threats Detected!")
                    st.subheader("🚨 Anomaly Details")
            
                    # Highlight anomalies clearly
                    styled_anomalies = anomalies.style.set_properties(
                        **{
                            "background-color": "#fee2e2",
                            "color": "#7f1d1d",
                            "font-size": "16px",
                            "font-weight": "bold"
                        }
                    )
            
                    st.dataframe(styled_anomalies, height=300, use_container_width=True)
            
                # Summary Statistics
                st.markdown("### 📊 Summary Statistics:")
                total_users = len(results_df)
                anomaly_count = len(anomalies)
                anomaly_percentage = (anomaly_count / total_users) * 100
            
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Users", total_users)
                col2.metric("Anomalies Detected", anomaly_count)
                col3.metric("Anomaly %", f"{anomaly_percentage:.2f}%")


                # Download Button
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Full Results as CSV",
                    data=csv,
                    file_name="prediction_results.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"❌ Error during processing: {e}")

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import shap
import ipaddress
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, roc_curve, auc, classification_report
)

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="Transaction Fraud Detection", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MODEL LOADING ---
@st.cache_resource
def load_model():
    try:
        with open('/Users/adityabanerjee/Desktop/Fraud Detection/saved models/xgb_model_tuned.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        st.error("Error: 'xgb_model_tuned.pkl' not found. Ensure the file is in the same folder as this script.")
        return None

model = load_model()

# --- 3. HELPER FUNCTIONS & CLEANING PIPELINE ---
def check_ip(ip):
    try:
        ipaddress.ip_address(str(ip).strip())
        return 0
    except:
        return 1

def preprocess_data(df, has_labels=True):
    # Work on a copy to avoid SettingWithCopy warnings
    w_df = df.copy()
    
    # Pre-calculated encoding maps from training
    global_mean = 0.179598
    cat_map = {'Apparel': 0.098813, 'Home Goods': 0.080035, 'Electronics': 0.421763, 'General Retail': 0.180553}
    name_map = {'www.shein.com': 0.179854, 'www.amazon.com': 0.179927, 'www.tripadvisor.com': 0.178906, 
                'www.asos.com': 0.178824, 'books.toscrape.com': 0.178697, 'www.newegg.com': 0.180648, 
                'www.ebay.com': 0.180331}
    status_map = {'Approved': 0.093266, 'Declined': 0.467554, 'Refunded': 0.469133}
    device_map = {'Desktop': -1, 'Mobile': 0, 'Tablet': 1}
    payment_map = {'Apple Pay': 1, 'Crypto': 2, 'Credit Card': 3, 'Debit Card': 4, 'PayPal': 5}

    # Time conversion and sorting is critical for rolling windows and shifts
    w_df['transaction_timestamp'] = pd.to_datetime(w_df['transaction_timestamp'], errors='coerce')
    w_df = w_df.sort_values('transaction_timestamp')
    
    # 1. Feature Engineering
    w_df['dup_transx'] = w_df['transaction_id'].duplicated(keep=False).astype(int)
    w_df['neg_transx'] = (w_df['transaction_amount'] < 0).astype(int)
    
    threshold = 1206.09
    w_df['night_outlier'] = (
        (w_df['transaction_timestamp'].dt.hour >= 1) & 
        (w_df['transaction_timestamp'].dt.hour <= 4) & 
        (w_df['transaction_amount'] > threshold)
    ).astype(int)
    
    # FIX for the ValueError: Use the index for time-based rolling
    temp_df = w_df.set_index('transaction_timestamp')
    w_df['transaction_velocity'] = temp_df.groupby('device_id')['transaction_amount'].transform(
        lambda x: x.rolling('1H').count()
    ).values
    
    w_df['prev_loc'] = w_df.groupby('user_id')['user_location'].shift(1)
    w_df['prev_time'] = w_df.groupby('user_id')['transaction_timestamp'].shift(1)
    w_df['loc_change'] = ((w_df['user_location'] != w_df['prev_loc']) & 
                          ((w_df['transaction_timestamp'] - w_df['prev_time']) <= pd.Timedelta(hours=3)) & 
                          (w_df['prev_loc'].notna())).astype(int)
    
    # 2. Encoding & Mapping
    w_df['merchant_category_encoded'] = w_df['merchant_category'].map(cat_map).fillna(global_mean)
    w_df['merchant_name_encoded'] = w_df['merchant_name'].map(name_map).fillna(global_mean)
    w_df['transaction_status_encoded'] = w_df['transaction_status'].map(status_map).fillna(global_mean)
    w_df['device_type'] = w_df['device_type'].map(device_map).fillna(0)
    w_df['payment_method'] = w_df['payment_method'].map(payment_map).fillna(3)
    
    w_df['bal_amt_ratio'] = np.where(w_df['account_balance'] != 0, 
                                     w_df['transaction_amount'] / w_df['account_balance'], 0).clip(0, 1)
    w_df['invalid_ip'] = w_df['ip_address'].apply(check_ip)
    
    # Capture target if exists
    y_true = w_df['is_fraudulent'] if (has_labels and 'is_fraudulent' in w_df.columns) else None
    
    # Reorder columns to match model training exactly
    final_cols = ['device_type', 'payment_method', 'dup_transx', 'neg_transx', 'night_outlier', 
                  'transaction_velocity', 'loc_change', 'merchant_category_encoded', 
                  'merchant_name_encoded', 'bal_amt_ratio', 'transaction_status_encoded', 'invalid_ip']
    
    return w_df[final_cols], y_true

# --- 4. MAIN INTERFACE ---
st.title("NexFlow - Marsh: Transaction Monitoring")
st.markdown("Automated cleaning and real-time fraud detection for incoming transaction logs.")

# Sidebar
st.sidebar.header("Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload Transaction CSV", type=['csv'])

mode = st.sidebar.radio("Analysis Mode", ("Evaluation (Has Labels)", "Inference (No Labels)"))
has_labels = mode == "Evaluation (Has Labels)"

if uploaded_file and model:
    raw_df = pd.read_csv(uploaded_file)
    
    with st.status("Initializing Security Pipeline...", expanded=False) as status:
        st.write("Cleaning raw data...")
        X, y_true = preprocess_data(raw_df, has_labels=has_labels)
        st.write("Generating predictions...")
        y_pred = model.predict(X)
        y_probs = model.predict_proba(X)[:, 1]
        status.update(label="Analysis Complete", state="complete")

    # --- RESULTS DASHBOARD ---
    st.write("---")
    st.subheader("📊 High-Level Insights")
    c1, c2, c3 = st.columns(3)
    c1.metric("Transactions Scanned", f"{len(X):,}")
    c2.metric("Fraud Cases Detected", f"{sum(y_pred):,}", delta=f"{(sum(y_pred)/len(X)):.2%}", delta_color="inverse")
    c3.metric("Avg Fraud Risk", f"{y_probs.mean():.2%}")

    # --- DETAILED EVALUATION (Only if labeled) ---
    if has_labels and y_true is not None:
        st.write("---")
        st.subheader("🎯 Model Performance Metrics")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Accuracy", f"{accuracy_score(y_true, y_pred):.2%}")
        m2.metric("Precision", f"{precision_score(y_true, y_pred):.2%}")
        m3.metric("Recall", f"{recall_score(y_true, y_pred):.2%}")
        m4.metric("F1-Score", f"{f1_score(y_true, y_pred):.2%}")

        # BEAUTIFIED CLASSIFICATION REPORT
        st.write("#### Detailed Performance Report")
        report = classification_report(y_true, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose().drop(index=['accuracy'])
        
        st.dataframe(
            report_df.style.background_gradient(cmap='RdYlGn', subset=['precision', 'recall', 'f1-score'])
            .format(precision=3), 
            use_container_width=True
        )

        p1, p2 = st.columns(2)
        with p1:
            st.write("#### Confusion Matrix")
            fig, ax = plt.subplots(figsize=(5, 4))
            sns.heatmap(confusion_matrix(y_true, y_pred), annot=True, fmt='d', cmap='Blues', ax=ax)
            ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
            st.pyplot(fig)
        with p2:
            st.write("#### ROC Curve")
            fpr, tpr, _ = roc_curve(y_true, y_probs)
            fig_roc, ax_roc = plt.subplots(figsize=(5, 4))
            ax_roc.plot(fpr, tpr, color='darkorange', label=f'AUC = {auc(fpr, tpr):.2f}')
            ax_roc.plot([0, 1], [0, 1], '--', color='navy')
            ax_roc.set_xlabel('FPR'); ax_roc.set_ylabel('TPR'); ax_roc.legend()
            st.pyplot(fig_roc)

    # --- SHAP EXPLAINABILITY ---
    st.write("---")
    st.subheader("💡 Explainability (SHAP Values)")
    st.write("Visualizing which engineered features impacted the fraud decision the most.")
    
    with st.spinner("Calculating SHAP summary..."):
        explainer = shap.TreeExplainer(model)
        # Sample for performance if file is large
        X_sample = X.head(500) if len(X) > 500 else X
        shap_vals = explainer.shap_values(X_sample)
        
        # Handle binary classification SHAP output consistency
        if isinstance(shap_vals, list) and len(shap_vals) > 1:
            shap_vals = shap_vals[1]

        fig_shap, ax_shap = plt.subplots(figsize=(10, 6))
        shap.summary_plot(shap_vals, X_sample, plot_type="bar", show=False)
        st.pyplot(fig_shap)

else:
    st.info("Ready for analysis. Please upload a CSV file via the sidebar.")
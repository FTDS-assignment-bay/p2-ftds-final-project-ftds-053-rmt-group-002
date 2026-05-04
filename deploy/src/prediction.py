import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os
BASE_DIR = os.path.dirname(__file__)

'''
    LOAD MODEL
'''
cluster_model = joblib.load(os.path.join(BASE_DIR, 'cluster_model.pkl'))
classification_model = joblib.load(os.path.join(BASE_DIR, 'classification_model.pkl'))
threshold = joblib.load(os.path.join(BASE_DIR, 'threshold.pkl'))



'''
    RESULT UI FUNCTION
''' 
def show_result(decision, prob, segment, pred_label, limit):
    percent = int(prob * 100)

    if decision == "APPROVE":
        st.success("**APPROVED ✅**")
        bar_color = "green"
    elif decision == "REVIEW":
        st.warning("**REVIEW ⚠️**")
        bar_color = "orange"
    else:
        st.error("**REJECTED ❌**")
        bar_color = "red"

    st.write(f"**Risk Segment:** {segment}")
    st.caption(f"Risk Level: {prob:.2%}")
    st.progress(int(prob * 100))
    st.write(f"**Prediction:** {pred_label}")
    
    if decision != "REJECT":
        st.success(f"Recommended Credit Limit: ${limit:,.2f}")
    else:
        st.error("Recommended Credit Limit: Not Available (Rejected)")



'''
    MAIN APP
'''
def run():

    def decision(prob):
        if prob < 0.20:
            return "APPROVE"
        elif prob < 0.40:
            return "REVIEW"
        else:
            return "REJECT"

    def prepare_input(data_input):
        df = pd.DataFrame([data_input])

        df['spend_to_income'] = df['purchase_amount'] / (df['monthly_income'] + 1)
        df['income_per_installment'] = df['monthly_income'] / (df['bnpl_installments'] + 1)
        df['delay_ratio'] = df['repayment_delay_days'] / (df['bnpl_installments'] + 1)

        return df

    def clustering(df):
        num_cols_cluster = [
            'age', 'monthly_income', 'credit_score',
            'repayment_delay_days', 'missed_payments',
            'app_usage_frequency'
        ]

        df['cluster'] = cluster_model.predict(df[num_cols_cluster])

        cluster_map = {
            0: "Low Risk",
            1: "Potential Risk",
            2: "High Risk"
        }

        df['cluster_label'] = df['cluster'].map(cluster_map)
        return df

    def predict(df):
        drop_cols = [
            'product_category', 'location', 'transaction_date',
            'risk_score', 'default_flag'
        ]

        df_model = df.drop(columns=drop_cols, errors='ignore')

        y_proba = classification_model.predict_proba(df_model)[:, 1]
        y_pred = (y_proba >= threshold).astype(int)

        prob = y_proba[0]

        label_map = {
            0: "Paid on Time",
            1: "Defaulted"
        }

        prediction_label = label_map[y_pred[0]]
        decision_result = decision(prob)

        return prob, prediction_label, decision_result

    def calculate_credit_limit(df, prob, decision):
        income = df['monthly_income'].iloc[0]

        PTI = 0.3
        monthly_capacity = income * PTI

        cluster = df['cluster'].iloc[0]
        requested_tenor = df['bnpl_installments'].iloc[0]
        if cluster == 0:        # Low Risk
            max_tenor = 12
        elif cluster == 1:      # Potential Risk
            max_tenor = 9
        else:                   # High Risk
            max_tenor = 6

        tenor = max(1, min(requested_tenor, max_tenor))

        base_limit = monthly_capacity * tenor

        risk_factor = max(0.3, 1 - prob)

        if cluster == 0:
            cluster_factor = 1.2
        elif cluster == 1:
            cluster_factor = 1.0
        else:
            cluster_factor = 0.5

        if decision == "APPROVE":
            decision_factor = 1.0
        elif decision == "REVIEW":
            decision_factor = 0.5
        else:
            decision_factor = 0.0

        credit_limit = base_limit * risk_factor * cluster_factor * decision_factor
        return max(0, round(credit_limit, 2))

    # UI
    st.markdown("### BNPL Credit Approval Prediction")
    st.write("Fill in customer information to predict approval status.")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### **Demographic**")
        age = st.number_input("Age", 18, 60, 30)
        employment_type = st.selectbox("Employment Type", ['Salaried', 'Self-Employed', 'Student', 'Unemployed'])
        location = st.selectbox("Location", ['USA', 'India', 'UK', 'Germany', 'Canada', 'Australia'])

    with col2:
        st.write("### **Behavioral Indicators**")
        repayment_delay_days = st.number_input("Repayment Delay (days)", 0, 60, 0)
        missed_payments = st.number_input("Missed Payments", 0, 20, 0)
        app_usage_frequency = st.number_input("App Usage (per week)", 0, 50, 5)

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        st.write("### **Financial Attributes**")
        monthly_income = st.number_input("Monthly Income", 0, 100000, 5000)
        credit_score = st.number_input("Credit Score", 300, 850, 600)
        debt_to_income_ratio = st.number_input("Debt to Income Ratio", 0.0, 1.0, 0.1)
        risk_score = st.number_input("Risk Score", 0.0, 400.0, 50.0)

    with col4:
        st.write("### **Transaction Details**")
        transaction_date = st.date_input("Transaction Date")
        product_category = st.selectbox("Product Category", ['Electronics', 'Fashion', 'Sports', 'Home', 'Beauty'])
        bnpl_installments = st.selectbox("Installments", [3, 6, 9, 12])
        purchase_amount = st.number_input("Purchase Amount", 0, 100000, 1000)

    data = {
        'user_id': 0,
        'age': age,
        'employment_type': employment_type,
        'monthly_income': monthly_income,
        'credit_score': credit_score,
        'purchase_amount': purchase_amount,
        'product_category': product_category,
        'bnpl_installments': bnpl_installments,
        'repayment_delay_days': repayment_delay_days,
        'missed_payments': missed_payments,
        'app_usage_frequency': app_usage_frequency,
        'location': location,
        'transaction_date': str(transaction_date),
        'debt_to_income_ratio': debt_to_income_ratio,
        'risk_score': risk_score,
        'customer_segment': ''
    }

    if st.button("Predict"):

        df_input = prepare_input(data)
        df_input = clustering(df_input)

        prob, pred_label, decision_result = predict(df_input)
        limit = calculate_credit_limit(df_input, prob, decision_result)

        st.markdown("---")
        st.subheader("Prediction Result")
        st.markdown('')
        show_result(
            decision_result,
            prob,
            df_input['cluster_label'].iloc[0],
            pred_label,
            limit
        )
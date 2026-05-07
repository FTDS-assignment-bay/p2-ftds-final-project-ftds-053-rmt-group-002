import streamlit as st
import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)

'''
    LOAD MODEL
'''
cluster_model = joblib.load(os.path.join(BASE_DIR, 'cluster_model.pkl'))
classification_model = joblib.load(os.path.join(BASE_DIR, 'classification_model.pkl'))
threshold = joblib.load(os.path.join(BASE_DIR, 'threshold.pkl'))

'''
    SAFE CSS
'''
st.markdown("""
<style>
/* ===== PAGE ===== */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: #07122A;
}

/* ===== TEXT ===== */
html, body, [class*="css"] {
    color: white;
}

/* ===== TITLE ===== */
.section-title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 10px;
}

.subtext {
    color: #94A3B8;
    font-size: 18px;
    margin-bottom: 35px;
}

/* ===== BUTTON ===== */
.stButton > button {
    width: 100%;
    height: 55px;

    border: none;
    border-radius: 14px;

    background: linear-gradient(
        135deg,
        #22C7F2,
        #3B82F6
    );

    color: white;
    font-size: 18px;
    font-weight: 700;
}

/* ===== INPUT ===== */
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
.stDateInput input {
    background-color: #111827 !important;
    color: white !important;
}

/* ===== METRIC ===== */
[data-testid="metric-container"] {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 16px;
}

</style>
""", unsafe_allow_html=True)

'''
    RESULT UI
'''
def show_result(decision, prob, segment, pred_label, limit):

    if decision == "APPROVE":

        st.markdown("""
        <h4 style='
            color:#22C55E;
            font-size:60px;
            font-weight:800;
            margin-bottom:0;
        '>
        APPROVED ✅
        </h4>
        """, unsafe_allow_html=True)

    elif decision == "REVIEW":

        st.markdown("""
        <h4 style='
            color:#F59E0B;
            font-size:60px;
            font-weight:800;
            margin-bottom:0;
        '>
        REVIEWED ⚠️
        </h4>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <h4 style='
            color:#EF4444;
            font-size:60px;
            font-weight:800;
            margin-bottom:0;
        '>
        REJECTED ❌
        </h4>
        """, unsafe_allow_html=True)

    st.markdown(" ")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Risk Level",
            f"{prob:.2%}"
        )

    with col2:
        st.metric(
            "Risk Segment",
            segment
        )

    with col3:
        if decision != "REJECT":
            st.metric(
                "Credit Limit",
                f"${limit:,.0f}"
            )
        else:
            st.metric(
                "Credit Limit",
                "N/A"
            )

    st.progress(min(int(prob * 100), 100))

    st.markdown(" ")
    st.markdown("### Risk Insight")
    st.info(f"""
Prediction Result: {pred_label}

Recommended Action: {decision}
""")


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

        df['spend_to_income'] = (
            df['purchase_amount'] /
            (df['monthly_income'] + 1)
        )

        df['income_per_installment'] = (
            df['monthly_income'] /
            (df['bnpl_installments'] + 1)
        )

        df['delay_ratio'] = (
            df['repayment_delay_days'] /
            (df['bnpl_installments'] + 1)
        )

        return df

    def clustering(df):

        num_cols_cluster = [
            'age',
            'monthly_income',
            'credit_score',
            'repayment_delay_days',
            'missed_payments',
            'app_usage_frequency'
        ]

        df['cluster'] = cluster_model.predict(
            df[num_cols_cluster]
        )

        cluster_map = {
            0: "Low Risk",
            1: "Potential Risk",
            2: "High Risk"
        }

        df['cluster_label'] = df['cluster'].map(cluster_map)

        return df

    def predict(df):

        drop_cols = [
            'product_category',
            'location',
            'transaction_date',
            'risk_score',
            'default_flag'
        ]

        df_model = df.drop(
            columns=drop_cols,
            errors='ignore'
        )

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

        if cluster == 0:
            max_tenor = 12
        elif cluster == 1:
            max_tenor = 9
        else:
            max_tenor = 6

        tenor = max(
            1,
            min(requested_tenor, max_tenor)
        )

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

        credit_limit = (
            base_limit *
            risk_factor *
            cluster_factor *
            decision_factor
        )

        return max(0, round(credit_limit, 2))

    '''
        HERO SECTION
    '''
    st.title("**BNPL Credit Approval Prediction**")

    '''
        INPUT FORM
    '''
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Demographic")

        age = st.number_input("Age", 18, 60, 30)

        employment_type = st.selectbox(
            "Employment Type",
            ['Salaried', 'Self-Employed', 'Student', 'Unemployed']
        )

        location = st.selectbox(
            "Location",
            ['USA', 'India', 'UK', 'Germany', 'Canada', 'Australia']
        )

    with col2:

        st.subheader("Behavioral Indicators")

        repayment_delay_days = st.number_input(
            "Repayment Delay (days)",
            0, 60, 0
        )

        missed_payments = st.number_input(
            "Missed Payments",
            0, 20, 0
        )

        app_usage_frequency = st.number_input(
            "App Usage (per week)",
            0, 50, 5
        )

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:

        st.subheader("Financial Attributes")

        monthly_income = st.number_input(
            "Monthly Income",
            0, 100000, 5000
        )

        credit_score = st.number_input(
            "Credit Score",
            100, 850, 600
        )

        debt_to_income_ratio = st.number_input(
            "Debt to Income Ratio",
            0.0, 1.0, 0.1
        )

        risk_score = st.number_input(
            "Risk Score",
            0.0, 400.0, 50.0
        )

    with col4:

        st.subheader("Transaction Details")

        transaction_date = st.date_input("Transaction Date")

        product_category = st.selectbox(
            "Product Category",
            ['Electronics', 'Fashion', 'Sports', 'Home', 'Beauty']
        )

        bnpl_installments = st.selectbox(
            "Installments",
            [3, 6, 9, 12]
        )

        purchase_amount = st.number_input(
            "Purchase Amount",
            0, 100000, 1000
        )

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

    if st.button("Predict Credit Approval"):

        df_input = prepare_input(data)

        df_input = clustering(df_input)

        prob, pred_label, decision_result = predict(df_input)

        limit = calculate_credit_limit(
            df_input,
            prob,
            decision_result
        )

        show_result(
            decision_result,
            prob,
            df_input['cluster_label'].iloc[0],
            pred_label,
            limit
        )
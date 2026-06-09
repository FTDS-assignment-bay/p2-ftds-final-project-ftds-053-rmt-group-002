import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

BASE_DIR = os.path.dirname(__file__)
'''
    SEABORN
'''
sns.set_theme(style="darkgrid")

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
    font-size: 34px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 10px;
}

.subtext {
    color: #94A3B8;
    font-size: 18px;
    margin-bottom: 35px;
}

/* ===== METRIC ===== */
[data-testid="metric-container"] {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 16px;
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
    font-size: 16px;
    font-weight: 600;
}

/* ===== CHART ===== */
[data-testid="stPyplot"] {
    background: #111827;
    border-radius: 16px;
    padding: 10px;
    border: 1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

'''
    LOAD DATA
'''
@st.cache_data
def load_data():
    return pd.read_csv(
        os.path.join(
            BASE_DIR,
            'Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv'
        )
    )


'''
    MAIN
'''
def run():

    df = load_data()

    '''
        HERO
    '''
    st.image(
        os.path.join(
            BASE_DIR,
            "FTDS-053-RMT-GROUP002-LOGO.png"
        )
    )

    st.title("**BNPL Credit Risk Analysis Application**")
    st.subheader("Smart credit approval and financial risk analysis using machine learning models.")
    st.markdown(" ")

    '''
        METRICS
    '''
    default_rate = df['default_flag'].mean() * 100

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Records",
            f"{df.shape[0]:,}"
        )

    with col2:
        st.metric(
            "Features",
            df.shape[1]
        )

    with col3:
        st.metric(
            "Default Rate",
            f"{default_rate:.1f}%"
        )

    with col4:
        st.metric(
            "Risk Segments",
            "3"
        )

    st.markdown("---")

    '''
        DATASET
    '''
    st.markdown("## **Dataset Overview**")
    st.markdown(" ")
    with st.expander("View Dataset Preview"):
        st.dataframe(df.head())

    with st.expander("View Data Types"):
        st.write(df.dtypes)

    st.markdown("---")

    '''
        EDA TITLE
    '''
    st.markdown("## **Exploratory Data Analysis**")
    st.markdown("Understanding customer financial behavior and repayment risk patterns.")

    '''
        ROW 1
    '''
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Default Distribution")

        fig, ax = plt.subplots(figsize=(6,4))
        sns.countplot(
            x='default_flag',
            data=df,
            ax=ax,
            palette=['#22C7F2', '#3B82F6']
        )
        ax.set_title('Default Distribution')
        ax.set_xlabel('')
        st.pyplot(fig)

        st.info("Most customers fall into the default category (60%), indicating a moderate class imbalance.")

    with col2:
        st.subheader("Credit Score vs Default")

        fig, ax = plt.subplots(figsize=(6,4))
        sns.boxplot(
            x='default_flag',
            y='credit_score',
            data=df,
            ax=ax,
            palette=['#22C7F2', '#3B82F6']
        )
        ax.set_title('Credit Score by Default')
        st.pyplot(fig)

        st.info("Default customers tend to have significantly lower credit scores.")

    '''
        ROW 2
    '''
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Missed Payments")

        fig, ax = plt.subplots(figsize=(6,4))
        sns.barplot(
            x='default_flag',
            y='missed_payments',
            data=df,
            ax=ax,
            palette=['#22C7F2', '#3B82F6']
        )
        ax.set_title('Missed Payments by Default')
        st.pyplot(fig)

        st.info("Customers with more missed payments show higher default tendencies.")

    with col4:
        st.subheader("Repayment Delay")

        fig, ax = plt.subplots(figsize=(6,4))
        sns.violinplot(
            x='default_flag',
            y='repayment_delay_days',
            data=df,
            ax=ax,
            palette=['#22C7F2', '#3B82F6']
        )
        ax.set_title('Repayment Delay Distribution')
        st.pyplot(fig)

        st.info("Longer repayment delays are strongly associated with higher default risk.")

    '''
        ROW 3
    '''
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Debt-to-Income Ratio")

        fig, ax = plt.subplots(figsize=(6,4))
        sns.kdeplot(
            df[df['default_flag'] == 0]['debt_to_income_ratio'],
            label='Paid',
            fill=True
        )
        sns.kdeplot(
            df[df['default_flag'] == 1]['debt_to_income_ratio'],
            label='Default',
            fill=True
        )
        ax.set_title('Debt-to-Income Ratio Distribution')
        st.pyplot(fig)

        st.info("Higher debt burdens indicate elevated financial risk.")

    with col6:
        st.subheader("Monthly Income Distribution")

        fig, ax = plt.subplots(figsize=(6,4))
        ax.hist(
            df['monthly_income'],
            bins=30,
            color='#22C7F2'
        )
        ax.set_title('Monthly Income Distribution')
        st.pyplot(fig)

        st.info("Income distribution is right-skewed with several high-income outliers.")

    st.markdown("---")

    '''
        FINAL INSIGHT
    '''
    st.markdown("### **Key Insights**")

    st.info("""
    #### Core Risk Drivers
            
    • Credit Score → Strong financial risk indicator.   
    • Missed Payments → Strong behavioral signal.   
    • Repayment Delay → High predictive power.   
    • Debt-to-Income Ratio → Financial burden indicator.   
    • Monthly Income → Requires outlier handling.   

    **Risk is influenced by both customer financial capacity
    and repayment behavior patterns**.
    """)
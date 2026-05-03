import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
BASE_DIR = os.path.dirname(__file__)

sns.set_theme(style="whitegrid", palette="pastel")

@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(BASE_DIR, 'Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv'))

def run():
    # HEADER
    st.title('A-Limit')
    st.subheader('BNPL Credit Risk Analysis Application')
    st.write('Made by Group 2')

    df = load_data()

    st.markdown('---') 



    # DATA OVERVIEW
    st.subheader("Dataset Overview")
    st.write(f"Shape: {df.shape}")
    st.dataframe(df.head())

    st.subheader("Data Types")
    st.write(df.dtypes)

    st.markdown('---')


    # VISUALIZATION
    # 1. TARGET DISTRIBUTION
    st.subheader("Default Distribution")

    fig, ax = plt.subplots(figsize=(5,3))
    sns.countplot(x='default_flag', data=df, ax=ax)
    ax.set_title('Default Distribution (0 = Paid, 1 = Default)')
    st.pyplot(fig)

    st.info("**Most customers are in the default group (60%), indicating class imbalance.**")
    st.markdown('')


    # 2. CREDIT SCORE
    st.subheader("Credit Score vs Default")

    fig, ax = plt.subplots(figsize=(6,4))
    sns.boxplot(x='default_flag', y='credit_score', data=df, ax=ax)
    ax.set_title('Credit Score by Default')
    st.pyplot(fig)

    st.info("**Default customers tend to have lower credit scores.**")
    st.markdown('')

    
    # 3. MISSED PAYMENTS
    st.subheader("Missed Payments vs Default")

    fig, ax = plt.subplots()
    sns.barplot(x='default_flag', y='missed_payments', data=df, ax=ax)
    ax.set_title('Missed Payments by Default')
    st.pyplot(fig)

    st.info("**Higher missed payments strongly correlate with default.**")
    st.markdown('')

    
    # 4. REPAYMENT DELAY
    st.subheader("Repayment Delay vs Default")

    fig, ax = plt.subplots()
    sns.violinplot(x='default_flag', y='repayment_delay_days', data=df, ax=ax)
    ax.set_title('Repayment Delay Distribution')
    st.pyplot(fig)

    st.info("**Default users show longer repayment delays.**")
    st.markdown('')

    
    # 5. DTI
    st.subheader("Debt-to-Income Ratio")

    fig, ax = plt.subplots()
    sns.kdeplot(df[df['default_flag'] == 0]['debt_to_income_ratio'], label='Paid', fill=True)
    sns.kdeplot(df[df['default_flag'] == 1]['debt_to_income_ratio'], label='Default', fill=True)
    ax.set_title('Debt-to-Income Ratio Distribution')
    ax.legend()
    st.pyplot(fig)

    st.info("**Higher debt-to-income ratio indicates higher risk.**")
    st.markdown('')

    
    # 6. INCOME DISTRIBUTION
    st.subheader("Monthly Income Distribution")

    fig, ax = plt.subplots()
    ax.hist(df['monthly_income'], bins=30)
    ax.set_title('Monthly Income Distribution')
    st.pyplot(fig)

    st.info("**Income is right-skewed with some high-income outliers.**")
    st.markdown('---')



    # FINAL INSIGHT
    st.subheader("Key Insights")

    st.markdown("""
    - **Credit Score** → Strong risk indicator  
    - **Missed Payments** → Strong behavioral signal  
    - **Repayment Delay** → High predictive power  
    - **Debt-to-Income Ratio** → Financial burden indicator  
    - **Monthly Income** → Needs outlier handling  

    Risk is driven by **both financial capacity and payment behavior.**
    """)
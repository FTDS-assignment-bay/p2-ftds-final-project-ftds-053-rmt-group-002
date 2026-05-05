[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/MQaDQXPI)
# A-Limit
<p align="center">
  <img src="assets/FTDS-053-RMT-GROUP002-LOGO.png">
</p>

---

## Repository Outline
```text
1. README.md  
   Overview and general explanation of the project.

2. modeling.ipynb  
   Data exploration, preprocessing, and model training process.

3. inference.ipynb  
   Notebook for making predictions (inference).

4. pipeline_DAG.py
   Apache Airflow DAG for ETL automation pipeline

5. deploy/
   ├── Dockerfile           Container configuration file.
   ├── requirements.txt     Project dependencies.
   └── src/
       ├── streamlit_app.py Main Streamlit application.
       ├── eda.py           Exploratory Data Analysis (EDA) module.
       └── prediction.py    Prediction module.

6. assets/
   └── FTDS-053-RMT-GROUP002-LOGO.png       Logo project.
```

## Problem Background
The rapid growth of Buy Now Pay Later (BNPL) services in Fintech, such as ShopeePay, has been very popular in Indonesia since it can be integrated directly into the Shopee ecosystem. While this increases transaction convenience, it significantly raises credit risk. Many platforms still rely on simple rule-based checks that fail to capture the nuances of a customer’s financial health. 

To address this, we have developed a multi-stage modeling pipeline: 
- **Segmenting users** based on behavior
- **Predicting approval** eligibility
- **Optimizing credit limits** to ensure sustainable lending.


## Objectives
1. **Customer Segmentation (Clustering)**    
   To segment users into **Low Risk, Potential Risk, and High Risk** groups based on financial and behavioral characteristics.

2. **Approval Classification**     
   To develop a classification model that predicts whether a customer should be **Approved, Reviewed, or Rejected**, based on their probability of default.

3. **Credit Limit Optimization**    
   To determine a **personalized credit limit** for approved users using financial principles (e.g., affordability ratio) combined with risk-based adjustments.

4. **Deployment for Real-Time Use**    
   To implement the model in a **Streamlit application** for real-time inference and decision support.


## Data
The dataset contains customer demographic, financial, and behavioral data used to analyze credit risk and predict default probability in a BNPL (Buy Now Pay Later) system. The original dataset consists of 17 columns and 10,345 rows.Columns included in the dataset:
- `user_id`: unique identifier.
- `age`: customer's age group relevant to financial behavior analysis.
- `employment_type`: customer’s source of income or employment stability.
- `monthly_income`: customer’s earning capacity on a monthly basis.
- `credit_score`: summarizes the customer’s historical creditworthiness.
- `purchase_amount`: transaction financed through BNPL.
- `product_category`: type of product purchased.
- `bnpl_installments`: number of payments chosen for the BNPL transaction.
- `repayment_delay_days`: delays in repayment indicating potential risk.
- `debt_to_income_ratio`: proportion of income allocated to debt obligations.
- `risk_score`: aggregated indicator reflecting overall customer risk level.
- `customer_segment`: customers group based on similar risk characteristics.
- `missed_payments`: past repayment reliability through missed obligations.
- `default_flag`: indicates whether the customer failed to meet repayment obligations.
- `app_usage_frequency`: user engagement with the BNPL platform.
- `location`: geographic information.
- `transaction_date`: timestamp  BNPL transaction occurred.


## Tech Stack
### Programming Language
- Python

### Libraries
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- phik
- joblib

### Data & Infrastructure
- PostgreSQL, CSV Dataset (Data & Storage)
- Apache Airflow (Pipeline)
- Docker (Containerization)

### Tools & Deployment
- VSCode
- GitHub
- Streamlit


## Project Output
- Implemented a **data pipeline using Apache Airflow** for automated data processing.
- Developed an end-to-end **BNPL credit risk system** integrating EDA, clustering, and classification.
- Built a model to predict **approval decisions and probability of default (PD)**.
- Designed a **dynamic credit limit formula** based on affordability, risk, segmentation, and policy.
- Created an **inference pipeline** for consistent and scalable model usage.
- Deployed an interactive **Streamlit application** for real-time prediction and decisioning.


## License
This project is open-source and can be used for learning purposes.


## References
### Technical
- [Python Documentation](https://docs.python.org/3/)
- [Data Structures for Statistical Computing in Python (Pandas)](https://pandas.pydata.org/docs/)
- [Array Programming with NumPy](https://numpy.org/doc/)
- [Scikit-learn: Machine Learning in Python](https://scikit-learn.org/stable/)
- [Matplotlib: A 2D Graphics Environment](https://matplotlib.org/stable/)
- [Seaborn: Statistical Data Visualization](https://seaborn.pydata.org/)
- [phik: Correlation Analyzer Library](https://phik.readthedocs.io/)

### BNPL System
- [Guidelines on Loan Origination and Monitoring](https://www.eba.europa.eu/regulation-and-policy/credit-risk/guidelines-on-loan-origination-and-monitoring)
- [International Convergence of Capital Measurement and Capital Standards (Basel II)](https://www.bis.org/publ/bcbs128.htm)
- [Responsible Lending and Borrowing](https://documents.worldbank.org/)
- [Consumer Credit and Responsible Lending](https://www.oecd.org/finance/)

### Deployment & Engineering
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Platform
- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)

# LoanShield

**LoanShield** is a machine learning project that predicts the risk of loan default to help lenders make informed decisions. The project includes a **Streamlit web interface** where users can select loan types (Personal, Business, Mortgage), enter loan and applicant details, and instantly receive a default risk prediction.

---

## Features

- **Interactive Loan Selection** – Users choose between Personal, Business, and Mortgage loans via clickable cards.
- **Streamlit Web App** – Clean, intuitive interface for entering applicant and loan information.
- **Multiple ML Models** – Separate models for personal, business, and mortgage loans, loaded dynamically.
- **Automated Preprocessing** – Consistent transformation of user inputs to match training features.
- **Creditworthiness Calculation** – Uses applicant’s income, debt ratio, credit score, and other features.
- **Predictive Insights** – Provides an estimate of default risk to support decision-making.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/salim359/LoanShield.git
cd LoanShield
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Models and Preprocessing Files

Train models using the notebooks in `notebooks/` and ensure the following files exist in the `models/` directory:

- `personal_loan_default_model.pkl` + `personal_X_columns.pkl`
- `business_loan_default_model.pkl` + `business_X_columns.pkl`
- `mortgage_default_model.pkl` + `mortgage_X_columns.pkl`
- `best_loan_default_model.pkl` (general model)
- `X_columns.pkl` (general feature columns)

Also include:

- `preprocessing.py` – contains the `preprocess_input` function
- `functions.py` – utility functions such as `calculate_credit_worthiness_business`

### 4. Run the Streamlit App

```bash
streamlit run loan_ui.py
```

---

## Usage

1. Open the Streamlit app in your browser (URL shown in terminal).
2. Select a loan type by clicking one of the three cards.
3. Enter loan and applicant details.
4. Click **Predict Default** to receive the risk prediction.

### Prediction Output Explained

- **Default (Will not repay):** The applicant is likely to miss payments or not repay the loan.
- **No Default (Will repay):** The applicant is predicted to successfully repay the loan.

---

## Directory Structure

```
LoanShield/
├── dataset/
│   └── Loan_Default.csv
├── loan_ui.py
├── functions.py
├── preprocessing.py
├── requirements.txt
├── .gitignore
├── models/
│   ├── business_loan_default_model.pkl
│   ├── mortgage_default_model.pkl
│   ├── personal_loan_default_model.pkl
│   ├── business_X_columns.pkl
│   ├── mortgage_X_columns.pkl
│   └── personal_X_columns.pkl
├── notebooks/
│   ├── business_loan.ipynb
│   ├── mortage.ipynb
│   └── personal_loan.ipynb
└── README.md
```

---

## Notes

- The app dynamically loads the correct model based on loan type and loan amount.
- Ensure preprocessing steps match between your notebooks and `preprocessing.py`.
- Update `functions.py` when adding new creditworthiness or feature engineering logic.

---

## Dataset

This project uses the [Loan Default Dataset from Kaggle](https://www.kaggle.com/datasets/yasserh/loan-default-dataset/data).

Download and place `Loan_Default.csv` in the `dataset/` directory.

---

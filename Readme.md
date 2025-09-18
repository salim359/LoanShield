
# LoanShield

**LoanShield** is a machine learning project that predicts the risk of loan default to help lenders make informed decisions. The project includes a **Streamlit web interface** where users can enter loan and applicant details and receive a default risk prediction instantly.

---

## Features

* **Streamlit Web App** – Intuitive interface for entering loan and applicant information.
* **Machine Learning Model** – Random Forest classifier trained on historical loan data.
* **Automated Preprocessing** – Ensures user inputs are transformed to match the model’s expectations.
* **Predictive Insights** – Provides an estimate of default risk to assist in decision-making.

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

### 3. Prepare Model and Preprocessing Files

* Train the model using `loan.ipynb` and ensure the following files are generated:

  * `best_loan_default_model.pkl` (trained model)
  * `X_columns.pkl` (list of feature columns used in training)
  * `preprocessing.py` (contains `preprocess_input` function)

### 4. Run the Streamlit App

```bash
streamlit run loan_ui.py
```

---

## Usage

1. Open the Streamlit app in your browser (URL will be provided in the terminal).
2. Enter loan and applicant details in the input fields.
3. Click **Predict Default** to receive the risk prediction.

---

## Directory Structure

```
LoanShield/
├── dataset/
│   └── Loan_Default.csv
├── loan.ipynb
├── loan_ui.py
├── preprocessing.py
├── best_loan_default_model.pkl
├── X_columns.pkl
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Notes

* Ensure that the input features in the app match those used during model training.
* Keep `preprocessing.py` in sync with the steps in `loan.ipynb` to avoid mismatches.

---

## Dataset

This project uses the [Loan Default Dataset from Kaggle](https://www.kaggle.com/datasets/yasserh/loan-default-dataset/data).

* Download the dataset from Kaggle and place `Loan_Default.csv` in the `dataset/` directory.

---

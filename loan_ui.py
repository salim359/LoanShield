import streamlit as st
import joblib
import pandas as pd
from preprocessing import preprocess_input
from functions import calculate_credit_worthiness


model = joblib.load('best_loan_default_model.pkl')
X_columns = joblib.load('X_columns.pkl')  # Save X.columns during training

st.set_page_config(page_title="Loan Default Predictor", page_icon="💸", layout="centered")
st.title("Loan Default Prediction")
st.write("Enter loan and applicant details below to predict default risk.")

# Input fields for relevant features
loan_amount = st.number_input("Loan Amount", min_value=0.0)
total_monthly_debt_payment = st.number_input("Total Monthly Debt Payment", min_value=0.0)
gender = st.selectbox("Gender", ["Male", "Female","Other"])
approv_in_adv = st.selectbox("Aprrove the loan(if the above details are okay are you approving the loan)" ,["YES","NO"])
rate_of_interest = st.number_input("Rate of Interest", min_value=0.0)
term = st.number_input("Term (months)", min_value=0)
neg_ammortization = st.selectbox("Negative Ammortization", ["Yes", "No"])
interest_only = st.selectbox("Interest Only", ["Yes", "No"])
lump_sum_payment = st.number_input("Lump Sum Payment", min_value=0.0)
income = st.number_input("Applicant Income", min_value=0.0)

age = st.number_input("Applicant Age", min_value=18)
open_credit = st.number_input("Open Credit Lines", min_value=0)
business_or_commercial = st.selectbox("Business or Commercial", ["Yes", "No"])
region = st.selectbox("Region", ["North", "South", "East", "West", "Other"])
year = st.number_input("Year", min_value=1900, max_value=2100)
submission_of_application = st.selectbox("Submission of Application", ["Online", "Offline"])

#credit details
credit_type = st.selectbox("Credit Type", ["CIB", "CRIF", "EXP", "EQUI"])
credit_score = st.number_input("Credit Score", min_value=0)
co_applicant_credit_type = st.selectbox("Co-applicant Credit Type", ["CIB", "CRIF", "EXP", "EQUI", "None"])

#property details
property_value = st.number_input("Property Value", min_value=0.0)
total_units = st.selectbox("Total Units", ["1U", "2U", "3U", "4U"])


# --- ARRANGED FEATURE ENGINEERING AND TRANSFORMATIONS ---
# Calculate LTV and dtir1
LTV = loan_amount / property_value if property_value else 0
dtir1 = (total_monthly_debt_payment / income) * 100 if income else 0

# Loan limit logic
conforming_limit = 25000000
loan_limit = 'CF' if loan_amount <= conforming_limit else 'NCF'

# Approval in advance transformation
approv_in_adv = 'pre' if approv_in_adv == "YES" else 'nopre'

# Income transformation (to dollars)
income_dollars = income / 325 if income else 0

# Business or commercial transformation
business_or_commercial_trans = 'b/c' if business_or_commercial == "Yes" else 'nob/c'

# Credit worthiness calculation
credit_worthiness = calculate_credit_worthiness(
    credit_score,                # credit_score
    income_dollars,              # income_usd
    dtir1,                       # dtir1
    open_credit,                 # open_credit
    loan_amount,                 # loan_amount_usd
    age,                         # age
    business_or_commercial_trans,# business_or_commercial
    property_value,              # property_value_usd
    LTV,                         # LTV
    term,                        # term
    rate_of_interest,            # rate_of_interest
    neg_ammortization,           # neg_ammortization
    interest_only,               # interest_only
    lump_sum_payment             # lump_sum_payment
)

# Interest rate spread
benchmark_rate = 6.5
interest_rate_spread = rate_of_interest - benchmark_rate

# Upfront charges (not used in model input)
upfront_charges = loan_amount * 0.01

if st.button("Predict Default"):
    # Prepare input for model
    input_dict = {
        'loan_limit': [loan_limit],
        'Gender': [gender],
        'LTV': [LTV],
        'dtir1': [dtir1],
        'approv_in_adv': [approv_in_adv],
        'Credit_Worthiness': [credit_worthiness],
        'credit_type': [credit_type],
        'co_applicant_credit_type': [co_applicant_credit_type],
        'Interest_rate_spread': [interest_rate_spread],
        'submission_of_application': [submission_of_application],
        'Region': [region]
    }

    input_df = pd.DataFrame(input_dict)
    input_processed = preprocess_input(input_df, X_columns)
    prediction = model.predict(input_processed)[0]
    st.success(f"Prediction: {'Default (Will not repay)' if prediction == 1 else 'No Default (Will repay)'}")




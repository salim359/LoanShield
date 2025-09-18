import streamlit as st
import joblib
import pandas as pd
from preprocessing import preprocess_input

model = joblib.load('best_loan_default_model.pkl')
X_columns = joblib.load('X_columns.pkl')  # Save X.columns during training

st.set_page_config(page_title="Loan Default Predictor", page_icon="💸", layout="centered")
st.title("Loan Default Prediction")
st.write("Enter loan and applicant details below to predict default risk.")

# Input fields for relevant features
loan_amount = st.number_input("Loan Amount", min_value=0.0)
rate_of_interest = st.number_input("Rate of Interest", min_value=0.0)
interest_rate_spread = st.number_input("Interest Rate Spread", min_value=0.0)
upfront_charges = st.number_input("Upfront Charges", min_value=0.0)
term = st.number_input("Term (months)", min_value=0)
neg_ammortization = st.selectbox("Negative Ammortization", ["Yes", "No"])
interest_only = st.selectbox("Interest Only", ["Yes", "No"])
lump_sum_payment = st.selectbox("Lump Sum Payment", ["Yes", "No"])
property_value = st.number_input("Property Value", min_value=0.0)
construction_type = st.selectbox("Construction Type", ["Type1", "Type2", "Other"])
occupancy_type = st.selectbox("Occupancy Type", ["Owner Occupied", "Rented", "Other"])
secured_by = st.selectbox("Secured By", ["Property", "Other"])
total_units = st.number_input("Total Units", min_value=1)
LTV = st.number_input("Loan to Value Ratio (LTV)", min_value=0.0, max_value=100.0)
income = st.number_input("Applicant Income", min_value=0.0)
credit_worthiness = st.selectbox("Credit Worthiness", ["Good", "Bad", "Average"])
credit_type = st.selectbox("Credit Type", ["Type1", "Type2", "Other"])
credit_score = st.number_input("Credit Score", min_value=0)
co_applicant_credit_type = st.selectbox("Co-applicant Credit Type", ["Type1", "Type2", "None"])
age = st.number_input("Applicant Age", min_value=18)
dtir1 = st.number_input("DTI Ratio (dtir1)", min_value=0.0)
open_credit = st.number_input("Open Credit Lines", min_value=0)
business_or_commercial = st.selectbox("Business or Commercial", ["Yes", "No"])
region = st.selectbox("Region", ["North", "South", "East", "West", "Other"])
year = st.number_input("Year", min_value=1900, max_value=2100)
loan_type = st.selectbox("Loan Type", ["Type1", "Type2", "Other"])
loan_purpose = st.selectbox("Loan Purpose", ["Home", "Business", "Other"])
submission_of_application = st.selectbox("Submission of Application", ["Online", "Offline"])
security_type = st.selectbox("Security Type", ["Type1", "Type2", "Other"])

if st.button("Predict Default"):
    # Prepare input for model
    input_dict = {
        'loan_amount': [loan_amount],
        'rate_of_interest': [rate_of_interest],
        'Interest_rate_spread': [interest_rate_spread],
        'Upfront_charges': [upfront_charges],
        'term': [term],
        'Neg_ammortization': [neg_ammortization],
        'interest_only': [interest_only],
        'lump_sum_payment': [lump_sum_payment],
        'property_value': [property_value],
        'construction_type': [construction_type],
        'occupancy_type': [occupancy_type],
        'Secured_by': [secured_by],
        'total_units': [total_units],
        'LTV': [LTV],
        'income': [income],
        'Credit_Worthiness': [credit_worthiness],
        'credit_type': [credit_type],
        'Credit_Score': [credit_score],
        'co-applicant_credit_type': [co_applicant_credit_type],
        'age': [age],
        'dtir1': [dtir1],
        'open_credit': [open_credit],
        'business_or_commercial': [business_or_commercial],
        'Region': [region],
        'year': [year],
        'loan_type': [loan_type],
        'loan_purpose': [loan_purpose],
        'submission_of_application': [submission_of_application],
        'Security_Type': [security_type]
    }

    input_df = pd.DataFrame(input_dict)
    input_processed = preprocess_input(input_df, X_columns)
    prediction = model.predict(input_processed)[0]
    st.success(f"Prediction: {'Default' if prediction == 1 else 'No Default'}")

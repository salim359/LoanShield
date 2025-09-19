import streamlit as st
import joblib
import pandas as pd
from functions import  preprocess_input ,calculate_credit_worthiness_business

st.set_page_config(page_title="Loan Default Predictor", page_icon="💸", layout="wide")

# --- Custom CSS for clickable cards ---
st.markdown(
    """
    <style>
    .card {
        border: 1px solid #e6e6e6;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        transition: transform 0.12s ease-in-out, box-shadow 0.12s ease-in-out;
        cursor: pointer;
        background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(250,250,250,1) 100%);
        margin-bottom: 10px;
    }
    .card:hover {
        transform: translateY(-6px);
        box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    }
    .card-title { font-size:20px; font-weight:600; margin-bottom:6px; }
    .card-desc { color:#666; font-size:14px; margin-bottom:12px; }
    .selected { border: 2px solid #2C7BE5 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if "selected" not in st.session_state:
    st.session_state.selected = None

st.title("💸 Loan Default Prediction")
st.write("Select loan type and enter applicant details to predict default risk.")

# --- Loan type selection ---
cols = st.columns(3)

cards = [
    {"title": "Personal Loan", "desc": "Small, short-term loans for individuals."},
    {"title": "Business Loan", "desc": "Working capital and growth loans for SMEs."},
    {"title": "Mortgage", "desc": "Long-term loans secured by property."},
]

for i, col in enumerate(cols):
    with col:
        card_html = f"""
        <div class='card {'selected' if st.session_state.selected == i+1 else ''}'>
            <div class='card-title'> {cards[i]['title']} </div>
            <div class='card-desc'> {cards[i]['desc']} </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        if st.button(f"Select {cards[i]['title']}", key=f"select_{i}"):
            st.session_state.selected = i + 1

st.write("---")

# --- Input fields ---


# Load appropriate model
if st.session_state.selected == 1:
    model = joblib.load("./models/personal_loan_default_model.pkl")
    X_columns = joblib.load("./models/personal_X_columns.pkl")
    
    credit_score = st.number_input("Credit Score", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    income = st.number_input("Applicant Income", min_value=0.0)
    open_credit = st.number_input("Open Credit Lines", min_value=0)
    age = st.number_input("Applicant Age", min_value=18)
    term = st.number_input("Term (months)", min_value=0)
    loan_amount = st.number_input("Loan Amount", min_value=0.0)
    total_monthly_debt_payment = st.number_input("Total Monthly Debt Payment", min_value=0.0)
    DTI= (total_monthly_debt_payment/income)*100 if income>0 else 0
    
    
    # --- Prediction ---
    if st.button("Predict Default"):
        input_dict = {
            "Credit_Score": [credit_score],
            "Gender": [gender],
            "Income": [income],
            "Open_Credit": [open_credit],
            "Age": [age],
            "Term": [term],
            "Loan_Amount": [loan_amount],
            "Total_Monthly_Debt_Payment": [total_monthly_debt_payment],
            "DTI": [DTI]
        }
    
        input_df = pd.DataFrame(input_dict)
        input_processed = preprocess_input(input_df, X_columns)
        prediction = model.predict(input_processed)[0]
    
        st.success(
            f"Prediction: {'❌ Default (High Risk)' if prediction == 1 else '✅ No Default (Low Risk)'}"
        )
    
elif st.session_state.selected == 2:
    model = joblib.load("./models/business_loan_default_model.pkl")
    X_columns = joblib.load("./models/business_X_columns.pkl")
    
    loan_amount = st.number_input("Loan Amount", min_value=0.0)
    loan_limit = "CF" if loan_amount <= 25000000 else "NCF"
    
    property_value = st.number_input("Property Value", min_value=0.0)
    LTV = loan_amount / property_value if property_value else 0
    income = st.number_input("Applicant Income", min_value=0.0)
    income_dollars = income / 325 if income else 0
    total_monthly_debt_payment = st.number_input("Total Monthly Debt Payment", min_value=0.0)
    dtir1 = (total_monthly_debt_payment / income_dollars) * 100 if income_dollars else 0
    
    credit_type = st.selectbox("Credit Type", ["CIB", "CRIF", "EXP", "EQUI"])
    
    rate_of_interest = st.number_input("Rate of Interest", min_value=0.0)
    benchmark_rate = 6.5
    interest_rate_spread = rate_of_interest - benchmark_rate
    business_or_commercial = st.selectbox("Business or Commercial", ["Yes", "No"])
    region = st.selectbox("Region", ["North", "South", "East", "West", "Other"])
    
    term = st.number_input("Term (months)", min_value=0)
    
    neg_ammortization = st.selectbox("Negative Amortization", ["Yes", "No"])
    interest_only = st.selectbox("Interest Only", ["Yes", "No"])
    lump_sum_payment = st.number_input("Lump Sum Payment", min_value=0.0)
   
    
    open_credit = st.number_input("Open Credit Lines", min_value=0)
    year = st.number_input("Year", min_value=1900, max_value=2100)
    submission_of_application = st.selectbox("Submission of Application", ["Online", "Offline"])
    
    # Credit details
    credit_score = st.number_input("Credit Score", min_value=0)
    
    business_or_commercial_trans = "b/c" if business_or_commercial == "Yes" else "nob/c"
    if st.session_state.selected == 2:
         credit_worthiness = calculate_credit_worthiness_business(
            credit_score,
            income_dollars,
            dtir1,
            open_credit,
            loan_amount,
            business_or_commercial_trans,
            LTV,
            term,
            rate_of_interest,
            neg_ammortization,
            interest_only,
            lump_sum_payment
        )
    else:
        credit_worthiness = "Not Applicable"
    
  
    
    upfront_charges = loan_amount * 0.01
    
    # --- Prediction ---
    if st.button("Predict Default"):
        input_dict = {
            "loan_limit": [loan_limit],
            "LTV": [LTV],
            "dtir1": [dtir1],
            "Credit_Worthiness": [credit_worthiness],
            "credit_type": [credit_type],
            "Interest_rate_spread": [interest_rate_spread],
            "Region": [region],
            "business_or_commercial": [business_or_commercial]
        }

    
        input_df = pd.DataFrame(input_dict)
        input_processed = preprocess_input(input_df, X_columns)
        prediction = model.predict(input_processed)[0]
    
        st.success(
            f"Prediction: {'❌ Default (High Risk)' if prediction == 1 else '✅ No Default (Low Risk)'}"
        )
else:
    model = joblib.load("./models/mortgage_default_model.pkl")
    X_columns = joblib.load("./models/mortgage_X_columns.pkl")

    loan_amount = st.number_input("Loan Amount", min_value=0.0)
    term = st.number_input("Term (months)", min_value=0)
    total_monthly_debt_payment = st.number_input("Total Monthly Debt Payment", min_value=0.0)
    rate_of_interest = st.number_input("Rate of Interest", min_value=0.0)
    
    neg_ammortization = st.selectbox("Negative Amortization", ["Yes", "No"])
    neg_ammortization="not_neg" if neg_ammortization=="No" else "neg_amm"
    
    interest_only = st.selectbox("Interest Only", ["Yes", "No"])
    interest_only="not_int" if interest_only=="No" else "int_only"
    
    lump_sum_payment = st.selectbox("Lump Sum Payment", ["Yes", "No"])
    lump_sum_payment = "not_lpsm" if lump_sum_payment=="No" else "lpsm"
    
    income = st.number_input("Applicant Income", min_value=0.0)
    income = income / 325 if income else 0
    
    # Credit details
    credit_score = st.number_input("Credit Score", min_value=0)
    
    # Property details
    property_value = st.number_input("Property Value", min_value=0.0)
    total_units = st.selectbox("Total Units", ["1U", "2U", "3U", "4U"])
    
    # --- Feature Engineering ---
    LTV = loan_amount / property_value if property_value else 0
    dtir1 = (total_monthly_debt_payment / income) * 100 if income else 0
    
    
    occupancy_type = st.selectbox("Occupancy Type", ["Owner", "Second Home", "Investment"])
    secured_by = st.selectbox("Secured By", ["home","land"])
    region = st.selectbox("Region", ["North", "South", "East", "West", "Other"])
    down_payment = property_value - loan_amount if property_value > loan_amount else 0
    
    benchmark_rate = 6.5
    interest_rate_spread = rate_of_interest - benchmark_rate
    DTI= (total_monthly_debt_payment/income)*100 if income>0 else 0
    occupancy_type = "pr" if occupancy_type=="Owner" else ("sr" if occupancy_type=="Second Home" else "ir")
    # --- Prediction ---
    if st.button("Predict Default"):
        input_dict = {
            'LTV': [LTV],
            'property_value':[property_value],
            'total_units':[total_units],
            'loan_amount':[loan_amount],
            'term':[term],
            'Interest_rate_spread':[interest_rate_spread],
            'DTI':[DTI],
            'Credit_Score':[credit_score],
            'down_payment':[down_payment],
            'occupancy_type':[occupancy_type],
            'Secured_by':[secured_by],
            'Region':[region],
            'income':[income],
            'Neg_ammortization':[neg_ammortization],
            'interest_only':[interest_only],
            'lump_sum_payment':[lump_sum_payment]
        }
    
        input_df = pd.DataFrame(input_dict)
        input_processed = preprocess_input(input_df, X_columns)
        prediction = model.predict(input_processed)[0]
    
        st.success(
            f"Prediction: {'❌ Default (High Risk)' if prediction == 1 else '✅ No Default (Low Risk)'}"
        )
def calculate_credit_worthiness(
    credit_score, income_usd, dtir1, open_credit, loan_amount_usd, age,
    business_or_commercial, property_value_usd, LTV, term, rate_of_interest,
    neg_ammortization, interest_only, lump_sum_payment
):
    score = 0

    # Credit score
    if credit_score >= 700:
        score += 2
    elif credit_score >= 600:
        score += 1

    # Income (in USD)
    if income_usd > (50000/325):
        score += 2
    elif income_usd > (30000/325):
        score += 1

    # DTI
    if dtir1 < 35:
        score += 2
    elif dtir1 < 45:
        score += 1

    # Open credit lines
    if open_credit <= 3:
        score += 1
    elif open_credit > 7:
        score -= 1

    # Loan amount vs property value (in USD)
    if loan_amount_usd < property_value_usd:
        score += 1

    # Age
    if age >= 30:
        score += 1

    # Business or commercial loan
    if business_or_commercial == "No":
        score += 1

    # LTV
    if LTV < 80:
        score += 1
    elif LTV > 90:
        score -= 1

    # Term
    if term < 240:
        score += 1

    # Rate of interest
    if rate_of_interest < 10:
        score += 1
    elif rate_of_interest > 15:
        score -= 1

    # Loan features
    if neg_ammortization == "No":
        score += 1
    if interest_only == "No":
        score += 1
    if lump_sum_payment == "Yes":
        score += 1

    # Final decision
    if score >= 10:
        return "Good"
    elif score >= 6:
        return "Average"
    else:
        return "Bad"
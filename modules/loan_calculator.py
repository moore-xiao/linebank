import numpy as np

def calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_months):
    """
    Calculate the monthly payment for a loan.
    
    Args:
        loan_amount: The principal loan amount
        annual_interest_rate: Annual interest rate in percentage (e.g., 5 for 5%)
        loan_term_months: Loan term in months
        
    Returns:
        Monthly payment amount
    """
    # Convert annual interest rate to monthly and decimal
    monthly_interest_rate = annual_interest_rate / 100 / 12
    
    # Calculate monthly payment using the formula
    if monthly_interest_rate == 0:
        return loan_amount / loan_term_months
    else:
        return loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / \
               ((1 + monthly_interest_rate) ** loan_term_months - 1)

def generate_payment_schedule(loan_amount, annual_interest_rate, loan_term_months, early_payment=0):
    """
    Generate amortization schedule for the loan.
    
    Args:
        loan_amount: The principal loan amount
        annual_interest_rate: Annual interest rate in percentage
        loan_term_months: Loan term in months
        early_payment: Amount of early payment per month (optional)
        
    Returns:
        List of dictionaries containing payment details for each month
    """
    monthly_interest_rate = annual_interest_rate / 100 / 12
    monthly_payment = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_months)
    
    remaining_balance = loan_amount
    payment_schedule = []
    
    for month in range(1, loan_term_months + 1):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        
        # Apply early payment if there's remaining balance after the regular payment
        current_early_payment = 0
        if early_payment > 0 and month == 1:  # Apply early payment in the first month
            current_early_payment = early_payment
            if current_early_payment > remaining_balance - principal_payment:
                current_early_payment = remaining_balance - principal_payment
        
        # Calculate remaining balance after regular payment
        remaining_balance -= principal_payment
        
        # Apply early payment
        if current_early_payment > 0:
            if current_early_payment > remaining_balance:
                current_early_payment = remaining_balance
            remaining_balance -= current_early_payment
        
        payment_schedule.append({
            'month': month,
            'payment': round(monthly_payment, 2),
            'principal': round(principal_payment, 2),
            'interest': round(interest_payment, 2),
            'early_payment': round(current_early_payment, 2) if current_early_payment > 0 else 0,
            'remaining_balance': round(remaining_balance, 2)
        })
        
        if remaining_balance <= 0:
            break
    
    return payment_schedule

def calculate_loan_payment(loan_amount, annual_interest_rate, loan_term_months, early_payment=0):
    """
    Calculate loan payment details including monthly payment and amortization schedule.
    
    Args:
        loan_amount: The principal loan amount
        annual_interest_rate: Annual interest rate in percentage
        loan_term_months: Loan term in months
        early_payment: Amount of early payment (optional)
        
    Returns:
        Tuple of (monthly_payment, payment_schedule, total_payment, total_interest, early_payment)
    """
    monthly_payment = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_months)
    payment_schedule = generate_payment_schedule(loan_amount, annual_interest_rate, loan_term_months, early_payment)
    
    # Calculate totals
    total_payment = sum(payment['payment'] for payment in payment_schedule)
    total_interest = sum(payment['interest'] for payment in payment_schedule)
    
    # Add early payment to total payment if it exists
    if early_payment > 0:
        total_payment += early_payment
    
    return round(monthly_payment, 2), payment_schedule, round(total_payment, 2), round(total_interest, 2), early_payment 
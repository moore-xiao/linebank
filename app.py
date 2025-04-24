from flask import Flask, render_template, request
from modules.loan_calculator import calculate_loan_payment
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    payment_schedule = None
    monthly_payment = None
    total_payment = None
    total_interest = None
    total_early_payment = None
    early_payments_input = {}
    form_data = {}
    
    if request.method == 'POST':
        # Store all form data to preserve input values
        form_data = {
            'loan_amount': request.form.get('loan_amount', ''),
            'interest_rate': request.form.get('interest_rate', ''),
            'loan_term': request.form.get('loan_term', ''),
            'processing_fee': request.form.get('processing_fee', ''),
            'start_date': request.form.get('start_date', '')
        }
        
        # Process single loan calculation
        loan_amount = float(request.form.get('loan_amount', 0))
        interest_rate = float(request.form.get('interest_rate', 0))
        loan_term = int(request.form.get('loan_term', 0))
        
        # Process processing fee if provided
        processing_fee = request.form.get('processing_fee', '')
        if processing_fee and float(processing_fee) > 0:
            processing_fee = float(processing_fee)
            # Deduct processing fee from loan amount
            effective_loan_amount = loan_amount - processing_fee
        else:
            processing_fee = 0
            effective_loan_amount = loan_amount
        
        # Process early payments
        early_payments = {}
        for key, value in request.form.items():
            if key.startswith('early_payment_') and value and float(value) > 0:
                try:
                    month = int(key.split('_')[2])
                    early_payments[month] = float(value)
                    early_payments_input[key] = value
                except (ValueError, IndexError):
                    pass
        
        monthly_payment, payment_schedule, total_payment, total_interest, total_early_payment = calculate_loan_payment(
            effective_loan_amount, interest_rate, loan_term, early_payments
        )
        
        # Add processing fee to total payment
        total_payment_with_fee = total_payment + processing_fee
        
        # Add dates to payment schedule if start date is provided
        start_date = request.form.get('start_date')
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            for i, payment in enumerate(payment_schedule):
                # Calculate the date for this payment (add i months to start date)
                payment_date = start_date.replace(year=start_date.year + ((start_date.month + i - 1) // 12),
                                               month=((start_date.month + i - 1) % 12) + 1)
                # Format date as string
                payment['date'] = payment_date.strftime('%Y-%m-%d')
        
        # Add processing fee to the context
        form_data['processing_fee_value'] = processing_fee
        form_data['effective_loan_amount'] = effective_loan_amount
        form_data['total_payment_with_fee'] = round(total_payment_with_fee, 2)
    
    return render_template('index.html', 
                          payment_schedule=payment_schedule,
                          monthly_payment=monthly_payment,
                          total_payment=total_payment,
                          total_interest=total_interest,
                          total_early_payment=total_early_payment,
                          early_payments_input=early_payments_input,
                          form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80) 
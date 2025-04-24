from flask import Flask, render_template, request, json
from modules.loan_calculator import calculate_loan_payment

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
            'loan_term': request.form.get('loan_term', '')
        }
        
        loan_amount = float(request.form.get('loan_amount', 0))
        interest_rate = float(request.form.get('interest_rate', 0))
        loan_term = int(request.form.get('loan_term', 0))
        
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
            loan_amount, interest_rate, loan_term, early_payments
        )
    
    return render_template('index.html', 
                          payment_schedule=payment_schedule,
                          monthly_payment=monthly_payment,
                          total_payment=total_payment,
                          total_interest=total_interest,
                          total_early_payment=total_early_payment,
                          early_payments_input=early_payments_input,
                          form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
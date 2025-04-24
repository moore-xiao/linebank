from flask import Flask, render_template, request
from modules.loan_calculator import calculate_loan_payment

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    payment_schedule = None
    monthly_payment = None
    total_payment = None
    total_interest = None
    early_payment = None
    
    if request.method == 'POST':
        loan_amount = float(request.form.get('loan_amount', 0))
        interest_rate = float(request.form.get('interest_rate', 0))
        loan_term = int(request.form.get('loan_term', 0))
        early_payment = float(request.form.get('early_payment', 0))
        
        monthly_payment, payment_schedule, total_payment, total_interest, early_payment = calculate_loan_payment(
            loan_amount, interest_rate, loan_term, early_payment
        )
    
    return render_template('index.html', 
                          payment_schedule=payment_schedule,
                          monthly_payment=monthly_payment,
                          total_payment=total_payment,
                          total_interest=total_interest,
                          early_payment=early_payment)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
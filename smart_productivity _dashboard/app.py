from flask import Flask, render_template, request, redirect, session
import pandas as pd
import os
from utils.analyze import get_summary

app = Flask(__name__)
app.secret_key = 'focusr_secret'

data_path = os.path.join("data", "employee_log.csv")
df = pd.read_csv(data_path)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "focusr123"

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin'):
        return redirect('/dashboard')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html', error=None)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    message = None
    if request.method == 'POST':
        email = request.form['email']
        message = f"If {email} is registered, a reset link has been sent."
    return render_template('forgot_password.html', message=message)

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/login')

    # Ensure all values are regular Python types
    employees = df['Name'].unique().tolist()
    chart_labels = employees
    chart_data = [int(df[df['Name'] == emp]['TasksCompleted'].sum()) for emp in employees]

    return render_template(
        'dashboard.html',
        employees=employees,
        chart_labels=chart_labels,
        chart_data=chart_data
    )

@app.route('/employee/<name>')
def employee(name):
    if not session.get('admin'):
        return redirect('/login')
    emp_data = df[df['Name'] == name]
    summary = get_summary(df, name)
    return render_template('employee.html', name=name, data=emp_data.to_dict(orient='records'), summary=summary)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

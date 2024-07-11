from flask import Flask, render_template, request, redirect, url_for, session
from soap_client import SoapClient
from rest_client import RestClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'

wsdl_url = "http://localhost/site/soap/soap_server.php?wsdl"
base_url = "http://localhost/site/api.php"
soap_client = SoapClient(wsdl_url)
rest_client = RestClient(base_url)

@app.route('/')
def index():
    if 'token' in session:
        return redirect(url_for('users'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        token = soap_client.authenticate(email, password)
        if token:
            session['token'] = token
            return redirect(url_for('users'))
        else:
            return render_template('login.html', error='Authentication failed.')
    return render_template('login.html')

@app.route('/users')
def users():
    if 'token' not in session:
        return redirect(url_for('login'))
    token = session['token']
    users = soap_client.list_users(token)
    return render_template('users.html', users=users, token=token)

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))

@app.route('/add_user', methods=['POST'])
def add_user():
    print("Form data received:", request.form)
    token = request.form['token']
    user = {
        'prenom': request.form['prenom'],
        'nom': request.form['nom'],
        'email': request.form['email'],
        'mot_de_passe': request.form['password'],
        'type': request.form['type']
    }
    soap_client.add_user(token, user)
    return redirect(url_for('users'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    token = request.form['token']
    user_id = request.form['user_id']
    soap_client.delete_user(token, user_id)
    return redirect(url_for('users'))

@app.route('/update_user', methods=['POST'])
def update_user():
    token = request.form['token']
    user = {
        'id': request.form['user_id'],
        'prenom': request.form['prenom'],
        'nom': request.form['nom'],
        'email': request.form['email'],
        'mot_de_passe': request.form['password'],
        'type': request.form['type']
    }
    soap_client.update_user(token, user)
    return redirect(url_for('users'))

if __name__ == "__main__":
    app.run(debug=True)

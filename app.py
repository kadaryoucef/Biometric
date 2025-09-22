from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import firebase_admin
from firebase_admin import credentials, auth
from functools import wraps
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random secret key

# Initialize Firebase Admin
cred = credentials.Certificate("firebase/biometrer-6e571-firebase-adminsdk-fbsvc-3f0f1f9a01.json")
firebase_admin.initialize_app(cred)

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'user_token' not in session:
			return redirect(url_for('login'))
		try:
			# Verify the Firebase token
			decoded_token = auth.verify_id_token(session['user_token'])
			session['user_id'] = decoded_token['uid']
		except:
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function

@app.route('/verify-token', methods=['POST'])
def verify_token():
	try:
		id_token = request.json['idToken']
		# Verify the token
		decoded_token = auth.verify_id_token(id_token)
		session['user_token'] = id_token
		session['user_id'] = decoded_token['uid']
		return jsonify({'status': 'success'})
	except Exception as e:
		return jsonify({'status': 'error', 'message': str(e)}), 401

@app.route('/')
@login_required
def index():
	return render_template('tast1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user_token' in session:
		return redirect(url_for('index'))
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('login'))

@app.route('/driving-license')
@login_required
def driving_license():
	return render_template('driving-license.html')

@app.route('/passport')
@login_required
def passport():
	return render_template('passport.html')

@app.route('/national-id')
@login_required
def national_id():
	return render_template('national-id.html')

@app.route('/statistics')
@login_required
def statistics():
	return render_template('statistics.html')

@app.route('/secretariat')
@login_required
def secretariat():
	return render_template('secretariat.html')

@app.route('/vehicle-registration')
@login_required
def vehicle_registration():
	return render_template('vehicle-registration.html')

@app.route('/administrative-certificate')
@login_required
def administrative_certificate():
	return render_template('tast3.html')

if __name__ == '__main__':
	app.run(debug=True)
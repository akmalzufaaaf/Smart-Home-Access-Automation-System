from flask import Flask, render_template, redirect, request, url_for, session
from mongodb import users_collection, logs_collection, admins_collection
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = admins_collection.find_one({
            "username": request.form['username'],
            "password": request.form['password']
        })
        if user:
            session['user'] = user['username']
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/users')
def users():
    if 'user' not in session:
        return redirect('/')
    user_data = list(users_collection.find())
    return render_template('users.html', users=user_data)

@app.route('/logs')
def logs():
    if 'user' not in session:
        return redirect('/')
    log_data = list(logs_collection.find().sort("timestamp", -1))
    return render_template('logs.html', logs=log_data)

import paho.mqtt.publish as publish

@app.route('/open-door', methods=['POST'])
def open_door():
    publish.single("smartdoor/command", "open", hostname="mqtt-broker-service")
    logs_collection.insert_one({
        "user": "Admin Remote",
        "method": "MQTT Command",
        "status": "Request Sent",
        "timestamp": datetime.now()
    })
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

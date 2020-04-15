from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage

app = Flask(__name__)

#admin routing for Flask

@app.route('/userhome')
def userhome(name):
   return render_template('userhome.html', name =name)

@app.route('/')
def splash(): 
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/validate', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
       if (len(request.form['fname']) != 0 and len(request.form['password']) != 0):
            user = request.form['fname']
            password = request.form['password']
            return userhome(user)
       else: 
            error = "Invalid input data"
            return redirect(url_for('error'))
   
   return redirect(url_for('error'))


if __name__ == '__main__':
    # Configures database and gets access to the database
    cred = credentials.Certificate('ServiceAccountKey.json')
    firebase_admin.initialize_app(cred)
    

    # Initialize the client for interfacing with the database
    DB = firestore.client()
    
    app.run()
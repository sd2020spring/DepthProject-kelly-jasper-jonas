from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
from User import *
from Item import *

app = Flask(__name__)


@app.route('/')
def splash(): 
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
	return render_template("signup.html")

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/validatelogin', methods = ['POST', 'GET'])
def validate_login():
   if request.method == 'POST':
       if (len(request.form['email']) != 0 and len(request.form['password']) != 0): #validation TODO
            user = request.form['email']
            password = request.form['password']
            return userhome(user)
       else: 
            error = "Invalid input data"
            return redirect(url_for('error'))
   
   return redirect(url_for('error'))

@app.route('/validatesignup', methods = ['POST', 'GET'])
def validate_signup():
   if request.method == 'POST':
       if 0 in {len(request.form['fname']), len(request.form['lname']), len(request.form['email']), len(request.form['school']), len(request.form['password'])}: 
            error = "Invalid input data"
            return redirect(url_for('error'))
       else: 
            user=User(request.form['fname'],request.form['lname'],request.form['email'],request.form['school'],request.form['phone'],request.form['password'])
            DB.collection(u'Users').add(user.to_dict()) 
            
            return userhome(user)
   
   return redirect(url_for('error'))

@app.route("/home/<userid>")#displays unique homepage for user
def userhome(user):
    return render_template("userhome.html")

@app.route("/list/<userid>") # list an item yourself here
def list():
	"""List an item to the marketplace
	- will probably be an html form

	"""
	return render_template("list.html")

@app.route("/item/<userid>/<item>") # view an item listing
def listing(item):
	return render_template("listing.html",item=item)


if __name__ == '__main__':
    # Configures database and gets access to the database
    cred = credentials.Certificate('ServiceAccountKey.json')
    firebase_admin.initialize_app(cred)
    

    # Initialize the client for interfacing with the database
    DB = firestore.client()

    #test if firebase connection is working
    # doc_ref = DB.collection(u'Users').limit(1)

    # try:
    #     docs = doc_ref.get()
    #     for doc in docs:
    #         print(u'Doc Data:{}'.format(doc.to_dict()))
    # except google.cloud.exceptions.NotFound:
    #     print(u'Missing data')
        
    app.run()

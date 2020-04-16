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


@app.route("/sign-up")
def signup():
	return render_template("sign-up.html")

@app.route("/search/?=<query>") # results page from a search
def search(query):
	return render_template("search.html",results=results)

@app.route("/list") # list an item yourself here
def list():
	"""List an item to the marketplace
	- will probably be an html form

	"""
	return render_template("list.html")

@app.route("/item/<item>") # view an item listing
def listing(item):
	return render_template("listing.html",item=item)

@app.route("/checkout") # checkout with current items
def checkout(items):
	return render_template("checkout.html")

@app.route("/thank-you") # purchase confirmation
def purchaseSuccess():
	return render_template("thank-you.html")

@app.route("/purchase-error") # purchase fail alert
def purchaseError():
	return render_template("purchase-error.html")


if __name__ == '__main__':
    # Configures database and gets access to the database
    cred = credentials.Certificate('ServiceAccountKey.json')
    firebase_admin.initialize_app(cred)
    

    # Initialize the client for interfacing with the database
    DB = firestore.client()
    
    app.run()

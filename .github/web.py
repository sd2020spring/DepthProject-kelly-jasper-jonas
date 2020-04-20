from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from User import *
from Item import *

app = Flask(__name__)

def get_all_items():
  '''Gets all the items in Items DB
     Returns them as a list of dictionaries'''
  items = DB.collection(u'Items').stream()
  items_list = []
  for item in items:
    item_dict = item.to_dict()
    item_dict.update({'id':item.id})
    items_list.append(item_dict)
  return items_list

def login_validate(email, password):
    users = DB.collection(u'Users').stream()
    for user in users:
        if user.get('password') == password and user.get('email') == email:
            return True, user.id
    return False, user.id

def check_email(email): #checks if the email a user is signing up with is in the approved list (makes sure they're a student)
    emails = DB.collection(u'Emails').stream()
    for e in emails:
        if email == e.get('email') and not e.get('taken'):
            return True
    return False

@app.route('/')
def splash(): 
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
	return render_template("signup.html")

@app.route('/loginerror')
def loginerror():
    return render_template('loginerror.html')

@app.route('/signuperror')
def signuperror():
    return render_template("loginerror.html")

@app.route('/validatelogin', methods = ['POST', 'GET'])
def validate_login():
   if request.method == 'POST':
       valid, userid = login_validate(request.form['email'], request.form['password'])
       if valid: 
            return redirect(url_for("userhome",userid=userid))
       else: 
            error = "Incorrect username or password"
            return redirect(url_for('loginerror'))

   return redirect(url_for('error'))

@app.route('/validatesignup', methods = ['POST', 'GET'])
def validate_signup():
   if request.method == 'POST':
       if 0 not in {len(request.form['fname']), len(request.form['lname']), len(request.form['email']), len(request.form['school']), len(request.form['password'])}: 
            if check_email(request.form['email']) and request.form['password'] == request.form['confirmpass']:
                user=User(request.form['fname'],request.form['lname'],request.form['email'],request.form['password'],request.form['school'],request.form['phone'])
                DB.collection(u'Users').add(user.to_dict())   
                return redirect(url_for("login")) #user must log in after creating account
            else:
                error = "invalid email or password confirmation"
                redirect(url_for('signuperror'))
       else:
            error = "Missing fields"
            return redirect(url_for('signuperror'))
            
   
   return redirect(url_for('signuperror'))

@app.route("/userhome/<userid>")#displays unique homepage
def userhome(userid):
    first_name = DB.collection(u'Users').document(userid).get().get('fname')
    items = get_all_items()
    return render_template("userhome.html", user_id=userid, name=first_name, items = items)

@app.route("/list/<userid>") # list an item yourself here
def list():
	"""List an item to the marketplace
	- will probably be an html form
	"""
	return render_template("list.html")

@app.route("/item/<userid>/<itemid>") # view an item listing
def item(userid, itemid):
  item = DB.collection(u'Items').document(itemid).get().to_dict()
  return render_template("item.html", item=item, itemid=itemid, user_id=userid)


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

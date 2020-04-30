"""
Supporting Code for Frank's List,
an open source webapp for buying and
selling items across college campuses.

@author(s): 
Jasper Katzban, Olin '23
Jonas Kazlauskas, Olin '23
Kelly Yen, Olin '23
"""

import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
import firebase_admin
from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion
from firebase_admin import credentials, firestore, auth, storage
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from User import *
from Item import *
from datetime import timedelta

app = Flask(__name__)
app.secret_key="JKKYJK"
app.permanent_session_lifetime = timedelta(days=2) #how long session lasts

def get_all_items():
    '''
    Gathers all the items in the DB

    Returns:
            All DB items in a list of dictionaries
    '''
    items = DB.collection(u'Items').get()
    items_list = []
    for item in items:
        item_dict = item.to_dict()
        print(item_dict['available'])
        if item_dict['available']: 
            items_list.append(item_dict)
    return items_list

def get_items(userid, field):
    '''
    Gathers all items that a user has saved

    Returns:
            All DB items in a list of dictionaries
    '''
    user_ref = DB.collection(u'Users').document(userid)
    items = user_ref.get().get(field)
    items_list = []
    for itemid in items:
        item = DB.collection(u'Items').document(itemid).get().to_dict()
        items_list.append(item)
    return items_list

def login_validate(email, password_attempt):
    ''' 
    Validates login by checking for matching email and password
    
    Returns:
            -True/False: whether login credentials are valid
            -user.id: id of user 
    '''
    users = DB.collection(u'Users').stream()
    for user in users:
        if check_password_hash(user.get('password'), password_attempt) and user.get('email') == email:
            return True, user.id
    return False, ""

def check_email(email): 
    '''
    Checks if the email a user is signing up with is approved (whether they're a student or not)

    Returns:
            True if email is approved and not taken, False otherwise
    '''
    emails = DB.collection(u'Emails').stream()
    for e in emails:
        if email == e.get('email') and not e.get('taken'):
            return True
    return False

def save_item(itemid, userid):
    '''
    Adds or removes item to user saved list in DB
    '''
    user_ref = DB.collection(u'Users').document(userid)
    user_saved = user_ref.get().get('saved_items')
    if user_saved == None or itemid not in user_saved:
        user_ref.set({
            u'saved_items': ArrayUnion([itemid])
        }, merge = True)
        flash('Saved to your profile')
    else:
        user_ref.set({
            u'saved_items': ArrayRemove([itemid])
        }, merge = True)
        flash('Removed from your profile')
    return None

def get_media_link(filename):
    image_blob = bucket.get_blob(filename)
    image_blob.make_public()
    return image_blob.media_link

def get_uploaded_images(images):
    print(len(images))
    uploaded_images = []
    for image in images:
        uploaded_images.append(upload_image(image, "item"))

    return uploaded_images

def upload_image(image, folder):
    unique = str(uuid.uuid4())
    if not os.path.exists(folder):
        os.mkdir(folder)

    image_filepath = os.path.join(app.config['UPLOAD_FOLDER'],folder, image.filename)
    image.save(image_filepath)
    filetype = image.content_type.split("/")[1]
    print(image.content_type)
    new = str(folder + "/" + unique + "." + filetype)
    os.rename(image_filepath, new)
    
    
    blob = bucket.blob(new)
    blob.upload_from_filename(new)

    # Deletes image from local directory after it was uploaded
    os.remove(new)

    return get_media_link(new)

def pull_images(itemid):
    images_src = DB.collection(u'Items').document(itemid).get().get('images')
    return images_src

def unlist(itemid, userid):
    item_ref = DB.collection(u'Items').document(itemid)
    user_ref = DB.collection(u'Users').document(userid)
    item_ref.update({u'available': False})
    user_ref.update({u'selling':ArrayRemove([itemid])})

@app.route('/')
def splash(): 
    '''Displays the landing page and prompts user to sign up or log in'''
    return render_template('index.html')

@app.route('/login')
def login():
    ''' Checks if user is already logged into a session, if not asks them to log in'''
    if "userid" in session:
        return redirect(url_for("userhome"))
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    '''log out of session and redirects to log in page'''
    session.pop("userid", None)
    return(redirect(url_for("login")))

@app.route("/signup")
def signup():
    '''Displays sign up page'''
    return render_template("signup.html")

@app.route('/loginerror')
def loginerror():
    '''Displays an error if user logs in with invalid credentials'''
    return render_template('loginerror.html')

@app.route('/signuperror')
def signuperror():
    '''Displays an error if user signs up with invalid credentials'''
    return render_template("loginerror.html")

@app.route('/validatelogin', methods = ['POST', 'GET'])
def validate_login():
    '''
    Validates a user's log in
    if user provided valid credentials, renders the userhome page, otherwise redirects to login error'''
    if request.method == 'POST':
       valid, userid = login_validate(request.form['email'], request.form['password'])
       if valid:
            session.permanent = True
            session['userid'] = userid
            return redirect(url_for("userhome"))
       else: 
            error = "Incorrect username or password"
            return redirect(url_for('loginerror'))
        
    return redirect(url_for('error'))

@app.route('/validatesignup', methods = ['POST', 'GET'])
def validate_signup():
    '''validates sign up by checking to make sure all fields are filled out properly, email belongs to a student, and password matches confirmed password'''
    if request.method == 'POST':
        if check_email(request.form['email']) and request.form['password'] == request.form['confirmpass']:
            
            hashed = generate_password_hash(request.form['password'])

            user=User(request.form['fname'],request.form['lname'],request.form['email'],hashed,request.form['school'],request.form['phone'])
            DB.collection(u'Users').add(user.to_dict())   

            return redirect(url_for("login")) #user must log in after creating account
        else:

            error = "Invalid email or password confirmation"
            redirect(url_for('signuperror'))
    return redirect(url_for('signuperror'))

@app.route('/validatelisting', methods = ['POST', 'GET'])
def validate_listing():
    if request.method == 'POST':
        userid = session['userid']
        itemref = DB.collection(u'Items').document()
        user_ref = DB.collection(u'Users').document(userid)

        new_item = Item(
            request.form['name'], 
            request.form['price'], 
            request.form['description'],
            request.form['category'],
            get_uploaded_images(request.files.getlist('picture')), 
            request.form['quality'], 
            userid, itemref.id)
        print(dir(DB.collection(u'Items').document()))

        user_ref.update({
            u'selling': ArrayUnion([itemref.id])
        })
        itemref.set(new_item.to_dict())
        flash('New listing added')
        return redirect(url_for('userhome'))
    else:
        pass

@app.route("/userhome", methods = ['POST', 'GET'])
def userhome():
    '''displays the user homepage, which consists of item listings and navbar'''
    if "userid" in session:
        userid = session['userid']
        user_ref = DB.collection(u'Users').document(userid)
        first_name = user_ref.get().get('fname')
        items = get_all_items()
        if request.method == 'POST':
            save_item(request.form['itemid'], userid)
        user_saved = user_ref.get().get('saved_items')
        return render_template("userhome.html", user_id=userid, name=first_name, items = items, user_saved = user_saved)
    else:
        return redirect(url_for("login"))

@app.route("/edituser", methods=['POST', 'GET'])
def edituser():
    '''Displays form for user to edit their information'''
    if "userid" in session:
        userid = session['userid']
        user_info = DB.collection(u'Users').document(userid).get().to_dict()
        if request.method == 'POST':
            if 0 in {len(request.form['fname']), len(request.form['lname']), len(request.form['email']), len(request.form['school'])}:
                flash(u'Oops! Name, email, and school name are required!', 'error')
                return render_template("edituser.html", user_id=userid, user_info=user_info)
            #User info changed
            user_ref = DB.collection(u'Users').document(userid)
            password = request.form['password']
            #Check if password was changed
            if len(request.form['password']) == 0:
                password = DB.collection(u'Users').document(userid).get().get('password')
            #Check if passwords match
            if request.form['password'] != request.form['confirmpass']:
                flash(u'Oops! New passwords do not match!', 'error')
                return render_template("edituser.html", user_id=userid, user_info=user_info)
            if check_email(request.form['email']):
                user_info=User(request.form['fname'],
                               request.form['lname'],
                               request.form['email'],
                               password,
                               request.form['school'],
                               request.form['phone'])
                user_ref.set(user_info.to_dict(), merge = True)
                flash('Your information was succesfully updated')
            else:
                flash(u'Invalid Email', 'error')
        return render_template("edituser.html", user_id=userid, user_info=user_info)
    else:
        return redirect(url_for("login"))

@app.route("/list")
def list_item():
    '''displays form for user to list new item'''
    if 'userid' in session:
        categories = DB.collection(u'Categories').document('categories').get().get('categories')
        return render_template("list.html", categories = categories)
    else:
        return redirect(url_for("login"))

@app.route("/wishlist", methods = ['POST', 'GET'])
def wishlist():
    '''displays user saved items'''
    if 'userid' in session:
        userid = session['userid']

        if request.method == 'POST':
            save_item(request.form['itemid'], userid)

        user_items_list = get_items(userid, "saved_items")
        return render_template("wishlist.html", user_items_list = user_items_list)
    else:
        return redirect(url_for("login"))

@app.route("/selling", methods = ['POST', 'GET'])
def sellinglist():
    '''display items user is selling'''
    if "userid" in session:
        userid = session['userid']
        if request.method == 'POST':
            unlist(request.form['itemid'], userid)
        user_selling_list = get_items(userid, "selling")
        return render_template("selling.html", user_selling_list=user_selling_list)
    else:
        return redirect(url_for("login"))

@app.route("/purchases", methods = ['POST', 'GET'])
def purchased():
    '''display items user has purchased in the past'''
    if "userid" in session:
        userid = session['userid']
        user_bought = get_items(userid, "purchases")
        return render_template("purchases.html", user_bought=user_bought)
    else:
        return redirect(url_for("login"))

@app.route("/item/<itemid>") 
def item(itemid):
    '''displays one item's information in depth'''
    if "userid" in session:
        userid = session['userid']
        item = DB.collection(u'Items').document(itemid).get().to_dict()
        images = pull_images(itemid)
        return render_template("item.html", item=item, itemid=itemid, images=images)
    else:
        return redirect(url_for("login"))

if __name__ == '__main__':
    # Configures database and gets access to the database
    cred = credentials.Certificate('ServiceAccountKey.json')

    firebase_admin.initialize_app(cred, {
    'storageBucket': 'depth-project-jkjkky.appspot.com'
    })

    # Initialize the client for interfacing with the database
    DB = firestore.client()
    bucket = storage.bucket()

    UPLOAD_FOLDER = os.getcwd()
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    #test if firebase connection is working
    # doc_ref = DB.collection(u'Users').limit(1)
    # try:
    #     docs = doc_ref.get()
    #     for doc in docs:
    #         print(u'Doc Data:{}'.format(doc.to_dict()))
    # except google.cloud.exceptions.NotFound:
    #     print(u'Missing data')
        
    app.run(debug=True)

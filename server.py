"""
Author : Hrishikesh S.
"""
from flask import (
    Flask,
    render_template,
    url_for,
    Markup,
    send_from_directory,
    flash,
    request
)
import os
import json
from werkzeug import secure_filename

http_methods = ['GET', 'POST']

#Markup('<h1><strong>Hello!</strong></h1>')

#create application instance
app = Flask(__name__, template_folder = "templates")
#secret key for sessions
app.secret_key = os.urandom(16)

#@app.errorhandler(404)
#def error_404():
#    print("Not working")

#declarator
#localhost:5000/homePage.html
@app.route('/homePage.html')
def home():
    #flash("Works!")
    #print(os.listdir())
    return render_template('homePage.html')

#for cate1, cate2 and cate3, the upload button is not rendering properly
#also need to the HTML page to load the images with the upvote button and name of user
#localhost:5000/cate1.html
@app.route('/cate1.html')
def cate1():
    #print(os.listdir())
    return render_template('cate1.html')

#localhost:5000/cate2.html
@app.route('/cate2.html')
def cate2():
    #print(os.listdir())
    return render_template('cate2.html')

#localhost:5000/cate3.html
@app.route('/cate3.html')
def cate3():
    #print(os.listdir())
    return render_template('cate3.html')

#localhost:5000/upload.html
@app.route('/upload.html')
def upload():
    return render_template('upload.html')

#localhost:5000/uploadImage
#need to fix this
@app.route('/uploadImage', methods = http_methods)
def uploadFile():
    #sub routine not working
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        print('File uploaded successfully')
    return render_template('homePage.html')

#needs fixing on HTML & CSS side immediately
@app.route('/login.html')
def login():
    return render_template('login.html')

#needs fixing on HTML & CSS side immediately
@app.route('/register.html')
def register():
    return render_template('register.html')

#add user
@app.route('/api/v1/users', methods = http_methods)
def addUser():
    if(request.method == 'POST'):
        print("Receiving data....")
        u_data = request.args.get('username')
        u_password = request.args.get('password')
        data = dict()
        data['username'] = u_data
        data['password'] = u_password
        file = "data/users/" + u_data + ".json"
        with open(file, 'w') as fp:
            json.dump(data, fp, sort_keys = True, indent = 4)
        message = u_data + ' has been added'
        return message
    else:
        return 'Invalid Request'

#remove user
@app.route('/api/v1/users/<username>', methods = ['DELETE'])
def removeUser(username):
    #username = "kvs"
    if(request.method == 'DELETE'):
        print("Receiving data....")
        print('OBJECTIVE : ', username)
        folder = os.listdir('data/users/')
        print(folder)
        target = username + ".json"
        found = False
        for i in folder:
            if(i == target):
                found =  True
                os.remove('data/users/'+target)
                message = username + ' has been removed'
                return message
        if(found == False):
            return username + ' not found'
    else:
        return 'Invalid Request'
"""
#list all categories
@app.route('/api/v1/categories', methods = http_methods)

#add a category
@app.route('/api/v1/categories/<username>')

#remove a category
@app.route('/api/v1/categories/<username>')

#list acts for a given category
@app.route('/api/v1/categories/<categoryName>/acts')

#list number of acts for a given category
@app.route('/api/v1/categories/<categoryName>/acts/size')

#return number of acts for a given category in a given range(inclusive)
@app.route('/api/v1/categories/<categoryName>/acts?start=<startRange>&end=<endRange>')

#upvote an act
@app.route('/api/v1/acts/upvote')

#remove an act
@app.route('/api/v1/acts/<actId>')

#upload an act
@app.route('/api/v1/acts')
"""

if __name__ == '__main__':
    app.run(debug = True)

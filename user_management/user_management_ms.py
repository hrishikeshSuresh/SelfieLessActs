"""
Authors : Hrishikesh S.   01FB16ECS139
          Karthik A.      01FB16ECS159
Status  : back-end front-end communications are mostly working
          need to add upvote button to catetemplate.html and make upvote working
          pass ip_address and port_no as arguments (OPTIONAL)
Notes   : # for developer's comment/insight
          ## for removing code
          Modify IP address & Port before running with act_management_ms.py
          To access the V.M., get the .pem key and run
                $ ssh -i "MYOSHLinux.pem" ubuntu@ec2-54-208-40-27.compute-1.amazonaws.com
          Run pre-run.sh before running this code on terminal/CMD PROMPT
"""
# I.P. address should be a string
ip_address = '54.208.40.27'
# port number should be a number
port_no = 80

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
from werkzeug import secure_filename, exceptions
import datetime
import shutil
import base64
import binascii
import re
import requests

http_methods = ['GET', 'POST']

n_http_requests = 0

##Markup('<h1><strong>Hello!</strong></h1>')

"""
General Functions
"""
def checkCategory(categoryName):
    path = "./data/categories/"
    cats = os.listdir(path)
    if categoryName in cats:
        return 1
    return 0

def checkUser(username):
    path = "./data/users/users.json"
    with open(path) as json_file:
        data = json.load(json_file)
    for user in data['users']:
        if(username == user['username']):
            return 1
    return 0

def checkId(actId):
    path = "./data/categories/"
    list_cat = os.listdir(path)
    for cat in list_cat:
        new_path = path + cat + '/' + cat + ".json"
        with open(new_path) as json_file:
            data = json.load(json_file)
            length = len(data['acts'])
            for i in range(length):
                if(data['acts'][i]['actId'] == actId):
                    return 1
    return 0

# create application instance
app = Flask(__name__, template_folder = "templates")
# generating a secret key for sessions
app.secret_key = os.urandom(16)

@app.errorhandler(exceptions.BadRequest)
def error_400(e):
    return 'bad request', 400

@app.errorhandler(401)
def error_401(e):
    return 'Unauthorized', 401

@app.errorhandler(exceptions.NotFound)
def error_404(e):
    return 'Not Found', 404

@app.errorhandler(exceptions.MethodNotAllowed)
def error_405(e):
    return 'Method Not Allowed', 405

@app.errorhandler(exceptions.RequestEntityTooLarge)
def error_413(e):
    return 'Request Entity too large', 413

# front-end supports
# localhost:5000/homePage.html
@app.route('/homePage')
def homeSupport():
    #flash("Works!")
	#print(os.listdir())
	f = os.listdir('data/categories')
	return render_template('homePage.html', categories = f, ip_address = ip_address, port_no = port_no)

# signup / add user webpage
# localhost:5000/signup
@app.route('/signup')
def signUpSupport():
    return render_template('signup.html', ip_address = ip_address, port_no = port_no)

# remove user webpage
# localhost:5000/rmuser.html
@app.route('/rmuser')
def removeUserSupport():
    return render_template('rmuser.html', ip_address = ip_address, port_no = port_no)

# upload webpage
# localhost:5000/upload.html
@app.route('/upload')
def uploadSupport():
    f = os.listdir('data/categories')
    return render_template('upload.html', categories = f, ip_address = ip_address, port_no = port_no)

# add category webpage
# localhost:5000/addcat.html
@app.route('/addcat')
def addCategorySupport():
    return render_template('addcat.html', ip_address = ip_address, port_no = port_no)

# list all acts
@app.route('/listallacts')
def listallactsSupport():
    f = os.listdir('data/categories')
    return render_template('listallacts.html', categories = f, ip_address = ip_address, port_no = port_no)

# remove category webpage
# localhost:5000/rmcategory
@app.route('/rmcategory')
def removeCategorySupport():
    f = os.listdir('data/categories')
    return render_template('rmcat.html', categories = f, ip_address = ip_address, port_no = port_no)

# list number of acts webpage
# localhost:5000/listnoofacts.html
@app.route('/listnoofacts')
def displaylistnoonactsSupport():
    f = os.listdir('data/categories')
    return render_template('listnoofacts.html', categories = f, ip_address = ip_address, port_no = port_no)

# list number of acts range webpage
# localhost:5000/listnoofactsrange.html
@app.route('/listactsrange')
def displaylistnoonactsrangeSupport():
    f = os.listdir('data/categories')
    return render_template('listactsrange.html', categories = f, ip_address = ip_address, port_no = port_no)

# remove acts
@app.route('/rmact')
def rmactSupport():
    return render_template('rmact.html', ip_address = ip_address, port_no = port_no)

# display category
@app.route('/display/<categoryName>')
def categoryDisplaySupport(categoryName):
    cat = os.listdir('./data/categories')
    curr_path = './data/categories/'+categoryName
    file = os.listdir(curr_path)
    with open(curr_path + '/' + file[0]) as json_file:
        data = json.load(json_file)
    ##print(data)
    for i in data['acts']:
        ##i['imgB64'] = base64.b64decode(i['imgB64'])
        print(i['actId'],i['upvotes'])
    return render_template('catetemplate.html', categories = cat, image_data = data['acts'], catName = categoryName, ip_address = ip_address, port_no = port_no)

"""
APIs
"""

# add user
# checked
# front-end done
@app.route('/api/v1/users', methods = ['POST'])
def addUser():
    global n_http_requests
    n_http_requests = n_http_requests + 1
    if(request.method == 'POST'):
        ##print(request.__dict__)
        print("Receiving data....")
        data = request.data.decode()
        ##print(type(data))
        ##print(request.form['username'], request.form['password'])
        if(data != ""):
            print("Not from front-end")
            data = data.split(sep = ',')
            u_data = data[0].split(sep = ':')[1]
            u_password = data[1].split(sep = ':')[1]
            u_data = u_data.lstrip()
            u_data = u_data.rstrip()
            u_data = u_data.replace("\"", "")
            u_data = u_data.replace("\t", "")
            u_data = u_data.replace("\n", "")
            u_password = u_password.lstrip()
            u_password = u_password.rstrip()
            u_password = u_password.replace("\"", "")
            u_password = u_password.replace("\t", "")
            u_password = u_password.replace("\n", "")
            u_password = u_password.replace("}", "")
            print(u_data, u_password)
            # check if SHA1 password
            pattern = re.compile(r'\b[0-9a-f]{40}\b')
            match = re.match(pattern, u_password)
            ##print(match)
            if(match == None):
                return "not SHA1 password"
        else:
            print("from front-end")
            u_data = request.form['username']
            u_password = request.form['password']
            print(u_data, u_password)
        flag = False
        file = os.listdir('./data/users')
        ##print("This is file ---> ",file)
        with open('./data/users/'+file[0]) as json_file:
            ##print("Opening a file is done")
            data = json.load(json_file)
        ##print("This is data -->",data)
        list_of_users = requests.get('http://' + ip_address + ':' + str(port_no) + '/api/v1/users')
        list_of_users = list_of_users.text
        list_of_users = list_of_users[1:-1].replace('\'','').replace(', ',',').split(sep = ",")
        print(list_of_users)
        for u in list_of_users:
            ##print(u)
            if(u_data in u):
                print("Match")
                return "user already exists"
        ##if(checkUser(u_data)):
            ##return "user already exists."
        dictionary = {}
        dictionary["username"] = u_data
        dictionary["password"] = u_password
        data['users'].append(dictionary)
        with open('./data/users/'+file[0],'w') as json_file:
            data = json.dump(data, json_file,indent = 4)
        message = u_data + ' has been added'
        return message
    else:
        return 'Invalid Request'

# remove user
# checked
# front-end done
@app.route('/api/v1/users/<username>', methods = ['DELETE'])
def removeUser(username):
    global n_http_requests
    n_http_requests = n_http_requests + 1
    if(request.method == 'DELETE'):
        print("Receiving data....")
        if(username == None):
            return "username returned None"
        print('OBJECTIVE : ', username)
        file = os.listdir('./data/users/')
        with open('./data/users/'+file[0]) as json_file:
            data = json.load(json_file)
        ##print("data is --> ",data)
        list_of_users = requests.get('http://' + ip_address+ ':' + str(port_no) + '/api/v1/users')
        list_of_users = list_of_users.text
        list_of_users = list_of_users[1:-1].replace('\'', '').replace(', ', ',').split(sep = ",")
        print(list_of_users)
        present = False
        for u in list_of_users:
            if(username == u):
                present = True
                break
        if(present == False):
            return "user does not exists"
        ##if(not checkUser(username)):
            ##return "user does not exists."
        arr = data['users']
        arr [:] = [d for d in arr if d.get('username') != username]
        data['users'] = arr
        with open('./data/users/'+file[0], 'w') as data_file:
            data= json.dump(data, data_file,indent = 4)
        return username + ' removed successfully'
        ##print(folder)
        ##target = username + ".json"
        ##found = False
        ##for i in folder:
        ##    if(i == target):
        ##        found =  True
        ##        os.remove('data/users/'+target)
        ##        message = username + ' has been removed'
        ##        return message
        ##if(found == False):
        ##    return username + ' not found'
    else:
        return 'Invalid Request'

# list all users
@app.route('/api/v1/users', methods = ['GET'])
def listAllUsers():
    global n_http_requests
    n_http_requests = n_http_requests + 1
    if(request.method == "GET"):
        path = "./data/users/users.json";
        with open(path) as json_file:
            data = json.load(json_file)
        users = []
        for i in data['users']:
            users.append(i['username'])
        print(users)
        return str(users)
    else:
        return "Invalid request."

@app.route('/api/v1/_count', methods = ['GET'])
def count_http_request():
    ##global n_http_requests
    ##n_http_requests = n_http_requests + 1
    if(request.method == "GET"):
        count_array = []
        count_array[0] = n_http_requests
        return str(count_array)

@app.route('/api/v1/_count', methods = ['DELETE'])
def reset_http_request():
    ##global n_http_requests
    ##n_http_requests = n_http_requests + 1
    if(request.method == "DELETE"):
        n_http_requests = 0
        return "{}"

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 80)

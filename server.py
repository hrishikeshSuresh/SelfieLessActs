"""
Authors : Hrishikesh S.   01FB16ECS139
          Karthik A.      01FB16ECS159
Status  : back-end front-end communications are mostly working
          need to add upvote button to catetemplate.html and make upvote working
          pass ip_address and port_no as arguments (OPTIONAL)
Notes   : # for developer's comment/insight
          ## for removing code
          To access the V.M., get the .pem key and run
                $ ssh -i "MYOSHLinux.pem" ubuntu@ec2-52-1-164-74.compute-1.amazonaws.com
          Run pre-run.sh before running this code on terminal/CMD PROMPT
"""
# I.P. address should be a string
ip_address = 'localhost'
# port number should be a number
port_no = 5000

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
            if(match != None):
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
        list_of_users = list_of_users.strip()[1:-1].split(sep = ",")
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
        list_of_users = list_of_users.strip()[1:-1].split(sep = ",")
        print(list_of_users)
        present = False
        for u in list_of_users:
            if(username in u):
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

# list all categories
# checked
# front-end done
@app.route('/api/v1/categories', methods = ['GET'])
def listCategories():
    if request.method == 'GET':
        ##print(os.listdir())
        cat = []
        cat = os.listdir('./data/categories')
        print(cat)
        dictionary = {}
        ##for i in range(0,len(cat)):
        ##    files = []
        ##    directory = "./data/categories/"+cat[i]
        ##    files = os.listdir(directory)
        ##    dictionary[cat[i]] = len(files)
        for file in cat:
            # read number of acts from each folder
            json_file = "./data/categories/" + file + "/" + file + ".json"
            ##print(json_file)
            with open(json_file, 'r') as fp:
               data = json.load(fp)
            dictionary[file] = len(data['acts'])
        return str(dictionary)
    else:
        return 'Invalid Request'

# add a category
# input should be JSON ARRAY []
# checked
# front-end done, but method not allowed pops up even API processed data successfully
@app.route('/api/v1/categories', methods = ['POST'])
def addCategory():
    if request.method == "POST":
        print("Receiving category name")
        ##catName = request.args.get['categoryName']
        catName = str(request.get_data().decode())
        print(catName)
        catName = catName.replace('\"', '')
        catName = catName.replace('\t', '')
        catName = catName.replace('\n', '')
        ##catName = catName[2:len(catName)-2]
        catName = catName.replace("\"", "")
        catName = catName.lstrip(' ')
        catName = catName.rstrip(' ')
        catName = catName[1:len(catName)-1]
        ##print(catName)
        if(catName == None):
            catName = request.form['categoryName']
        print("category name is -->", catName)
        # should be entered into database
        path = "./static/categories/"
        cats = os.listdir(path)
        if catName not in cats:
            os.mkdir("./static/categories/" + catName)
            os.mkdir("./data/categories/" + catName)
            data = {'acts':[]}
            with open("./data/categories/"+ catName + '/' + catName + ".json", 'w') as json_file:
                data= json.dump(data, json_file, indent = 4)
            print(catName + ' added')
            return catName + ' added'
        else:
            return catName + ' already present'
    ##else:
    ##    print("method is -->",request.method)
    ##    return 'category not added'
    ##    print(catName)
    ##    os.mkdir("./static/categories/"+catName)
    ##    # should be entered into database
    ##    return 'Category added'
    else:
        return 'Invalid Request'


# remove a category
# checked
# front-end done, but need to reload page on submit
@app.route('/api/v1/categories/<categoryName>', methods = ['DELETE'])
def removecategory(categoryName):
    ##print('OBJECTIVE : ', categoryName)
    if(request.method == 'DELETE'):
        print("Receiving data....")
        path = "./static/categories/"
        cats = os.listdir(path)
        if categoryName  in cats:
            shutil.rmtree("./static/categories/" + categoryName)
            shutil.rmtree("./data/categories/" + categoryName)
            return categoryName + " successfully removed"
        else:
            return categoryName + " not found"
        ##if(os.path.exists("data/categories/" + categoryName)):
            ##print("Going to delete it")
            ##os.rmdir("data/categories/"+categoryName)
            ##message = "Deleting "+ categoryName
            ##return message
        ##else:
        ##    return 'This category does not exists'
    else:
        return 'Invalid Request'

# list acts for a given category (when total #acts is less than 100)
# return is JSON array [{}]
# checked
# front-end done, but need to check again after uploading act
@app.route('/api/v1/categories/<categoryName>/acts', methods = ['GET'])
def listActs(categoryName):
    if request.method == "GET":
        list_acts = []
        cats = os.listdir('./data/categories')
        print("List all categories")
        print(categoryName)
        if(categoryName not in cats):
            return "category Name Not Exists."
        path = "./data/categories/"+categoryName
        list_acts = os.listdir(path)
        file = list_acts[0]
        print("This is file --> ",file)
        with open(path + '/'+ file) as json_file:
            data = json.load(json_file)
        if(len(data['acts']) > 100):
            return "Number of acts are more than 100"
        ##print("This is data -->",data['acts'])
        return str(data['acts'])
    else:
        return 'Invalid Request'

# list number of acts for a given category
# check if category is present
# checked
# front-end done
@app.route('/api/v1/categories/<categoryName>/acts/size', methods = ['GET'])
def listNoOfActs(categoryName):
    if request.method == "GET":
        list_acts = []
        cats = os.listdir('./data/categories')
        if(categoryName not in cats):
            return "category Name Not Exists."
        path = "./data/categories/"+categoryName
        list_acts = os.listdir(path)
        file = list_acts[0]
        with open(path+'/'+file) as json_file:
            data = json.load(json_file)
            print(data['acts'])
            print(len(data['acts']))
            return str(len(data['acts']))
    else:
        return "Invalid Request"

# return number of acts for a given category in a given range(inclusive)
# checked
# front-end done, need to check after uploading acts
@app.route('/api/v1/categories/<categoryName>/acts?start=<startRange>&end=<endRange>', methods = ['GET'])
def listActsInGivenRange(categoryName,startRange,endRange):
    print("Receiving data...")
    if(request.method == "GET"):
        #startRange = request.args.get('start')
        #endRange = request.args.get('end')
        print("startRange = ",startRange)
        print("type is ",type(startRange))
        print("endRange = ",endRange)
        list_acts = []
        cats = os.listdir('./data/categories')
        if(not checkCategory(categoryName)):
            return "category does not exists."
        path = "./data/categories/"+categoryName
        list_acts = os.listdir(path)
        file = list_acts[0]
        with open(path+'/'+file) as json_file:
            data = json.load(json_file)
        arr = []
        for i in range(int(startRange),int(endRange)+1):
            arr.append(data['acts'][i])
        return str(arr)
    else:
        return "Invalid Request"

# upvote an act
# json array []
# checked
# need to modify catetemplate
@app.route('/api/v1/acts/upvote', methods = ['POST'])
def upvoteAct():
    if request.method == "POST":
        actId = request.get_data().decode()
        actId = str(actId)
        actId = actId[1:len(actId)-1]
        actId = actId.replace("\t", "")
        actId = actId.replace("\n", "")
        actId = actId.lstrip(' ')
        actId = actId.rstrip(' ')
        actId = actId.replace(' ', '')
        print("actId is = ", actId)
        print("type of actId is = ", str(actId))
        list_cat = []
        if(not checkId(actId)):
                return "ActId does not Exists."
        path = "./data/categories"
        list_cat = os.listdir(path)
        for fold in list_cat:
            cur_path = path+"/"+fold
            list_file = os.listdir(cur_path)
            with open(cur_path+'/'+list_file[0]) as json_file:
                data = json.load(json_file)
                count = 0
                for d in data['acts']:
                    if(d['actId'] == actId):
                        data['acts'][count]['upvotes'] =str(int(d['upvotes'])+1)
                        break
                    count+=1
            with open(cur_path+'/'+list_file[0], 'w') as data_file:
                data= json.dump(data, data_file,indent = 4)
        return "Upvote Done"
            ##with open(list_file[0], 'w') as data_file:
            ##    data= json.dump(data, data_file,indent = 4)
    else:
        return "Invalid Request"

# remove an act
# checked
# front-end done
@app.route('/api/v1/acts/<actId>', methods = ['DELETE'])
def removeAct(actId):
    if request.method == "DELETE":
        list_cat = []
        print(actId)
        ##actId = int(actId)
        path = "./data/categories"
        list_cat = os.listdir(path)
        for fold in list_cat:
            cur_path = path+"/"+fold
            list_file = os.listdir(cur_path)
            if(not checkId(actId)):
                return "ActId does not Exists."
            with open(cur_path+'/'+list_file[0]) as json_file:
                data = json.load(json_file)
            arr = data['acts']
            arr [:] = [d for d in arr if str(d.get("actId")) != actId]
            print(arr)
            data['acts'] = arr
            print(data['acts'])
            with open(cur_path + '/' + list_file[0], 'w') as data_file:
                data= json.dump(data, data_file,indent = 4)
        return "Acts successfully removed"
    else:
         return "Invalid Request"

# upload an act
# checked
# front-end works, but incoming base64 string is not loaded correctly in catetemplate
# probably need to find a correct way to convert image to base64 string in upload.html
@app.route('/api/v1/acts', methods = ['POST'])
def uploadAct():
    x = datetime.datetime.now()
    print("Received @ ", x.time())
    if(request.method == 'POST'):
        print("Receiving data....")
        if(request.form != ""):
            print("Form data")
            print(request.form)
            u_actId = request.form['actId']
            print(u_actId)
            u_name = request.form['username']
            u_caption = request.form['caption']
            u_cat = request.form['categoryName']
            u_imgB64 = str(request.form['imgB64'])
            u_time = request.form['timestamp']
        else:
            print("Not form data")
            print(json.loads(request.data.decode()))
            u_actId = json.loads(request.data.decode())['actId']
            u_name = json.loads(request.data.decode())['username']
            u_time = json.loads(request.data.decode())['timestamp']
            u_caption = json.loads(request.data.decode())['caption']
            u_cat = json.loads(request.data.decode())['categoryName']
            u_imgB64 = json.loads(request.data)['imgB64']
        ##if(u_name == None):
        print(u_actId, u_name, u_caption, u_cat, u_time, u_imgB64)
        timeFormat = "%d-%m-%Y:%S-%M-%H"
        try:
            valid_time = datetime.datetime.strptime(u_time, timeFormat)
            print("Valid time")
        except ValueError:
            print("Incorrect Time format")
            print(u_time)
            return "invalid time format"
        image = ""
        try:
            image = base64.b64decode(u_imgB64)
            ##print(image)
        except:
            return "not a valid base64 string"
        val = checkCategory(u_cat)
        if(val == 0):
            return "category does not exists."
        val = checkId(u_actId)
        # checks if the actId is currently there in the given directory.
        if(val == 1):
            return "act id is already assigned."
        list_of_users = requests.get('http://' + ip_address+ ':' + str(port_no) + '/api/v1/users')
        list_of_users = list_of_users.text
        list_of_users = list_of_users.strip()[1:-1].split(sep = ",")
        print(list_of_users)
        present = False
        for u in list_of_users:
            if(u_name in u):
                present = True
                break
        if(present == False):
            return "user does not exists"
        ##new_val = checkUser(u_name)
        ##if(new_val == 0):
           ##return "user not found"
        dictionary = {}
        dictionary['actId'] = str(u_actId)
        dictionary['username'] = u_name
        dictionary['timestamp'] = u_time
        dictionary['caption'] = u_caption
        dictionary['categoryName'] = u_cat
        dictionary['imgB64'] = u_imgB64
        dictionary['upvotes'] = 0
        path = "./data/categories/" + u_cat + '/' + u_cat + ".json"
        with open(path) as json_file:
            data = json.load(json_file)
            data['acts'].append(dictionary)
        with open(path,'w') as data_file:
            data= json.dump(data, data_file,indent = 4)
        with open('./static/categories/' + u_cat + '/'+ str(u_actId) + '.png', 'wb') as f_img:
            f_img.write(image)
        return "act uploaded successfully"

# list all users
@app.route('/api/v1/users', methods = ['GET'])
def listAllUsers():
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

if __name__ == '__main__':
    app.run(debug = True, host = ip_address, port = port_no)

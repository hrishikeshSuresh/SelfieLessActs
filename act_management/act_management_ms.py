"""
Authors : Hrishikesh S.   01FB16ECS139
          Karthik A.      01FB16ECS159
Status  : back-end front-end communications are mostly working
          need to add upvote button to catetemplate.html and make upvote working
          pass ip_address and port_no as arguments (OPTIONAL)
Notes   : # for developer's comment/insight
          ## for removing code
          Modify IP address & Port before running with user_management_ms.py
          To access the V.M., get the .pem key and run
                $ ssh -i "MYOSHLinux.pem" ubuntu@public_dns
          Run pre-run.sh before running this code on terminal/CMD PROMPT
"""
# I.P. address should be a string
# enter I.P. address of users instance
ip_address = '35.174.107.114'
origin = '18.212.26.145'
# port number should be a number
port_no = 80
# health of container
healthy = True

from flask import (
    Flask,
    render_template,
    url_for,
    Markup,
    send_from_directory,
    flash,
    request,
    jsonify
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

headers = {'Origin' : '18.212.26.145'}

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

# list all categories
# checked
# front-end done
@app.route('/api/v1/categories', methods = ['GET'])
def listCategories():
    global n_http_requests
    n_http_requests = n_http_requests + 1
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
            ##if(len(data['acts']) == 0):
                ##return jsonify({}), 204
        return jsonify(dictionary), 200
    else:
        return jsonify({}), 405

# add a category
# input should be JSON ARRAY []
# checked
# front-end done, but method not allowed pops up even API processed data successfully
# need to find reason for code 400
@app.route('/api/v1/categories', methods = ['POST'])
def addCategory():
    global n_http_requests
    n_http_requests = n_http_requests + 1
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
            return jsonify({}), 200
        else:
            return jsonify({}), 400
    ##else:
    ##    print("method is -->",request.method)
    ##    return 'category not added'
    ##    print(catName)
    ##    os.mkdir("./static/categories/"+catName)
    ##    # should be entered into database
    ##    return 'Category added'
    else:
        return jsonify({}), 405

# remove a category
# checked
# front-end done, but need to reload page on submit
@app.route('/api/v1/categories/<categoryName>', methods = ['DELETE'])
def removecategory(categoryName):
    global n_http_requests
    n_http_requests = n_http_requests + 1
    ##print('OBJECTIVE : ', categoryName)
    if(request.method == 'DELETE'):
        print("Receiving data....")
        path = "./static/categories/"
        cats = os.listdir(path)
        if categoryName  in cats:
            shutil.rmtree("./static/categories/" + categoryName)
            shutil.rmtree("./data/categories/" + categoryName)
            return jsonify({}), 200
        else:
            return jsonify({}), 400
        ##if(os.path.exists("data/categories/" + categoryName)):
            ##print("Going to delete it")
            ##os.rmdir("data/categories/"+categoryName)
            ##message = "Deleting "+ categoryName
            ##return message
        ##else:
        ##    return 'This category does not exists'
    else:
        return jsonify({}), 405

# list acts for a given category (when total #acts is less than 100)
# return is JSON array [{}]
# checked
# front-end done, but need to check again after uploading act
@app.route('/api/v1/categories/<categoryName>/acts', methods = ['GET'])
def listActs(categoryName):
    global n_http_requests
    n_http_requests = n_http_requests + 1
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
            return jsonify({}), 413
        ##print("This is data -->",data['acts'])
        if(len(data['acts']) == 0):
            return jsonify({}), 204
        return jsonify(data['acts']), 200
    else:
        return jsonify({}), 405

# list number of acts for a given category
# check if category is present
# checked
# front-end done
@app.route('/api/v1/categories/<categoryName>/acts/size', methods = ['GET'])
def listNoOfActs(categoryName):
    global n_http_requests
    n_http_requests = n_http_requests + 1
    if request.method == "GET":
        list_acts = []
        cats = os.listdir('./data/categories')
        if(categoryName not in cats):
            return jsonify({}), 404
        path = "./data/categories/"+categoryName
        list_acts = os.listdir(path)
        file = list_acts[0]
        with open(path+'/'+file) as json_file:
            data = json.load(json_file)
            print(data['acts'])
            print(len(data['acts']))
            number_of_acts = list(len(data['acts']))
            return jsonify(number_of_acts), 200
    else:
        return jsonify({}), 405

# return number of acts for a given category in a given range(inclusive)
# checked
# front-end done, need to check after uploading acts
@app.route('/api/v1/categories/<categoryName>/acts?start=<startRange>&end=<endRange>', methods = ['GET'])
def listActsInGivenRange(categoryName,startRange,endRange):
    global n_http_requests
    n_http_requests = n_http_requests + 1
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
            return jsonify({}), 404
        path = "./data/categories/"+categoryName
        list_acts = os.listdir(path)
        file = list_acts[0]
        with open(path+'/'+file) as json_file:
            data = json.load(json_file)
        arr = []
        for i in range(int(startRange),int(endRange)+1):
            arr.append(data['acts'][i])
        if(len(arr) > 100):
            return jsonify({}), 413
        if(len(arr) == 0):
            return jsonify({}), 204
        print(arr)
        arr = list(len(arr))
        return jsonify(arr), 200
    else:
        return jsonify({}), 405

# upvote an act
# json array []
# checked
# need to modify catetemplate
@app.route('/api/v1/acts/upvote', methods = ['POST'])
def upvoteAct():
    global n_http_requests
    n_http_requests = n_http_requests + 1
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
        actId = int(actId)
        if(not checkId(actId)):
                return jsonify({}), 404
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
        return jsonify({}), 200
            ##with open(list_file[0], 'w') as data_file:
            ##    data= json.dump(data, data_file,indent = 4)
    else:
        return jsonify({}), 405

# remove an act
# checked
# front-end done
@app.route('/api/v1/acts/<actId>', methods = ['DELETE'])
def removeAct(actId):
    global n_http_requests
    n_http_requests = n_http_requests + 1
    if request.method == "DELETE":
        list_cat = []
        print(actId)
        actId = int(actId)
        path = "./data/categories"
        list_cat = os.listdir(path)
        for fold in list_cat:
            cur_path = path+"/"+fold
            list_file = os.listdir(cur_path)
            if(not checkId(actId)):
                return jsonify({}), 404
            with open(cur_path+'/'+list_file[0]) as json_file:
                data = json.load(json_file)
            arr = data['acts']
            arr [:] = [d for d in arr if d.get("actId") != actId]
            print(arr)
            data['acts'] = arr
            print(data['acts'])
            with open(cur_path + '/' + list_file[0], 'w') as data_file:
                data= json.dump(data, data_file,indent = 4)
        return jsonify({}), 200
    else:
         return jsonify({}), 405

# upload an act
# checked
# front-end works, but incoming base64 string is not loaded correctly in catetemplate
# probably need to find a correct way to convert image to base64 string in upload.html
@app.route('/api/v1/acts', methods = ['POST'])
def uploadAct():
    global origin
    headers = {'Origin' : origin}
    global n_http_requests
    n_http_requests = n_http_requests + 1
    x = datetime.datetime.now()
    print("Received @ ", x.time())
    if(request.method == 'POST'):
        print("Receiving data....")
        if(request.method == ""):
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
            return jsonify({}), 400
        image = ""
        try:
            image = base64.b64decode(u_imgB64)
            ##print(image)
        except:
            return jsonify({}), 400
        val = checkCategory(u_cat)
        if(val == 0):
            return jsonify({}), 404
        val = checkId(u_actId)
        # checks if the actId is currently there in the given directory.
        if(val == 1):
            return jsonify({}), 400
        ##return "works till here"
        list_of_users = requests.get('http://' + ip_address+ ':' + str(port_no) + '/api/v1/users', headers = headers)
        list_of_users = list_of_users.text
        list_of_users = list_of_users[1:-1].replace('\'','').replace(', ',',').split(sep = ",")
        print(list_of_users)
        present = False
        for u in list_of_users:
            if(u_name in  u):
                present = True
                break
        if(present == False):
            return jsonify({}), 404
        ##new_val = checkUser(u_name)
        ##if(new_val == 0):
           ##return "user not found"
        dictionary = {}
        dictionary['actId'] = u_actId
        dictionary['username'] = u_name
        dictionary['timestamp'] = u_time
        dictionary['caption'] = u_caption
        dictionary['categoryName'] = u_cat
        dictionary['imgB64'] = u_imgB64
        dictionary['upvotes'] = "0"
        path = "./data/categories/" + u_cat + '/' + u_cat + ".json"
        with open(path) as json_file:
            data = json.load(json_file)
            data['acts'].append(dictionary)
        with open(path,'w') as data_file:
            data= json.dump(data, data_file,indent = 4)
        with open('./static/categories/' + u_cat + '/'+ str(u_actId) + '.png', 'wb') as f_img:
            f_img.write(image)
        return jsonify({}), 405

@app.route('/api/v1/_count', methods = ['GET'])
def count_http_request():
	global n_http_requests
	n_http_requests = n_http_requests + 1
	if(request.method == "GET"):
		n_http_requests_list = list(n_http_requests)
		return jsonify(n_http_requests_list), 200
	else:
		return jsonify({}), 405

@app.route('/api/v1/_count', methods = ['DELETE'])
def reset_http_request():
	global n_http_requests
	n_http_requests = n_http_requests + 1
	if(request.method == "DELETE"):
		n_http_requests = 0
		return jsonify({}), 200
	else:
		return jsonify({}), 405

@app.route('/api/v1/acts/count', methods = ['GET'])
def countAllActs():
	global n_http_requests
	n_http_requests = n_http_requests + 1
	if(request.method == "GET"):
		path = "./data/categories/"
		list_folder = os.listdir(path)
		count = 0
		for fold in list_folder:
			new_path = path + fold + '/' + fold + ".json"
			with open(new_path) as json_file:
				data = json.load(json_file)
			count += len(data['acts'])
		count_list = list(count)
		return jsonify(count), 200
	else:
		return jsonify({}), 405

# health check
@app.route('/api/v1/_health', methods = ['GET'])
def health():
	global healthy
	if(healthy == True):
		return jsonify({}), 200
	else:
		return jsonify({}), 500

# crash server
@app.route('/api/v1/_crash', methods = ['POST'])
def crash():
	global healthy
	healthy = False
	return jsonify({}), 200

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 80)

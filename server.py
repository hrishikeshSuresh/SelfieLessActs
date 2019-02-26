"""
Authors : Hrishikesh S.   01FB16ECS139
          Karthik A.      01FB16ECS159
Status  : Need to fix back-end front-end communications
Note    : # for developer comment
          ## for comment/removing code
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
from werkzeug import secure_filename, exceptions
import datetime
import shutil
import base64
import binascii

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
    return 'bad request!', 400

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


# supports
# localhost:5000/homePage.html, non-functional
@app.route('/homePage.html')
def homeSupport():
    #flash("Works!")
	#print(os.listdir())
	f = os.listdir('data/categories')
	return render_template('homePage.html', categories = f)

# upload webpage
# localhost:5000/upload.html
@app.route('/upload.html')
def uploadSupport():
    f = os.listdir('data/categories')
    return render_template('upload.html', categories = f)

# list all acts
@app.route('/listallacts.html')
def listallactsSupport():
    f = os.listdir('data/categories')
    return render_template('listallacts.html', categories = f)

# list number of acts webpage
# localhost:5000/listnoofacts.html
@app.route('/listnoofacts.html')
def displaylistnoonactsSupport():
    f = os.listdir('data/categories')
    return render_template('listnoofacts.html', categories = f)

# list number of acts range webpage
# localhost:5000/listnoofactsrange.html
@app.route('/listnoofactsrange.html')
def displaylistnoonactsrangeSupport():
    f = os.listdir('data/categories')
    return render_template('listnoofactsrange.html', categories = f)

# signup / add user webpage
# localhost:5000/signup
@app.route('/signup')
def signUpSupport():
    return render_template('signup.html')

# remove category webpage
# localhost:5000/rmcategory
@app.route('/rmcategory')
def removeCategorySupport():
    f = os.listdir('data/categories')
    return render_template('rmcat.html', categories = f)

# add category webpage
# localhost:5000/addcat.html
@app.route('/addcat.html')
def addCategorySupport():
    return render_template('addcat.html')

# remove user webpage
# localhost:5000/rmuser.html
@app.route('/rmuser.html')
def removeUserSupport():
    return render_template('rmuser.html')

# remove acts
@app.route('/rmact.html')
def rmactSupport():
    return render_template('rmact.html')

# display category
@app.route('/display/<categoryName>.html')
def categoryDisplaySupport(categoryName):
    cat = os.listdir('./data/categories')
    curr_path = './data/categories/'+categoryName
    file = os.listdir(curr_path)
    with open(curr_path + '/' + file[0]) as json_file:
        data = json.load(json_file)
    ##print(data)
    for i in data['acts']:
        ##i['imgB64'] = base64.b64decode(i['imgB64'])
        print(i['actId'])
    return render_template('catetemplate.html', categories = cat, image_data = data['acts'], catName = categoryName)

#for cate1, cate2 and cate3, the upload button is not rendering properly
#also need to the HTML page to load the images with the upvote button and name of user
#localhost:5000/cate1.html, non-functional
##@app.route('/cate1.html')
##def cate1():
##    #print(os.listdir())
##    return render_template('cate1.html')

#localhost:5000/cate2.html, non-functional
##@app.route('/cate2.html')
##def cate2():
##    #print(os.listdir())
##    return render_template('cate2.html')

#localhost:5000/cate3.html, non-functional
##@app.route('/cate3.html')
##def cate3():
##    #print(os.listdir())
##    return render_template('cate3.html')

#localhost:5000/uploadImage
#need to fix this, non-functional
##@app.route('/uploadImage', methods = http_methods)
##def uploadFile():
##    #sub routine not working
##    if request.method == 'POST':
##        f = request.files['file']
##        f.save(secure_filename(f.filename))
##        print('File uploaded successfully')
##    return render_template('homePage.html')

# needs fixing on HTML & CSS side immediately, non-functional
##@app.route('/login.html')
##def login():
##    return render_template('login.html')

# needs fixing on HTML & CSS side immediately, non-functional
##@app.route('/register.html')
##def register():
##    return render_template('signup.html')

# register user, non-functional
##@app.route('/registerUser')
##def registeredUser():
##    if(request.method == 'POST'):
##        print("Receiving data...")
##        data = request.form
##        print(data[0])
##    return redirect(url_for('home'))

#test, signup user
##@app.route('/api/v1/users', methods=['POST'])
##def signUpUser():
##    if(request.method == 'POST'):
##        print("Receiving data....")
##        u_data = request.args.get('username')
##        u_password = request.args.get('password')
##        print(u_data, u_password)
##        if(u_data == None and u_password == None):
##            u_data = request.form['username']
##            u_password = request.form['password']
##        data = dict()
##        data['username'] = u_data
##        data['password'] = u_password
##        file = "data/users/" + u_data + ".json"
##        with open(file, 'w') as fp:
##            json.dump(data, fp, sort_keys = True, indent = 4)
##        message = u_data + ' has been added'
##        return message
##    else:
##        return 'Invalid Request'

"""
APIs
"""

# add user
# use this flag is True if data is from 'form'
# check if user is already in the database
# check is password is SHA1 hash hex
# getting added twice
@app.route('/api/v1/users', methods = http_methods)
def addUser():
    if(request.method == 'POST'):
        print(request.form)
        print("Receiving data....")
        u_data = request.args.get('username')
        u_password = request.args.get('password')
        print(u_data, u_password)
        flag = False
        if(u_data == None and u_password == None):
            u_data = request.form['username']
            u_password = request.form['password']
        file = os.listdir('./data/users')
        ##print("This is file ---> ",file)
        with open('./data/users/'+file[0]) as json_file:
            ##print("Opening a file is done")
            data = json.load(json_file)
        ##print("This is data -->",data)
        if(checkUser(u_data)):
            return "User already Exists."
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
# check if user is present or absent in the database before deleting (optional)
@app.route('/api/v1/users/<username>', methods = ['DELETE'])
def removeUser(username):
    if(request.method == 'DELETE'):
        print("Receiving data....")
        if(username == None):
            return "username does not exit on route"
        print('OBJECTIVE : ', username)
        file = os.listdir('./data/users/')
        with open('./data/users/'+file[0]) as json_file:
            data = json.load(json_file)
        ##print("data is --> ",data)
        if(not checkUser(username)):
            return "User does not Exists."
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
@app.route('/api/v1/categories', methods = ['GET'])
def listCategories():
    if request.method == 'GET':
        ##print(os.listdir())
        cat = []
        cat = os.listdir('./data/categories')
        print(cat)
        dictionary = {}
        for i in range(0,len(cat)):
            files = []
            directory = "./data/categories/"+cat[i]
            files = os.listdir(directory)
            dictionary[cat[i]] = len(files)
        return str(dictionary)
    else:
        return 'Invalid Request'

# add a category
# should be JSON ARRAY []
# check if category is already present (case-sensitive) , done
@app.route('/api/v1/categories', methods = ['POST'])
def addCategory():
    if request.method == "POST":
        print("Receiving category name")
        catName = request.args.get('categoryName')
        if(catName == None):
            catName = request.form['categoryName']
        print("category Name is -->", catName)
        # should be entered into database
        path = "./static/categories/"
        cats = os.listdir(path)
        if catName not in cats:
            os.mkdir("./static/categories/"+ catName)
            os.mkdir("./data/categories/"+ catName)
            data = {'acts':[]}
            with open("./data/categories/"+ catName + '/' + catName + ".json",'w') as json_file:
                data= json.dump(data, json_file,indent = 4)
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
# check if less than 100, else return relevant error code
# category name must exist
# return is JSON array [{}]
@app.route('/api/v1/categories/<categoryName>/acts', methods = http_methods)
def listActs(categoryName):
    if request.method == "GET":
        list_acts = []
        path = "./data/categories/"+categoryName
        list_acts = os.listdir(path)
        file = list_acts[0]
        if(categoryName not in cats):
            return "category Name Not Exists."
        print("This is file --> ",file)
        with open(path + file) as json_file:
            data = json.load(json_file)
        if(len(data['acts']) > 100):
            return "Number of acts are more than 100"
        print("This is data -->",data['acts'])
        return str(data['acts'])
        ##file = list_acts[0]+".json"
        ##with open(file) as json_file:
        ##    data = json.load(json_file)
        ##    arr = [] # This is array of dictionary...
        ##    for d in data['acts']:
        ##        dictionary = {}
        ##        dictionary['actId'] = d['actId']
        ##        dictionary['username'] = d['username']
        ##        dictionary['timestamp'] = d['timestamp']
        ##        dictionary['caption'] = d['caption']
        ##        dictionary['upvotes'] = d['upvotes']
        ##        dictionary['imgB64'] = d['imgB64']
        ##        arr.append(dictionary)
        ##return str(arr)
    else:
        return "categoryName Not Found"

# list number of acts for a given category
# check if category is present
@app.route('/api/v1/categories/<categoryName>/acts/size', methods = ['GET'])
def listNoOfActs(categoryName):
    if request.method == "GET":
        list_acts = []
        path = "./data/categories/"+categoryName
        list_acts = os.listdir(path)
        file = list_acts[0]
        if(categoryName not in cats):
            return "category Name Not Exists."
        with open(path+'/'+file) as json_file:
            data = json.load(json_file)
            print(data['acts'])
            print(len(data['acts']))
            return str(len(data['acts']))
        ##file = list_acts[0]+".json"
        ##with open(file) as json_file:
        ##    data = json.load(json_file)
        ##    print(data['acts'])
        ##    print(len(data['acts']))
        ##    return str(len(data['acts']))
    else:
        return "category not found"

# return number of acts for a given category in a given range(inclusive)
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
        path = "./data/categories/"+categoryName
        list_acts = os.listdir(path)
        file = list_acts[0]
        if(not checkCategory(categoryName)):
            return "category does not exists."
        with open(path+'/'+file) as json_file:
            data = json.load(json_file)
        arr = []
        for i in range(int(startRange),int(endRange)+1):
            arr.append(data['acts'][i])
        return str(arr)
    else:
        return "categoryName Not Found"

# upvote an act
# does not work
# global act ID
@app.route('/api/v1/acts/upvote', methods = ['POST'])
def upvoteAct():
    if request.method == "POST":
        actId = request.get_data()
        actId = str(actId)
        actId = actId[2:len(actId)-1]
        print("actId is = ",actId)
        print("type of actId is = ",type(actId))
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
# check if act is present or not
# does not work
# need to make act ID global
@app.route('/api/v1/acts/<actId>', methods = ['DELETE'])
def removeAct(actId):
    if request.method == "DELETE":
        list_cat = []
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
            ##with open(list_file[0]) as json_file:
            ##    data = json.load(json_file)
            ##    arr = data['acts']
            ##    arr [:] = [d for d in arr if a.get('actId') != actId]
            ##    data['acts'] = arr
            ##with open(list_file[0], 'w') as data_file:
            ##    data= json.dump(data, data_file,indent = 4)
    else:
         return "Invalid Request"

# upload an act
# check if BASE64 string or not
# act id must be globally unique
# add image in static
@app.route('/api/v1/acts', methods = ['POST'])
def uploadAct():
    x = datetime.datetime.now()
    print("Received @ ", x.time())
    if(request.method == 'POST'):
        print("Receiving data....")
        print(request.form)
        u_actId = request.args.get('actId')
        ##print(u_actId)
        u_name = request.args.get('username')
        u_time = request.args.get('timestamp')
        u_caption = request.args.get('caption')
        u_cat = request.args.get('categoryName')
        u_imgB64 = request.args.get('imgB64')
        if(u_name == None):
            u_actId = request.form['actId']
            print(u_actId)
            u_name = request.form['username']
            u_caption = request.form['caption']
            u_cat = request.form['categoryName']
            u_imgB64 = request.form['imgB64']
            u_time = request.form['timestamp']
        print(u_actId, u_name, u_caption, u_cat, u_time, u_imgB64)
        timeFormat = "%d-%m-%Y:%S-%M-%H"
        try:
            valid_time = datetime.datetime.strptime(u_time, timeFormat)
            print("Valid time")
        except ValueError:
            print("Incorrect Time format")
            print(u_time)
            return "Invalid Time Format"
        image = ""
        try:
            image = base64.b64decode(request.args.get('imgB64'))
            print(image)
        except binascii:
            return "not a valid base64 string"
        val = checkCategory(u_cat)
        if(val == 0):
            return "category does not exists."
        val = checkId(u_actId)
        # checks if the actId is currently there in the given directory.
        if(val):
            return "ActId is already assigned."
        dictionary = {}
        dictionary['actId'] = u_actId
        dictionary['username'] = u_name
        dictionary['timestamp'] = u_time
        dictionary['caption'] = u_caption
        dictionary['categoryName'] = u_cat
        dictionary['imgB64'] = u_imgB64
        dictionary['upvote'] = 0
        path = "./data/categories/" + u_cat + '/' + u_cat + ".json"
        with open(path) as json_file:
            data = json.load(json_file)
            data['acts'].append(dictionary)
        with open(path,'w') as data_file:
            data= json.dump(data, data_file,indent = 4)
        ##with open('./static/categories/' + u_cat + '/'+ u_actId + '.png', 'wb') as f_img:
        ##    f_img.write(image.decode('base64'))
        return "Uploaded Act successfully.  "
        ##u_data = request.args.get('username')
        ##u_file = u_data + ".json"
        ##all_users = os.listdir("data/users/")
        ##all_act_ids = os.listdir("data/categories/")
        ##u_act_id = request.args.get('actId')
        ##if u_file in all_users:
        ##    print("Valid User")
        ##    if u_act_id not in all_act_ids:
        ##        print("Act found")
        ##        timeFormat = "%d-%m-%Y:%S-%M-%H"
        ##        input_time = request.args.get('timestamp')
        ##        try:
        ##            valid_time = datetime.datetime.strptime(input_time, timeFormat)
        ##            print("Valid time")
        ##        except ValueError:
        ##            print("Incorrect Time format")
        ##            print(input_time)
        ##            return "Invalid Time Format"
        ##        if(request.args.get('categoryName') == ""):
        ##            return 'No category name'
        ##        else:
        ##            print("Valid category")
        ##            image = ""
        ##            try:
        ##                image = base64.b64decode(request.args.get('imgB64'))
        ##                print(image)
        ##            except binascii:
        ##                return "not a valid base64 string"
        ##            file = "data/categories/"+ request.args.get('categoryName') +"/"+request.args.get('categoryName') + ".json"
        ##            dictionary= {}
        ##            dictionary['actId'] = request.args.get('actId')
        ##            dictionary['username'] = request.args.get('username')
        ##            dictionary['timestamp'] = request.args.get('timestamp')
        ##            dictionary['caption'] = request.args.get('caption')
        ##            if(request.args.get('upvotes') == None):
        ##                upvotes = 0
        ##                dictionary['upvotes'] = upvotes
        ##            else:
        ##                dictionary['upvotes'] =  request.args.get('upvotes')
        ##            dictionary['categoryName'] = request.args.get('categoryName')
        ##            dictionary['imgB64'] = request.args.get('imgB64')
        ##            dictionary = [dictionary]
        ##            print(dictionary)
        ##            with open(file, 'a') as json_file:
        ##                data = json.load(json_file)
        ##                data['acts'].append(dictionary)
        ##                #json.dump(request.args.get, fp, sort_keys = True, indent = 4)
        ##            message = u_act_id + ' has been added'
        ##            return message

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)

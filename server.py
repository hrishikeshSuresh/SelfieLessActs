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
from werkzeug import secure_filename

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
@app.route('/uploadImage', methods = ['POST', 'GET'])
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

#with app.test_request_context():
    #print(url_for('home', filename = 'home/homePage.css'))
    #print(url_for('home', filename = 'bck.jpeg'))
    #print(url_for('upload', filename = 'upload.html'))
    #url_for('static', filename = "homePage.css")

if __name__ == '__main__':
    app.run(debug = True)

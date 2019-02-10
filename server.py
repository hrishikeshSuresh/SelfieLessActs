from flask import (
    Flask,
    render_template,
    url_for,
    Markup,
    send_from_directory,
    flash
)
import os
from werkzeug import secure_filename

Markup('<h1><strong>Hello!</strong></h1>')

#create application instance
app = Flask(__name__)
app.secret_key = os.urandom(16)

#@app.errorhandler(404)
#def error_404():
#    print("Not working")

@app.route('/homepage.html')
def home():
    #flash("Works!")
    #print(os.listdir())
    return render_template('/templates/homepage.html')
    #return send_from_directory('home')

@app.route('/cate1.html')
def cate1():
    #print(os.listdir())
    return render_template('/templates/cate1.html')

@app.route('/cate2.html')
def cate2():
    #print(os.listdir())
    return render_template('/templates/cate2.html')

@app.route('/cate3.html')
def cate3():
    #print(os.listdir())
    return render_template('/templates/cate3.html')

@app.route('/upload.html')
def upload():
    return render_template('/templates/upload.html')

@app.route('/upload/uploadImage', methods = ['POST'])
def uploadFile():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        print('File uploaded successfully')

#with app.test_request_context():
    #print(url_for('home', filename = 'home/homePage.css'))
    #print(url_for('home', filename = 'bck.jpeg'))
    #print(url_for('upload', filename = 'upload.html'))

if __name__ == '__main__':
    app.run(debug = True)

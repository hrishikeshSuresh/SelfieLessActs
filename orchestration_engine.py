"""
Authors : Hrishikesh S.   01FB16ECS139
Status  : back-end front-end communications are mostly working
          need to add upvote button to catetemplate.html and make upvote working
          pass ip_address and port_no as arguments (OPTIONAL)
Notes   : # for developer's comment/insight
          ## for removing code
          Modify IP address & Port before running with act_management_ms.py
          To access the V.M., get the .pem key and run
                $ ssh -i "MYOSHLinux.pem" ubuntu@public_dns
          Run pre-run.sh before running this code on terminal/CMD PROMPT
"""
# I.P. address should be a string
# enter I.P. address of your AWS instance
ip_address = '54.208.40.27'
origin = '3.86.77.173'
# port number should be a number
port_no = 80
# acts port numbers
act_ports = [8000, 8001, 8002]
act_public_dns_list = ['ip1', 'ip2', 'ip3']

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

# decision pointer for deciding which container will be used
rr_pointer = 0

# list all categories
@app.route('/api/v1/categories', methods = ['GET'])
def listCategories():
	global rr_pointer
	if request.method == 'GET':
		response = requests.get('http://'+act_public_dns_list[rr_pointer] + ':' + str(act_ports[rr_pointer])+'/api/v1/categories')
	# increment rr pointer after usage	
		rr_pointer = (rr_pointer+1)%3
		return response
	else
		return 'Invalid Request'

# add a category
# input should be JSON ARRAY []
@app.route('/api/v1/categories', methods = ['POST'])
def addCategory():
	global rr_pointer
	if request.method == 'POST':
		data = str(request.get_data().decode())
		response = requests.post('http://'+act_public_dns_list[rr_pointer] + ':' + str(act_ports[rr_pointer])+'/api/v1/categories', data = data)
	# increment rr pointer after usage	
		rr_pointer = (rr_pointer+1)%3
		return response
	else
		return 'Invalid Request'

# remove a category
@app.route('/api/v1/categories/<categoryName>', methods = ['DELETE'])
def removecategory(categoryName):
	global rr_pointer
	if request.method == 'DELETE':
		data = str(request.get_data().decode())
		response = requests.post('http://'+act_public_dns_list[rr_pointer] + ':' + str(act_ports[rr_pointer])+'/api/v1/categories/'+categoryName)
	# increment rr pointer after usage	
		rr_pointer = (rr_pointer+1)%3
		return response
	else
		return 'Invalid Request'

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 80)

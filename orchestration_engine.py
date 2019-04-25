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

# active containers
active_ports = {8000:"dkjfhal32877",8001:"ssjf2983mj"}
healthy_containers = [1, 1]

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
import time
# importing thread library
import threading
# importing docker-py to run and stop containers
import docker

# connect to docker daemon using default socket
docker_client = docker.from_env()

# decision pointer for deciding which container will be used
rr_pointer = 0

# http requests counter
n_http_requests = 0

# auto scale started flag
auto_scale_flag = 1

# critical task - RUN APP
def run_app():
    print("Name of thread : ", threading.current_thread().name())
    app.run(debug = True, host = '0.0.0.0', port = 80)

# critical task - FAULT TOLERANCE
def faultTolarence():
    print("Name of thread : ", threading.current_thread().name())
    threading.timer(1.0,faultTolarence).start()
	for i in range(len(act_public_dns_list)):
		response = requests.get("http://" + act_public_dns_list[i] + ":" + str(act_ports[i]) + "api/v1/_health")
		if(response == 500):
			container = dict_cont_port[act_ports[i]]
			container.stop()
			docker_client.containers.run("hrishikesh/acts:latest",ports = {'80':str(act_ports[i])})

# critical task - AUTO SCALING
def auto_scaling():
    # start timer only if first requests
    print("Name of thread : ", threading.current_thread().name())
    global n_http_requests, auto_scale_flag, docker_client, act_ports, active_ports
    # one container will start immediately
    ##if(n_http_requests < 20 and act_ports[0] not in active_ports):
    # container starts before first incoming requests
    if(act_ports[0] not in active_ports):
        docker_client.containers.run("hrishikeshsuresh/acts:latest", ports = {'80' : str(act_ports[0])})
        active_ports.append({act_ports[0] : docker_client.containers.list(limit = 1)})
        print("First container started. Current active ports ", active_ports)
    # wait till we get the first request
    while(auto_scale_flag == 1):
        time.sleep(1)
        if n_http_requests >= 1:
            auto_scale_flag = 0
    if(n_http_requests >= 20 and n_http_requests < 40 and act_ports[1] not in active_ports):
        docker_client.containers.run("hrishikeshsuresh/acts:latest", ports = {'80' : str(act_ports[1])})
        active_ports.append({act_ports[1] : docker_client.containers.list(limit = 1)})
        print("Second container started. Current active ports ", active_ports)
    elif(n_http_requests >= 40 and n_http_requests < 60 and act_ports[2] not in active_ports):
        docker_client.containers.run("hrishikeshsuresh/acts:latest", ports = {'80' : str(act_ports[2])})
        active_ports.append({act_ports[2] : docker_client.containers.list(limit = 1)})
        print("Third container started. Current active ports ", active_ports)
    # start timer and execute every 2 minutes
    print("starting timer")
    threading.Timer(120.0, auto_scaling).start()
    ##n_http_requests = 0

# list all categories
@app.route('/api/v1/categories', methods = ['GET'])
def listCategories():
	global rr_pointer, n_http_requests, act_public_dns_list, active_ports
    n_http_requests = n_http_requests + 1
	if request.method == 'GET':
		response = requests.get('http://' + act_public_dns_list[rr_pointer] + ':' + str(active_ports[rr_pointer])+'/api/v1/categories')
	# increment rr pointer after usage
		rr_pointer = (rr_pointer+1)%3
		return response
	else
		return 'Invalid Request'

# add a category
# input should be JSON ARRAY []
@app.route('/api/v1/categories', methods = ['POST'])
def addCategory():
	global rr_pointer, n_http_requests, act_public_dns_list, active_ports
    n_http_requests = n_http_requests + 1
	if request.method == 'POST':
		data = str(request.get_data().decode())
		response = requests.post('http://' + act_public_dns_list[rr_pointer] + ':' + str(active_ports[rr_pointer])+'/api/v1/categories', data = data)
	# increment rr pointer after usage
		rr_pointer = (rr_pointer+1)%3
		return response
	else
		return 'Invalid Request'

# remove a category
@app.route('/api/v1/categories/<categoryName>', methods = ['DELETE'])
def removecategory(categoryName):
	global rr_pointer, n_http_requests, act_public_dns_list, active_ports
    n_http_requests = n_http_requests + 1
	if request.method == 'DELETE':
		data = str(request.get_data().decode())
		response = requests.post('http://' + act_public_dns_list[rr_pointer] + ':' + str(active_ports[rr_pointer])+'/api/v1/categories/'+categoryName)
	# increment rr pointer after usage
		rr_pointer = (rr_pointer+1)%3
		return response
	else
		return 'Invalid Request'

if __name__ == '__main__':
    # creating threads
    auto_scale_thread = threading.Thread(target = auto_scaling, name = 'AUTO SCALE')
    ##threading.Timer(120.0, auto_scaling).start()
    app_thread = threading.Thread(target = run_app, name = 'RUN APP')

    # starting threads
    auto_scale_thread.start()
    app_thread.start()

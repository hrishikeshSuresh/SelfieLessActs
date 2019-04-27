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


# create application instance
app = Flask(__name__)
# generating a secret key for sessions
app.secret_key = os.urandom(16)

# port number should be a number
port_no = 80

# acts port numbers
act_port_init = 8000
act_port_end = 8001
act_public_dns_list = '18.207.223.105'

# active containers
active_ports = {}
healthy_containers = []

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
    print("Name of thread : ", threading.current_thread().name)
    print("App running @ port 8080")
    app.run(debug = True, use_reloader = False, host = '0.0.0.0', port = 8080)

# critical task - FAULT TOLERANCE
def faultTolerance():
    print("Name of thread : ", threading.current_thread().name)
    print("Fault Tolerance")
    global n_http_requests, docker_client, active_ports
    threading.Timer(10.0,faultTolerance).start()
    for i in range(len(active_ports)):
    	response = requests.get("http://" + act_public_dns_list + ":" + str(active_ports[i]) + "/api/v1/_health")
        if(response == 500):
            container = dict_cont_port[active_ports[i]]
            container.stop()
            docker_client.containers.run("hrishikesh/acts:latest", ports = {'80':str(active_ports[i])})
            print("Faulty container restarted @ port ", active_ports[i])
        else:
            print("No faulty container")

def up_scale(scale_factor):
    print("Upscaling...")
    global n_http_requests, docker_client, act_port_init, act_port_end, active_ports
    act_port_end = act_port_end + scale_factor
    for port_i in range(act_port_init, act_port_end):
        if(port_i not in active_ports):
            docker_client.containers.run("hrishikeshsuresh/acts:latest", ports = {'80' : str(port_i)})
            ##active_ports.append({port_i : docker_client.containers.list(limit = 1)})
            active_ports[port_i] = docker_client.containers.list(limit = 1)
            print("New container started. Current active ports ", active_ports)
            print("New container @ port ", port_i)
    return

def down_scale(scale_factor):
    print("Downscaling...")
    global n_http_requests, docker_client, act_port_init, act_port_end, active_ports
    # scale_factor is negative, so we add
    for port_i in range(act_port_end + scale_factor, act_port_end):
        if(port_i in active_ports):
            container_to_be_stopped = active_ports[port_i]
            container_to_be_stopped.stop()
            # None to prevent error
            active_ports.pop(port_i, None)
            print("Container removed @ port ", )
    # scale_factor is negative, so we add
    act_port_end = act_port_end + scale_factor
    return

# critical task - AUTO SCALING MAIN
def auto_scaling():
    # start timer only if first requests
    print("Name of thread : ", threading.current_thread().name)
    global n_http_requests, auto_scale_flag, docker_client, act_port_init, act_port_end, active_ports
    print("Number of containers running ", len(active_ports))
    ##if(n_http_requests < 20 and act_ports[0] not in active_ports):
    print("INIT PORT ", act_port_init)
    print("ACTIVE PORT ", active_ports)
    print(act_port_init not in active_ports)
    # one container will start immediately
    # container starts before first incoming requests
    if(act_port_init not in active_ports):
        docker_client.containers.run("hrishikeshsuresh/acts:latest", ports = {'80' : str(act_port_init)}, detach = True)
        ##active_ports.append({act_ports[0] : docker_client.containers.list(limit = 1)})
        active_ports[act_port_init] = docker_client.containers.list(limit = 1)
        print("First container started. Current active ports ", active_ports)
        act_port_end = act_port_end + 1
    # wait till we get the first request
    while(auto_scale_flag == 1):
        time.sleep(5)
        print("Waiting for first request")
        if n_http_requests >= 1:
            auto_scale_flag = 0

    # number of containers to be created
    containers_to_be_created = n_http_requests // 20
    # to decide port range for next iterations
    # formula scale_factor = r - n + 1
    print("Deciding scale factor")
    scale_factor = containers_to_be_created - len(active_ports) + 1
    if(scale_factor > 0):
        up_scale(scale_factor)
    elif(scale_factor < 0):
        down_scale(scale_factor)
    else:
        print("No scaling...")

    ##next_act_port_end = act_port_end + containers_to_be_created
    ##for port_i in range(act_port_init, act_port_end + containers_to_be_created):
        ##if(containers_to_be_created >= 1 and port_i not in active_ports):
            ##docker_client.containers.run("hrishikeshsuresh/acts:latest", ports = {'80' : str(port_i)})
            ##active_ports.append({port_i : docker_client.containers.list(limit = 1)})
            ##print("New container started. Current active ports ", active_ports)
            ##act_port_end = act_port_end + 1
            ##containers_to_be_created = containers_to_be_created - 1
    ##act_port_end = new_act_port_end

    # start timer and execute every 2 minutes
    print("starting timer...")
    n_http_requests = 0
    threading.Timer(120.0, auto_scaling).start()

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
    else:
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
    else:
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
    else:
    	return 'Invalid Request'

if __name__ == '__main__':
    # creating threads
    auto_scale_thread = threading.Thread(target = auto_scaling, name = 'AUTO SCALE')
    fault_tolerance_thread = threading.Thread(target = faultTolerance, name = 'FAULT TOLERANCE')
    ##threading.Timer(120.0, auto_scaling).start()
    app_thread = threading.Thread(target = run_app, name = 'RUN APP')
    # starting threads
    app_thread.start()
    time.sleep(5)
    auto_scale_thread.start()
    time.sleep(2)
    fault_tolerance_thread.start()

    app_thread.join()
    auto_scale_thread.join()
    fault_tolerance_thread.join()

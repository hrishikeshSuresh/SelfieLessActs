<h1>Cloud Computing Project</h1>

<h6> LOAD BALANCER DNS NAME </h6> : http://CCFINAL-246629101.us-east-1.elb.amazonaws.com
<h6> ACTS INSTANCE IP </h6> : 18.212.26.145 , PORT 80
<h6> USER INSTANCE IP </h6> : 35.174.107.114 , PORT 80

INSTRUCTIONS :
Check file structure before starting with the code
<br>
<h3> Run pre-run.sh before running server.py </h3>
<h3> Run user management container on VM 1 using, </h3>
$ sudo docker run -dp 80:80 -v user_management:user_management hrishikeshsuresh/users:latest
<h3> Run act management container, which contains the orchestration engine, on VM 2 using, </h3>
$ sudo python3 orchestration
<h3> To kill the processes, run </h3>
$ ./kill_rogue_unprivileged.sh
$ ./search_python_process.sh
<h2>About the project.</h2>
SelfieLessActs is a cloud-based web application, that is used to share information about anything that is good for soceity that you 
observe.<br>
Examples of such acts could be<br>
● Picking up a piece of garbage and dumping it in a garbage can<br>
● Road getting laid in your area<br>
● Someone helping a blind man cross the road.<br>
● You helping your mother at home in the kitchen.<br>

<h2>DIRECTORY STRUCTURE</h2>
act_management --- contains files for running acts container<br>
data --- contains data of users and acts <br>
static --- contains .css and .js files<br>
templates --- contains .html<br>
user_management --- contains files for running user container<br>
logs --- logs while running containers<br>
pre-run.sh --- flushes data and creates folders<br>
server.py --- cloud web app when users and acts are on same instance<br>
base64encoder.py --- base64 encoding in python <br>

<h4>The following part constitutes the main part of front-end functionality.</h4>

The SelfieLessActs application will allow users of the application to
upload image of the act with a small caption and a categories. A user
of the application will be presented with a screen that<br>
● Shows them lists of categories on which Acts have been shared.
An act is a combination of an image and a caption for that
image.<br>
● Allows them to select to a topic.<br>
● On selection, they will be shown all Acts in a category sorted in
reverse chronological order (latest image first).<br>
● Upvote a particular Act.<br>
● Upload an Act.<br>
● Delete an Act.<br>

<h2>The entire application is built using AWS(Amazon Web Service).</h2>

The following constitutes of the backend functionality.<br>
APIs are implemented for the following functions<br>
1. Add a user<br>
2. Remove a user<br>
3. Add a category<br>
4. Remove a category<br>
5. List acts for a given category<br>
6. List number of acts for a given category<br>
7. Return number of acts for a given category<br>
8. Upvote an act<br>
9. Remove an act<br>
10. Upload an act.<br>

You need Flask installed on your PC before running this code.<br>
$ pip install Flask

To run the cloud based web app, edit the ip_address variable in server.py and then run,<br>
$ python3 server.py

To run the cloud-based apps,<br>
1) build the image<br>
2) run the container on port 8080 mapped 80 for user_management.py and 8000 mapped to 80 for act_management.py<br>

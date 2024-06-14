from flask import Flask , request , redirect , render_template

################ modules imports ##############

from modules.login_credential import users_credential
from modules.user import users_module
from modules.errors import error_logs
from modules.listdir import ls

############ usr defined parameters ############

re_login_time = 1 ### time after re-login is required ( in hours )
folder_path = "./share"

##############################################

app = Flask(__name__,template_folder="Templates")
app.config["SESSION_PERMANENT"] = False

##############################################

def authenticate_user(username,password,ipaddress):
    if username in users_credential.keys():
        if users_credential[username] == password:
            user = users_module.user(username,ipaddress)
            return True, user
        else:
            return False, None
    else:
        return False, None

##############################################

@app.route("/",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pass")
        ip_address = request.remote_addr
        status, user = authenticate_user(username,password,ip_address)
        if status is True:
            file_explor(user,folder_path)
        else:
            return render_template()
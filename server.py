from flask import Flask , request , redirect , render_template , send_file , send_from_directory

################ modules imports ##############

from modules.login_credential import user_credential
from modules.user import users_module
from modules.errors import error_logs
from modules.folder_operator import ls
from modules.folder_selector import get_folder

############ usr defined parameters ############

re_login_time = 1 ### time after re-login is required ( in hours )
folder_path = get_folder()

##############################################

app = Flask(__name__,template_folder="Template")
app.config["SESSION_PERMANENT"] = False

##############################################

def authenticate_user(username,password,ipaddress) -> any:
    if username in user_credential.keys():
        if user_credential[username] == password:
            user = users_module.user(username,ipaddress)
            return True, user
        else:
            return False, None
    else:
        return False, None

##############################################

def validate_folder(folder:str) -> bool:
    daughter_folder = folder.split("/")
    parent_folder = folder_path.split("/")
    for i in range(len(parent_folder)):
        if parent_folder[i] != daughter_folder[i]:
            return False
    return True

##############################################

def up_folder_path(folder:str) -> str:
    daughter_folder = folder.split("/")
    result_path = ""
    for i in range(len(daughter_folder)-1):
        result_path = result_path + "/" + daughter_folder[i]
    return result_path

##############################################

@app.route("/")
def index():
    return redirect("/login")

##############################################

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pass")
        ip_address = request.remote_addr
        status, user = authenticate_user(username,password,ip_address)
        if status is True:
            return file_explorer(user,folder_path)
        else:
            return render_template("./login form/index.html", login="False")
    return render_template("login form/index.html",login="True")

################################################

@app.route("/file",methods=['GET','POST'])
def file_explorer(user,folder_path):
    if user.validate_user() is True:
        if request.method == "POST":
            item_type = request.form.get("item_type")
            item_name = request.form.get("item_name")
            parent_folder = request.form.get("parent_folder")
            if item_type == "dir":
                if validate_folder(parent_folder+item_name) is True:
                    return file_explorer(user,folder_path=parent_folder+item_name)
            elif item_type == "file":
                if validate_folder(parent_folder) is True:
                    return send_file_to_client(user,folder_path+item_name)
            elif item_type == "up_dir":
                if validate_folder(up_folder_path(parent_folder)) is True:
                    return file_explorer(user,folder_path=up_folder_path(parent_folder))
            else:
                return render_template("share page/index.html",content=ls(folder_path),username=user.username,session_id=user.session_id,parent_folder=folder_path)
        else:
            return render_template("share page/index.html",content=ls(folder_path),username=user.username,session_id=user.session_id,parent_folder=folder_path)
        
###################################################

@app.route('/download_file/{file_name}')
def send_file_to_client(user,file_path):
    try:
        if user.validate_user() is True:
            return send_file(file_path)
    except Exception as error:
        error_logs(error,send_file_to_client)
        return file_explorer(user,folder_path)
    
#################################################

if __name__ == "__main__":
    app.run(debug=False)
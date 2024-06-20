from flask import Flask , request , redirect , render_template , send_file , url_for , send_from_directory


################ modules imports ##############

from modules.login_credential import user_credential
from modules.user import users_module
from modules.errors import error_logs
from modules.folder_operator import ls
from modules.folder_selector import get_folder
from modules.random_secret import secret_generator , secret_set

############ usr defined parameters ############

re_login_time = 1 ### time after re-login is required ( in hours )
initial_folder_path = get_folder()

##############################################

parser = dict()

##############################################

app = Flask(__name__,template_folder="Template")
app.config["SESSION_PERMANENT"] = False
app.config['UPLOAD_FOLDER'] = initial_folder_path

##############################################

# CERT_FILE = "./certificates/cert.pem"
# KEY_FILE = "./certificates/key.pem"

# context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# context.load_cert_chain(CERT_FILE,KEY_FILE)

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
    try:
        daughter_folder = folder.split("/")
        parent_folder = initial_folder_path.split("/")
        if daughter_folder.__len__() < parent_folder.__len__():
            return False
        for i in range(len(parent_folder)):
            if parent_folder[i] != daughter_folder[i]:
                return False
        return True
    except Exception as error:
        error_logs(error,validate_folder)
        return False

##############################################

def up_folder_path(folder:str) -> str:
    daughter_folder = folder.split("/")
    result_path = daughter_folder[0]
    for i in range(1,len(daughter_folder)-1):
        result_path = result_path + "/" + daughter_folder[i]
    return result_path

##############################################

def send_file_helper(path):
    new_path = path.split("/")
    res_path , filename = new_path[0] , new_path[-1]
    for i in range(1,len(new_path)-1):
        res_path = res_path + "/" + new_path[i]
    return res_path,filename

##############################################

@app.route("/")
def index():
    return redirect("/login")

##############################################

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("pass")
            ip_address = request.remote_addr
        except:
            return render_template("login form/index.html",login='True')
        status, user = authenticate_user(username,password,ip_address)
        if status is True:
            secret = secret_generator(16)
            parser[secret] = [user,initial_folder_path]
            return redirect(url_for('.file_explorer',parser_key=secret))
        else:
            return render_template("login form/index.html", login="False")
    return render_template("login form/index.html",login="True")

################################################

@app.route("/file",methods=['GET','POST'])
def file_explorer():
    try:
        secret = request.args['parser_key']
        user , folder_path = parser[secret]
        del parser[secret]
        secret_set.remove(secret)
    except:
        return redirect('/login')
    if user.validate_user() is True:
        if request.method == "POST":
            item_type = request.form.get("item_type")
            item_name = request.form.get("item_name")
            parent_folder = request.form.get("parent_folder")
            if item_type == "dir":
                if validate_folder(parent_folder+"/"+item_name) is True:
                    secret = secret_generator(16)
                    parser[secret] = [user,parent_folder+"/"+item_name]
                    return redirect(url_for('.file_explorer',parser_key=secret))
                else:
                    secret = secret_generator(16)
                    parser[secret] = [user,parent_folder]
                    message = "Page is Forbidden to access. You have no permission to access this page"
                    return render_template('error page/index.html',message=message,code=403,secret=secret)
            elif item_type == "file":
                if validate_folder(parent_folder) is True:
                    secret = secret_generator(16)
                    parser[secret] = [user,parent_folder+"/"+item_name]
                    return redirect(url_for('.send_file_to_client',parser_key=secret))
                else:
                    secret = secret_generator(16)
                    parser[secret] = [user,parent_folder]
                    message = "Page is Forbidden to access. You have no permission to access this page"
                    return render_template('error page/index.html',message=message,code=403,secret=secret)
            elif item_type == "up_dir":
                if validate_folder(up_folder_path(parent_folder)) is True:
                    secret = secret_generator(16)
                    parser[secret] = [user,up_folder_path(parent_folder)]
                    return redirect(url_for('.file_explorer',parser_key=secret))
                else:
                    secret = secret_generator(16)
                    parser[secret] = [user,parent_folder]
                    message = "Page is Forbidden to access. You have no permission to access this page"
                    return render_template('error page/index.html',message=message,code=403,secret=secret),403
            elif item_type == "refresh":
                if validate_folder(parent_folder) is True:
                    secret = secret_generator(16)
                    parser[secret] = [user,initial_folder_path]
                    return redirect(url_for('.file_explorer',parser_key=secret))
                else:
                    secret = secret_generator(16)
                    parser[secret] = [user,parent_folder]
                    message = "Page is Forbidden to access. You have no permission to access this page"
                    return render_template('error page/index.html',message=message,code=403,secret=secret),403
            else:
                secret = secret_generator(16)
                parser[secret] = [user,parent_folder]
                message = "Page is not found. The request is invalid"
                return render_template('error page/index.html',message=message,code=404,secret=secret),404
        elif request.method =="GET":
            secret = secret_generator(16)
            parser[secret] = [user,folder_path]
            return render_template("share page/index.html",content=ls(folder_path),username=user.username,session_id=user.session_id,parent_folder=folder_path,secret=secret)
    else:
        return redirect('/login')
        
###################################################

@app.route('/download_file')
def send_file_to_client():
    try:
        secret = request.args['parser_key']
        user , file_path = parser[secret]
    except:
        return redirect("/login")
    try:
        if user.validate_user() is True:
            file_path_ , filename = send_file_helper(file_path)
            return send_from_directory(file_path_,filename)
    except Exception as error:
        error_logs(error,send_file_to_client)
        secret = secret_generator(16)
        parser[secret] = [user,initial_folder_path]
        return redirect(url_for('.file_explorer',parser_key=secret))
    
#################################################

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000',debug=True,threaded=True)
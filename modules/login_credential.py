import json
from path.database_paths import user_credential_database_path

def login_credential_loader(path):
    with open(path) as file:
        return json.load(file)
    

user_credential = login_credential_loader(user_credential_database_path)
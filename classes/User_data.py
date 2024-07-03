import re
import getpass
import hashlib
import json
from classes.Functions import UserUtilities




class User_Data:
    def __init__(self):
        pass
        
    def verification_username(username:str):
        from classes.functions_admin import Manager
        
        users=Manager.load_json_file("databases/Users.json" ,"r+", {})
        
        if username in users:
            return False ,"Username already exists. Please choose a different username."
        else:
            return True , ""
    
    def email_verification(email:str , list_email:dict):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, email) is None:
            return False, "Invalid email address. Please enter a valid email."    
        if any(user_data['email'] == email for user_data in list_email.values()):
            return False, "Email address already exists. Please enter a different email."
        return True, ""
    def input_data():
            try:
                with open("Databases/Users.json", "r+", encoding="UTF-8") as file:
                    file.seek(0)
                    try:
                        users = json.load(file)
                    except json.JSONDecodeError:
                        users = {}
            except FileNotFoundError:
                users = {}

            print("Register your account")
            name = input("Enter your name: ")
            while True:
                username = input("Enter your username: ")
                ver_user , message_username = User_Data.verification_username(username)
                if ver_user == False:
                    print(message_username)
                else:
                    break
                    
                    
            
            
            
            '''
            while True:
                username = input("Enter your username: ")
                if username in users:
                    print("Username already exists. Please choose a different username.")
                else:
                    break
            '''
            while True:
                email = input("Enter your email: ")
                ver_email , message_email = User_Data.email_verification(email, users)
                if ver_email:
                    print(f"Your email is being verified. A verification code will be sent to you via email ....")
                else:
                    print(message_email)
                Validation_code= UserUtilities.generate_verification_codes() 
                UserUtilities.send_email(email ,username, Validation_code=Validation_code )
                print("A verification code has been sent to your email")
                while True:
                    code=input("Enter the code : ")
                    if code != Validation_code:
                        print(f"The code is incorrect")
                    else:
                        break
                break

                    
            while True:
                password = getpass.getpass("Enter your password: ")
                verification_password = getpass.getpass("Re-enter your password: ")
                if password == verification_password:
                    break
                else:
                    print("Password does not match. Please enter a matching password.")
            
            
            hash_password = User_Data.hash_password(password)
            users[username] = {
            
                'username':username,
                'name': name,
                'email': email,
                'password': hash_password
            }
            print("User data has been saved successfully  you can log in now")
            

            try:
                with open("Databases/Users.json", "r+", encoding="UTF-8") as file:
                    json.dump(users, file, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Error: {e}")
    def hash_password(password):
        hash_password = hashlib.sha256(password.encode()).hexdigest()
        return hash_password
    def login_user():
        print("-"*15 , "LOGIN", "-"*15)
        with open("Databases/Users.json", "r+", encoding="UTF-8") as file:
            file.seek(0)
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
        
        
        while True:
            UserName=input("User Name : ")
            Password=getpass.getpass("password : ")
            hash_password= User_Data.hash_password(Password)
            for user_data in users.values():
                    if 'username' in user_data and 'password' in user_data:
                        if user_data['username'] == UserName and user_data['password'] == hash_password:
                            email_user=user_data['email']
                            name=user_data['name']
                            Validation_code= UserUtilities.generate_verification_codes() 
                            UserUtilities.send_email(email_user ,user_data['username'] , Validation_code=Validation_code )
                            print("A verification code has been sent to your email (If you want to go back to logging in type 'back')")
                            while True:
                                code=input("Enter the code : ")
                                if code == "back":
                                    break
                                elif code != Validation_code:
                                    print("The code is incorrect")
                                    continue
                                else:
                                    
                                    session={}
                                    session={
                                        'username':UserName,
                                        'email':email_user,
                                        'name':name
                                    }
                                    from classes.functions_admin import Manager
                                    Manager.dump_json_file("databases/session.json", 'w',session , {})
                                    return True 
                                    
                            
                        
            print("Invalid username or password.")
            exit=input("Do you want to return to the home page? If yes write “y” If you want to continue write “n” : ")
            if exit.lower()=="y":
                break
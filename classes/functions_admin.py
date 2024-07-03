import json
from classes.Functions import UserUtilities
import getpass
import sys

class Manager:
    def __init__(self) -> None:
       pass
    def login_admin(self):
        from classes import User_Data
        print("-"*15 , "LOGIN", "-"*15)
        admin= self.load_json_file('Databases/admin.json', 'r+' , {})
        while True:
            UserName=input("User Name : ")
            Password=getpass.getpass("password : ")
            hash_password= User_Data.hash_password(Password)
            for user_data in admin.values():
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
                                    
                                    self.dump_json_file("databases/session.json", 'w',session , {})
                                    self.main_menu()
                                    
                                    
                            
                        
            print("Invalid username or password.")
            exit=input("Do you want to return to the home page? If yes write “y” If you want to continue write “n” : ")
            if exit.lower()=="y":
                break
    def main_menu(self):
        while True:
            choice=input("""
Main Menu
            
1. Add Book
2. Add Category
3. Edit User
4. Exit
                         
Enter your choice: """)
            

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.add_category()
            elif choice == "3":
                self.edit_user()
            elif choice == "4":
                print("Exiting...")
                sys.exit()
                
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")
    
    def dump_json_file(self,file_path, mode, lists, default_value):
        try:
            with open(file_path, mode, encoding="UTF-8") as file:
                json.dump(lists, file, ensure_ascii=False, indent=4)
                return True  
        except FileNotFoundError:
            return False  
        except json.JSONDecodeError:
            return default_value  
    
    def load_json_file(self,file_path, mode, default_value):
        try:
            with open(file_path, mode, encoding="UTF-8") as file:
                file.seek(0)
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return default_value
        except FileNotFoundError:
            return default_value

    
    def add_book(self):
    
        
        try:
            colors=UserUtilities.colors()
            Books = self.load_json_file("Databases/book.json", "r+", {})
            category = self.load_json_file("Databases/category.json", "r+", [])

            while True:
                name_book = input("Enter the name of the book > ")
                description_book = input(" Enter the book description > ")

                while True:
                    try:
                        price = int(input("Enter the price of the book (number only) > "))
                    except ValueError:
                        print(f"{colors['Red']}The book price must consist of numbers only. Please try again")
                    else:
                        break

                while True:
                    print(f"{colors['Blue']}Choose the book category")
                    for num, categor in enumerate(category, 1):
                        print(f"{num} - {categor}")
                    specified_category = input("Type the desired category > ")
                    if specified_category not in category:
                        print(f"{colors['Red']}Category not found. Please select an existing category")
                    else:
                        break
                Check_the_book = False
                for cat, books in Books.items():
                    if any(book['name_book'] == name_book for book in books):
                        print(f"{colors['Red']}The book '{name_book}' already exists in the category '{cat}'.")
                        Check_the_book = True
                        break

                if Check_the_book:
                    continue
                if specified_category not in Books:
                    Books[specified_category] = []
                Books[specified_category].append({
                    'name_book': name_book,
                    'description_book': description_book,
                    'price': price,
                })

                try:
                    with open("Databases/book.json", "w", encoding="UTF-8") as file:
                        json.dump(Books, file, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(f"Error: {e}")

                completion = input("Do you want to add more books? If yes write 'y' and if no 'n' ")
                if completion.lower() == "n":
                    break
        except KeyboardInterrupt:
            print(f"\n{colors['Blue']} We thank you for your effort, our dear manager. Take a break. Goodbye 🙄")

    
    def add_category(self):
        from classes.Functions import UserUtilities
        
        colors=UserUtilities.colors()
        category = self.load_json_file("Databases/category.json", "r+", [])

        while True:
            name_category = input("Enter the name of the category: ")
            if name_category not in category:
                category.append(name_category)
                try:
                    with open("Databases/category.json", "w", encoding="UTF-8") as file:
                        json.dump(category, file, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print(f"{colors['Blue']}Category already exists.")

            completion = input("Do you want to add more categories? If yes write 'y' and if no 'n' ")
            if completion.lower() == "n":
                break

    def edit_user(self):
        from classes.User_data import User_Data
        colors  = UserUtilities.colors()
        users = self.load_json_file("Databases/Users.json", "r+", {})
        while True:
            User_options=input("""
User options
                
1- Display all users
2- Search by user name
3- Modify user data                            
> """)
            
            if User_options == "1":
                print("-"*30)
                for num ,(key, user) in enumerate(users.items() , 1):
                    print(f"""
{num} - Name : {user['name']} 
• Username : {user['username']} 
• Email : {user['email']}""")
                print("-"*30)
            elif User_options == "2":
                User_name=input("Enter name : ")
                Availability_status=False
                for key, user in users.items():
                    if user['username'] == User_name:
                        print(f"Name: {user['name']} - Username: {user['username']} - Email: {user['email']}")
                        Availability_status=True
                        break
                if not Availability_status:
                    print(f"{colors['Red']} There is no user with this username")
            elif User_options == "3":
                User_name = input("Enter username: ")
                availability_status = False
                for key, user in users.items():
                    if user['username'] == User_name:
                        print(f"""
                              • Name: {user['name']} 
                              • Username: {user['username']} 
                              • Email: {user['email']}""")
                        
                        print("-" * 30)
                        print(f"{colors['Red']}The field in which you do not want to change anything, leave it as it is")
                        while True:
                            new_username = input("Enter the new username: ")
                            new_name = input("Enter the new name: ")
                            new_email = input("Enter the new email: ")
                            if len(new_email) > 0 :
                                email_verification , message_email=User_Data.email_verification(new_email , users)
                                if not email_verification:
                                    print(message_email)
                                    continue
                            elif len(new_username) > 0:
                                verification_username , message_username=User_Data.verification_username(new_username)
                                if not verification_username:
                                    print(message_username)
                                    continue
                            
                            break
                                
                        users[key]['username'] = new_username if new_username else users[key]['username']
                        users[key]['name'] = new_name if new_name else users[key]['name']
                        users[key]['email'] = new_email if new_email else users[key]['email']
                        
                        if new_username and new_username != key:
                            users[new_username] = users.pop(key)
                        self.dump_json_file("Databases/Users.json", "w", users, {})
                        print(f"{colors['Green']}Modified")
                        availability_status = True
                        break
                    
                if not availability_status:
                    print(f"{colors['Red']} There is no user with this username")
                
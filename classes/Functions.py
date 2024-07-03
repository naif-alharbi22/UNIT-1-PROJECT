
from colorama import Fore, Style, init
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import random
import string
import os
import datetime

class UserUtilities:
    def __init__(self) -> None:
        pass
    
    def lists(self):
        from classes import User_Data as user_data
        try:
            while True:
                result=input("""                
    1- Log in 
    2- Create a new account
    3- exit

    >  """)

                if result == "1":
                    Verification=user_data.login_user()
                    if Verification ==True:
                        UserUtilities.index()
                elif result == "2":
                    user_data.input_data()
                elif result == "3":
                    print("""
                            We are happy to have you here. Please visit us again 
                                        
                                    --  bye  --
                                        
                        """)
                    break
                else:
                    print("Option not found, please choose from the options above")
        except KeyboardInterrupt:
            print("\nWe are happy to have you here. Please visit us again\n\n--  bye  --")
            
    def index():
        try:
            colors  = UserUtilities.colors()
            while True:
                print(f"{colors['Blue']}Hello, we hope you are happy shopping with us and we are happy for you to contact us regarding any problem you face")
                choice=input(f"""
                                                Emeil:naif@niaf-alharbi.com
                                                
        1- Show categories
        2- View all books
        3- My library
        4- View my personal information
                    
        >  """)
                if choice == "1":
                    UserUtilities.Show_categories()
                elif choice == "2":
                    UserUtilities.the_books()
                elif choice == "3":
                    UserUtilities.My_library()
                elif choice=="4":
                    UserUtilities.My_info()
        except KeyboardInterrupt:
            print("\nWe are happy to have you here. Please visit us again\n\n--  bye  --")

                


    def colors():
        init(autoreset=True)
        colors = {
            'Red': Fore.RED,
            'Green': Fore.GREEN,
            'Blue': Fore.BLUE,
        }
        
        return colors 
    
    def send_email(User_email , User, path='Email_pages/Email_login_page.html',name_book=None , Validation_code=None ):
        sender_email = 'naif.n1158@gmail.com' 
        sender_password = 'wxfh iqwb pazh erqs' 
        with open(path, 'r') as file:
            html_content = file.read()
        
        html_content = html_content.replace('%USER%', User)
        

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = User_email
        
        
        if name_book!=None:
            msg['Subject'] = 'Your book has arrived 😍'
            html_content = html_content.replace('%BOOK_TITLE%', name_book)
            with open(f'books/{name_book}.pdf', 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                pdf_path=f'books/{name_book}.pdf'
                part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(pdf_path)}')
            msg.attach(part)
        else:
            msg['Subject'] = 'Verification Code for Login'
            html_content = html_content.replace('%CODE%', Validation_code)
        msg.attach(MIMEText(html_content, 'html'))
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, User_email, msg.as_string())
            server.quit()
            return True,  f'Email sent successfully to {User_email}'
        except Exception as e:
            return False, f'Error sending email: {str(e)}'
    def generate_verification_codes(code_length=6):
        characters = string.ascii_letters + string.digits  
        code = ''.join(random.choice(characters) for _ in range(code_length))
        return code

    def Show_categories():
        try:
            from classes.functions_admin import Manager
            category =Manager.load_json_file("Databases/category.json", "r+", [])
            books =Manager.load_json_file("Databases/book.json", "r+", [])
            colors  = UserUtilities.colors()
            while True:
                print(f"{colors['Blue']}Choose the book category")
                for num, categor in enumerate(category, 1):
                    print(f"{num} - {categor}")
                categories= input("Choose the category you want to enter or type 'back' to return to the main menu : ")
                if categories == "back":
                    return True
                if categories in books:
                    print(f"{colors['Blue']}-"*15, f"{colors['Blue']}Books in {categories}" , f"{colors['Blue']}-"*15)
                    for num ,name in enumerate(books[categories] ,1):
                        print(f"{num} - {name['name_book']} - {name['description_book']} - {name['price']}")
                    print(f"{colors['Blue']}-"*100)
                    choose=input("""
        1 - Buy a book
        2 - back 
        >  """)
                    if choose == "1":
                        UserUtilities.Buy_book(categories)
                    elif choose == "2":
                        continue
                else:
                    print("done") 
        except KeyboardInterrupt:
            print("\nWe are happy to have you here. Please visit us again\n\n--  bye  --")
          
    def Buy_book(categories = None):
        try:
            from classes.functions_admin import Manager
            colors  = UserUtilities.colors()
            username=Manager.load_json_file('databases/session.json' , 'r+' , {})
            colors=UserUtilities.colors()
            
            books =Manager.load_json_file("Databases/book.json", "r+", [])
            while True:
                Book_name = input(f"{colors['Blue']}Type the name of the book you want to get > ")
                Book_found = any(book['name_book'].lower() == Book_name.lower() for books_list in books.values() for book in books_list)
                if Book_found:
                    book_info = next((book for books_list in books.values() for book in books_list if book['name_book'].lower() == Book_name.lower()), None)
                    print(f"{colors['Red']}You are now trying to buy the book '{book_info['name_book']}', price is ${book_info['price']}. Complete the payment information to purchase:")
                    username_pay=username['username']
                    pay=Manager.load_json_file('databases/Payment_cards.json', 'r+',{})
                    if username_pay in pay:
                        user_pay = pay[username_pay]
                        if isinstance(user_pay, list):
                            user_pay = user_pay[0]
                
                            number_card = str(user_pay['number_card'])
                        Choose=input(f"{colors['Blue']}You have a previous card saved in your account that ends with the number {number_card[-4:]}. Do you want to use it? 'y' or 'n'")
                        if Choose == "y":
                            Card_number= user_pay['number_card']
                            year = user_pay['year']
                            month= user_pay['month']
                            ccv=user_pay['CCV']
                            UserUtilities.Purchase_by_card(username['username'] , Card_number , year , month , ccv, True)
                        elif Choose == "n":
                            UserUtilities.Purchase_by_card(username['username'] )
                    else:
                        UserUtilities.Purchase_by_card(username['username'])
                    Validation_code= UserUtilities.generate_verification_codes() 
                    UserUtilities.send_email(username['email'] , username['username'], 'Email_pages/pay_page.html',Validation_code=Validation_code)
                    print(f"{colors['Blue']}The purchase verification code has been sent to your email (if you want to cancel the order, write 'cancel')")
                    while True:
                        code=input("Enter the code : ")
                        if code == "cancel":
                            break
                        elif code != Validation_code:
                            print(f"The code is incorrect")
                            continue
                        else:
                            print(f"{colors['Blue']}Your purchase was completed successfully 👍")
                            try:
                                librarie= Manager.load_json_file('Databases/Libraries.json','r+' , {})
                                if username['username']not in librarie:
                                    librarie[username['username']]=[]
                                librarie[username['username']].append({
                                    'book_name':book_info['name_book'],
                                    'description_book':book_info['description_book'],
                                })
                                Manager.dump_json_file('Databases/Libraries.json' , 'r+', librarie , {})
                            except Exception as n:
                                print(n)
                            try:
                                ordars=Manager.load_json_file('databases/ordars.json' , 'r+', {})
                                username_user=username['username']
                                if username_user not in ordars:
                                    ordars[username_user]=[]
                                ordars[username_user].append({
                                    'book_name':book_info['name_book'],
                                    'description_book':book_info['description_book'],
                                    'Order_time':datetime.datetime.now().isoformat(),
                                    'price':book_info['price']
                                })
                                Manager.dump_json_file('Databases/ordars.json' , 'r+', ordars , {})
                            except Exception as n:
                                print(n)
                            break
                        
                else:
                    print(f"{colors['Red']}The book does not exist. Please make sure the book exists or is written correctly")
                    print(f"{colors['Red']}The book's name is wrong or you did not write it well")
                    back=input(f"{colors['Blue']}Do you want to try searching again for the book name? 'y' if you want to continue. 'n' if you want to return to the home page >")
                    if back == "n":
                        break
        except KeyboardInterrupt:
            print("\nWe are happy to have you here. Please visit us again\n\n--  bye  --")
        
    def Purchase_by_card(username, card_number=None , year=None , month=None , ccv=None , condition=False):
        from classes.functions_admin import Manager
        try:
            colors=UserUtilities.colors()
            if condition == False:
                while True:
                    try:
                        Card_number=int(input("enter card number : "))
                        year=int(input("Enter the year in the format (yyyy) : "))
                        month=int(input("Enter the month in the format (00): "))
                        ccv=int(input("Enter your three-digit CCV number : "))
                    except ValueError:
                        print(f"{colors['Red']}Only numbers must be entered")
                        continue
                    year_now =datetime.datetime.now().year
                    if len(str(Card_number)) in [13, 15, 16, 19] and year >= year_now and month <=12 and len(str(ccv))==3:
                        break
                    else:
                        print("The card is invalid")
                save=input("Do you want to save the payment method in your account? If yes, write 'y' If no, write 'n'")
                if save == "y":
                    card=Manager.load_json_file('databases/payment_cards.json', 'r+' , {})
                    if username not in card:
                        card[username]=[]
                    card[username].append({
                        'number_card':Card_number,
                        'year': year,
                        'month':month,
                        'CCV': ccv
                    })
                    card_file=Manager.dump_json_file('databases/payment_cards.json' , 'r+' , card , {})
                    print("The card has been saved in the account 👍")
        except KeyboardInterrupt:
            print("\nWe are happy to have you here. Please visit us again\n\n--  bye  --")
    def the_books():
        from classes.functions_admin import Manager
        try:
            books =Manager.load_json_file("Databases/book.json", "r+", [])
            for categories in books:
                print(f"* {categories}")
                for num ,book in enumerate(books[categories] , 1):
                    print(f"""
    {num} - {book['name_book']} - {book['description_book']} - Pricr: {book['price']}
                            """)
            Select_Book_List=input("""
                                
    Choose the option you want by writing the number in it only:

    1- I want to buy the curriculum book
    2- Return  
                                
    >  """)
            if Select_Book_List == "1":
                UserUtilities.Buy_book()
            elif Select_Book_List == "2":
                UserUtilities.index()
        except KeyboardInterrupt:
            print("\nWe are happy to have you here. Please visit us again\n\n--  bye  --")        
    def My_library():
        from classes.functions_admin import Manager
        try:
            library=Manager.load_json_file('Databases/Libraries.json' , 'r+',{})
            username=Manager.load_json_file('Databases/session.json' , 'r+' ,{} ) 
            user=username['username']
            user_email=username['email']
            if user in library:
                for num , book in enumerate(library[user] , 1):
                    print(f"{num} - {book['book_name']} - {book['description_book']}")
                install=input("Do you want to download a book to read? 'y' if the answer is yes, and if you want to return to the home page, type 'n'")
                if install == "y":
                    name_book_install=input("Type the name of the book you want to download > ")
                    if any(book['book_name'] == name_book_install for book in library[user]):
                        ver,msg = UserUtilities.send_email(user_email , user , 'Email_pages/send_book.html' , name_book_install )
                        if ver ==True:
                            print(msg)
                    else:
                        print(library[user])
            else:
                print("no books")
        except KeyboardInterrupt:
            print("\nWe are happy to have you here. Please visit us again\n\n--  bye  --")
           
    def My_info():
        from classes.User_data import User_Data
        colors=UserUtilities.colors()
        from classes.functions_admin import Manager
        
        users_old=Manager.load_json_file("Databases/Users.json", 'r+',{})
        user_session=Manager.load_json_file("Databases/session.json", 'r+',{})
        try:
            while True:
                print(f"{colors['Blue']}Your account information")
                print(f"""
        Name: {user_session['name']}
        Username: {user_session['username']}
        Email: {user_session['email']}             
                    """)
                chose_edit_info=input("""
        1- Modifying personal data 
        2- Return                
        > """)
                if chose_edit_info == "1":
                    print(f"{colors['Blue']}Choose what you want to change")
                    data=input(f"""
        1- Name: {user_session['name']}
        2- Username: {user_session['username']}
        3- Email: {user_session['email']}            
        > """)
                    if data == "1":
                        while True:
                            name=input("Enter the new name : ")
                            if len(name)>2:
                                users_old[user_session['username']]['name'] = name
                                user_session['name'] = name
                                Manager.dump_json_file('Databases/Users.json' , 'w',users_old , {})
                                Manager.dump_json_file('Databases/session.json' , 'w',user_session , {})
                                print(f"{colors['Blue']}Modified")
                                break
                            else:
                                print("The name must consist of more than two letters")
                                continue
                            
                    elif data == "2":
                        check_while=False
                        while True:
                            if check_while != True:
                                Username_new=input("Enter the new Username : ")
                                if len(Username_new)>2:
                                    check , msg=User_Data.verification_username(Username_new)
                                    if check != True:
                                        print(msg)
                                        continue
                                    elif check_while == True or Username_new == "back":
                                        break
                                    elif check == True:
                                        code=UserUtilities.generate_verification_codes()
                                        UserUtilities.send_email(user_session['email'] , user_session['name'] ,Validation_code=code, path='Email_pages/send_code_edit.html')
                                        print("A verification code has been sent to your email (If you want to go back to logging in type 'back')")
                                        while True:
                                            q_code=input("Enter the code : ")
                                            if q_code == "back":
                                                check_while=True
                                                break
                                            elif q_code != code:
                                                print("The code is incorrect")
                                                continue
                                            else: 
                                                users_old[user_session['username']]['username'] = Username_new
                                                users_old[Username_new]=users_old.pop(user_session['username'])
                                                user_session['username'] = Username_new
                                                Manager.dump_json_file('Databases/Users.json' , 'w',users_old , {})
                                                Manager.dump_json_file('Databases/session.json' , 'w',user_session , {})
                                                print(f"{colors['Blue']}Modified")
                                                check_while=True
                                                break
                                    else:
                                            print(f"{colors['Red']} The user name must consist of more than two letters")
                                            continue
                            else:
                                break        
                    elif data == "3":
                        while True :
                            email_new=input("Enter the new email : ")
                            check , msg=User_Data.email_verification(email_new , users_old)
                            if check !=True:
                                print(msg)
                                continue
                            elif check ==True:
                                code=UserUtilities.generate_verification_codes()
                                UserUtilities.send_email(user_session['email'] , user_session['name'] ,Validation_code=code, path='Email_pages/send_code_edit.html')
                                print("A verification code has been sent to your email (If you want to go back to logging in type 'back')")
                                while True:
                                    q_code=input("Enter the code : ")
                                    if q_code == "back":
                                        break
                                    elif q_code != code:
                                        print("The code is incorrect")
                                        continue
                                    else:
                                        user_session=Manager.load_json_file("Databases/session.json", 'r+',{})
                                        users_old[user_session['username']]['email']=email_new
                                        user_session['email']=email_new
                                        Manager.dump_json_file('Databases/Users.json' , 'w' ,users_old , {} )
                                        Manager.dump_json_file('Databases/session.json' , 'w' ,user_session , {} )
                                        print(f"{colors['Blue']}Modified")
                                        break
                                if q_code =="back":
                                    continue
                                else:
                                    break
                elif chose_edit_info == "2":
                    break
        except KeyboardInterrupt:
            print("\nWe are happy to have you here. Please visit us again\n\n--  bye  --")            
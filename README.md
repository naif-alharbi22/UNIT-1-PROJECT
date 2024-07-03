
# Electronic Library Backend

# Project Description
## The Electronic Library Backend is a web application designed to facilitate the purchase and download of books. Users can browse a collection of books, make purchases securely, and download their purchased books. The backend system handles user authentication, book catalog management, payment processing, and book download functionalities.

# Package used
```
Package         Version
--------------- -----------
art             6.2
colorama        0.4.6
matplotlib      3.9.0
```

# Running the Project
- Run cone to load the project with this command
```
git clone https://github.com/naif-alharbi22/UNIT-1-PROJECT.git
cd UNIT-1-PROJECT
python main.py
```
- Download the following libraries with their respective versions to ensure they work well 
```
Package         Version
--------------- -----------
art             6.2
colorama        0.4.6
matplotlib      3.9.0
```
- Open the main.py file, run it, and enjoy


# Technologies used
- Folder StructOTP system via email verification: used during purchase, data modification and login to enhance security.
- User Authentication: A secure user login and registration system.
- Book Catalog Management: Allows administrators to add books to the catalog.
- Payment Processing: Securely handles payment transactions for book purchases.
- Book Download Functions: Enables users to download their purchased books in PDF format.

# Folder Structure
```
project/
│
├── classes/
│   ├── Functions.py
│   ├── functions_admin.py
│   └── UserUtilities.py
│
├── Email_pages/
│   ├── Email_login_page.html
│   ├── pay_page.html
│   └── send_code_edit.html
│   └── send_book.html
|
├── books/
│   |Here are the books
|
├── Databases/
│   ├── Users.json
│   ├── session.json
│   └── Libraries.json
│   └── admin.json
|   └── book.json
|   └── category.json
│   └── orders.json
│   └── Payment_card.json
├── main.py
├── main_admin.py
├── requirements.txt
└── README.md
```
# Install dependencies
```
pip install -r requirements.txt
```

# Contact
```
Email:naif.n1158@gmail.com
```

This program is be able to read and write to the .csv file, 
as well as support multiple levels of user access 
(Guest, User, Superuser, and Administrator)
Security information, terms, and definitions have been implemented properly

# INSTRUCTIONS

## Requirements
* Python 3.7 or higher
* Pip
* sqlite3
* os
* shutil
* csv 
* pandas
* numpy

## Installing the requirements
```
pip install requirements.txt
```

open this folder in the console
type:

```
python main.py
```

# Workflow
The python program is divided into three files and the file main.py is to be launched. 
* io_spreadsheet: READ  / WRITE to the .csv file
* utilities: DATA ANALYSIS and DATA EXTRACTION
* main.py (ONLY OPEN THIS FILE)

The following program is a well defined implementation of the four different level of user access:

* ## Guest access:
    The guest can only view some comany specific analysis information
* ## User access: 
    The user can view some company specific analysis information but can also possess his very own profile and some details. The user cannot access other user's information.
* ## Superuser access: 
    The superuser can view all the company specific analysis information, Edit, Delete and add more Rows to the sample.csv and can also possess his very own profile. The superuser also can access, create and manage and delete all the information of the users.

* ## Administrator access:
    The administrator is the top level. He has read/write access to all the information of the company and can also possess his very own profile. He can create, delete, update and manage the information of all the superusers. The administrator cannot access the information of the users.

# Important points to note
    * For the system to work there should be an administrator and a superuser.
    
    * Only the administrator can add or delete a superuser.

    * The default administrator credentials are:
        * Username: admin
        * Password: admin
    
    * Log in with the administrator account with the credentials given to add a superuser.

    
    

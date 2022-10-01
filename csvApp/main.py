import sqlite3
import os
import shutil
import io_spreadsheet
import utilities

# create the database directory if does not exist
if not os.path.exists('db'):
    os.mkdir('db')

# create the backup if does not exist
if not os.path.exists('.backup'):
    os.mkdir('.backup')
if not os.path.exists('.backup/sample.csv'):
    shutil.copy("sample.csv", './.backup/')

# function to clear the console
def clearConsole(): return os.system('cls'
                                     if os.name in ('nt', 'dos') else 'clear')


# connect to database
conn = sqlite3.connect('./db/accounts.db')

# create cursor
c = conn.cursor()

# this function generates the initial tables if they are not presernt


def create_tables():
    # create table
    # the unique ROW ID gets assigned for each patient
    # When the account gets created
    c.execute("""
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL,
            pass text NOT NULL
        );
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS superuser(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL,
            pass text NOT NULL
        );
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS admin(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL,
            pass text NOT NULL
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS info(
            id text PRIMARY KEY NOT NULL,
            address text,
            phone INTEGER,
            email text,
            age text,
            department text
        );
    """)

    # Create an admin if does not exist
    # Very important
    c.execute("""
        INSERT OR REPLACE INTO admin(name, pass) VALUES('admin', 'admin');
    """)

    conn.commit()


def setHeader(value):
    # set the header (top part)
    clearConsole()
    print(f"""{'-'*15}|    {value}    |{'-'*15}\n""")


def promptInput(message="", keys=[]):
    # prompt user for input INFINITELY until a valid input is given
    print(message)
    usrInput = ""
    while(True):
        usrInput = input()
        if usrInput in keys:
            return usrInput
        else:
            print(f"Invalid Choice! Accepted values are{keys}")


class SuperUser:
    # SuperUser class for all the operations of the super user
    def __init__(self, actMgr=None):
        self.loginID = None
        self.username = None
        self.actMgr = actMgr
        self.userIDs = set()

    def setLoginCredentials(self, loginID, username):
        self.loginID = loginID
        self.username = username

    def logout(self):
        self.loginID = None
        self.username = None

    # A superuser has full access to all the users
    def viewUsers(self):
        setHeader("View Users")
        c.execute("SELECT * FROM user")
        for row in c.fetchall():
            self.userIDs.add(str(row[0]))
            print(row)

    def addUser(self):
        self.actMgr.createAccount(mode="superuser")

    def deleteUser(self):
        if self.userIDs:
            deleteID = promptInput("Enter user ID to delete: ",self.userIDs)
            status = self.actMgr.deleteAccount(mode="superuser", accType="user", accId=deleteID)
            if status:
                self.userIDs.remove(deleteID)
            return status
        else:
            print("You must view the users first")

    def viewUserInfo(self):
        userId = promptInput("Enter user ID to view info: ",self.userIDs)
        tempUser = self.actMgr.loginID
        self.actMgr.loginID = self.actMgr.types["user"]+userId
        self.actMgr.getProfileInfo()
        self.actMgr.loginID = tempUser

class Admin:
    # The administrator class for all the operations of the admin
    def __init__(self, actMgr=None):
        self.loginID = None
        self.username = None
        self.actMgr = actMgr
        self.superUserIDs = set()

    def setLoginCredentials(self, loginID, username):
        self.loginID = loginID
        self.username = username

    def logout(self):
        self.loginID = None
        self.username = None

    # An admin has full access to all the superusers
    def viewSuperUsers(self):
        setHeader("Viewing SuperUsers")
        c.execute("SELECT * FROM superuser")
        for row in c.fetchall():
            self.superUserIDs.add(str(row[0]))
            print(row)

    def addSuperUser(self):
        self.actMgr.createAccount(mode="admin")

    def deleteSuperUser(self):
        if self.superUserIDs:
            deleteID = promptInput("Enter user ID to delete: ",self.superUserIDs)
            status = self.actMgr.deleteAccount(mode="admin", accType="superuser", accId=deleteID)
            if status:
                self.superUserIDs.remove(deleteID)
            return status
        else:
            print("You must view the SuperUsers first")


class CompanyInfo:
    # A class for managing all the company specific information present in the csv
    def __init__(self,actMgr=None):
        self.actMgr = actMgr
    
    #authenticate the user access
    # check for superuser or admin
    def authenticate(self):
        if self.actMgr.loginID:
            if (self.actMgr.loginID[0] == self.actMgr.types["superuser"] 
                or self.actMgr.loginID[0] == self.actMgr.types["admin"]):
                return True
        return False

    def viewHighestSales(self):
        setHeader("Highest Sales")
        print(utilities.getHighestSales())

    def viewMostRecentSales(self):
        setHeader("Most Recent Sales")
        print(utilities.getMostRecentSales())

    def viewSegmentNames(self):
        setHeader("Segment Names")
        print(utilities.getSegmentNames())

    def viewHighestProfits(self):
        setHeader("Highest Profits")
        print(utilities.getHighestProfits())
    
    def viewAllData(self):
        if self.actMgr.loginID:
            if self.authenticate():
                setHeader("All Company Data")
                print(utilities.getAllData())
            else:
                print("You are not authorized to view this data")
        else:
            print("Warning! You must login first")

    def addNewRow(self):
        if self.actMgr.loginID:
            if self.authenticate():
                setHeader("Add new data for company")
                # Column Values

                
                segment = input("Segment name:   ")
                country = input("country name:   ")
                product = input("Product name:   ")
                discounts = input("Discount:     ")
                sales = input("sales:   ")
                profit = input("profit:     ")
                monthNumber = input("monthNumber:   ")
                year = input("year:     ")

                row = (segment, country, product,'','','','','', discounts, sales,'', profit,'', monthNumber,'', year)

                response = io_spreadsheet.Operate().write_data(data=row)
                print(response)
            else:
                print("You are not authorized to change this data")
        else:
            print("Warning! You must login first")

    def deleteRow(self):
        if self.actMgr.loginID:
            if self.authenticate():
                rowNum = int(input(f"Enter row number to delete: [1 to {utilities.getRowCount()}] "))
                if rowNum > 0 and rowNum <= utilities.getRowCount():
                    utilities.deleteRow(rowNum)
                    setHeader("Row deleted Successfully")
                else:
                    setHeader("Invalid row number")
            else:
                print("You are not authorized to change this data")
        else:
            print("Warning! You must login first")

class AccountManager:
    # A class for manaing all the accounts of user, superuser and admin
    def __init__(self):
        # this will be updated if used logs in
        self.loginID = None
        self.username = None
        self.types = {
            "user": "U",
            "admin": "A",
            "superuser": "S"
        }
        pass

    # function to check if a account exists

    def accountExists(self, accountType=None, username=None, password=None):
        c.execute(f"""
            SELECT * from {accountType}
            WHERE name = '{username}' AND pass = '{password}'
        """)
        found = c.fetchone()
        if found and username in found:
            userid = found[0]
            self.loginID = self.types[accountType] + str(userid)
            self.username = username
            return True
        else:
            self.loginID = None
            self.username = None

        return False

    def login(self, accountType):
        clearConsole()

        username = ""
        password = ""

        if accountType == "guest":
            setHeader("LOGGED IN AS GUEST")
            return True
        elif accountType in self.types.keys():
            username = input("Enter your username: ").lower()
            password = input("Enter your password: ")

            if self.accountExists(accountType, username, password):
                setHeader(
                    f"{accountType.capitalize()} login successful as {username}")
                return True
            else:
                setHeader("Account does not exist")
        else:
            setHeader("Invalid account type")

        return False

    def createAccount(self, mode="default"):
        types = {
            "user": "U",
            "admin": "A",
            "superuser": "S"
        }

        accountType = None
        if mode == "default":
            accountType = input(f"Enter the account type: {types.keys()}\n")
            if accountType != "user":
                print("You are only allowed to create a user account")
                response = promptInput("Try again: [y/n]: ", ["y", "n"])
                if response == "y":
                    self.createAccount()
                else:
                    return False
        elif mode == "superuser":
            setHeader("ADDING USER FROM SUPERUSER ACCOUNT: ACCESS GRANTED")
            accountType = "user"
        elif mode == "admin":
            setHeader(
                "ADDING SUPERUSER FROM ADMINISTRATOR ACCOUNT: ACCESS GRANTED")
            accountType = "superuser"
        if accountType in types.keys():
            username = input("Enter username: ").lower()
            password = input("Enter password: ")
            if self.accountExists(accountType, username, password):
                print("Error! Account already exists")
            else:
                # insert into the desired database
                c.execute(f"""  
                    INSERT INTO {accountType}(name, pass)
                    VALUES('{username}', '{password}')
                """)

                # obtain the row id of the inserted row
                rowid = c.lastrowid
                c.execute(f"""
                    SELECT id from {accountType}
                    WHERE rowid = {rowid}
                """)

                # get the id of the inserted row from rowid
                id = c.fetchone()[0]

                # initialize the info table with the id eg: U1, A1, S1
                c.execute(f"""  
                    INSERT INTO info(id)
                    VALUES('{types[accountType]}{id}')
                """)

                conn.commit()
                print("Account created successfully")
                return True

        else:
            print("Invalid account type")
            return False

    def deleteAccount(self,mode="default",accType=None,accId=None):
        try:
            c.execute(f"""
                DELETE FROM {accType}
                WHERE id = '{accId}'
            """)

            c.execute(f"""
                DELETE FROM info
                WHERE id = '{self.types[accType]}{accId}'
            """)

            conn.commit()
            return True
        except sqlite3.Error() as e:
            print(e)
        return False
        

    def getProfileInfo(self):
        c.execute(f"""
            SELECT * from info
            WHERE id = '{self.loginID}'
        """)

        found = c.fetchone()

        if found:
            accountType = [k for k, v in self.types.items() if v == self.loginID[0]]

            setHeader("PROFILE INFORMATION")

            print("username    : ", self.username)
            print("account type: ", accountType[0])
            print("address     : ", found[1])
            print("phone       : ", found[2])
            print("email       : ", found[3])
            print("age         : ", found[4])
            print("department  : ", found[5])
        else:
            setHeader("No profile information found")

    def setProfileInfo(self):
        address = input("Enter your address     : ")
        phone = input("Enter your phone number: ")
        email = input("Enter your email       : ")
        age = input("Enter your age         : ")
        department = input("Enter your department  : ")

        c.execute(f"""
            UPDATE info
            SET address = '{address}', phone = {phone}, email = '{email}',
            age = '{age}', department = '{department}'
            WHERE id = '{self.loginID}'
        """)

        conn.commit()
        setHeader("Profile information updated successfully")



class Dashboard:
    # Contains all the dashboards
    # Has an instance of all the other classes
    def __init__(self, actMgr=None, su=None, admin=None, compInfo=None):
        self.actMgr = actMgr
        self.admin = admin
        self.compInfo = compInfo
        self.su = su
        pass

    # MAIN DASHBOARD
    def dashboard(self):
        clearConsole()
        print("WELEOME TO THE Login System")

        print("1: Guest Login")
        print("2: User Login")
        print("3: SuperUser Login")
        print("4: Admin Login")
        print("5: Create Account")
        print("q: Quit")
        choice = input("Enter Choice: ")
        if choice == '1':
            status = self.actMgr.login(accountType="guest")
            if status:
                self.guestDashboard()
        elif choice == '2':
            status = self.actMgr.login(accountType="user")
            if status:
                self.userDashboard()
        elif choice == '3':
            status = self.actMgr.login(accountType="superuser")
            if status:
                self.su.setLoginCredentials(
                    self.actMgr.loginID, self.actMgr.username)
                self.superuserDashboard()
        elif choice == '4':
            status = self.actMgr.login(accountType="admin")
            if status:
                self.admin.setLoginCredentials(
                    self.actMgr.loginID, self.actMgr.username)
                self.adminDashboard()
        elif choice == '5':
            status = self.actMgr.createAccount()
            if status:
                self.dashboard()
            else:
                setHeader("Account creation failed")
                response = promptInput("go back to dashboard: [y/n]: ", ["y", "n"])
                if response == "y":
                    self.dashboard()
                else:
                    exit()
        elif choice == 'q' or choice == 'Q':
            exit()
        else:
            print("Invalid Choice")

    def salesDashboard(self):
        clearConsole()
        # These options are available publicly
        print("1: View top 5 highest sale values")
        print("2: View 5 most recent sales")
        print("3: List the types of segments")

        # These options are only available to superusers and administrators
        print("4: View All the data")
        print("5: Delete Row")
        print("6: Add new data")

        print("b: Back")

        choice = input("Enter Choice: ")
        if choice == '1':
            self.compInfo.viewHighestSales()
        elif choice == '2':
            self.compInfo.viewRecentSales()
        elif choice == '3':
            self.compInfo.viewSegmentNames()
        elif choice == '4':
            self.compInfo.viewAllData()
            response = promptInput("b = back", ["b"])
            if response == "b":
                self.salesDashboard()
        elif choice == '5':
            self.compInfo.deleteRow()
            response = promptInput("b = back", ["b"])
            if response == "b":
                self.salesDashboard()
        elif choice == '6':
            self.compInfo.addNewRow()
            response = promptInput("b = back", ["b"])
            if response == "b":
                self.salesDashboard()
        elif choice == 'b' or choice == 'B':
            return
        else:
            print("invalid choice")

    def guestDashboard(self):
        print("1: View Company Sales Dashboard")
        print("b: Back")
        choice = input("Enter Choice: ")
        if choice == '1':
            self.salesDashboard()
        elif choice == 'b' or choice == 'B':
            self.dashboard()
        else:
            print("Invalid Choice")

    def userDashboard(self):
        print("Welcome to the User Dashboard")
        print("1. View my profile")
        print("2: Update my profile information")
        print("3: View Sales Dashboard")
        print("4: Delete My Account")
        print("b: Back")
        choice = input("Enter Choice: ")
        if choice == '1':
            self.actMgr.getProfileInfo()
        elif choice == '2':
            self.actMgr.setProfileInfo()
        elif choice == '3':
            self.salesDashboard()
        elif choice == '4':
            status = self.actMgr.deleteAccount(mode="default",accType="user", accId=self.actMgr.loginID[1:])
            if status:
                response = promptInput("Account deleted successfully, go back to dashboard: [y/n]: ", ["y", "n"])
                if response == "y":
                    self.dashboard()
                else:
                    exit()
        elif choice == 'b' or choice == 'B':
            self.dashboard()
        else:
            print("Invalid Choice")

    def superuserDashboard(self):
        clearConsole()
        print("Welcome to the SuperUser Dashboard")
        print("1: View Users")
        print("2: Add a User")
        print("3: Delete a User")
        print("4: View Company information")
        print("5: View my Profile")
        print("6: Update my Profile information")
        print("7: Delete my Account")
        print("8: View User Information")
        print("b: Log Out")
        choice = input("Enter Choice: ")
        if choice == '1':
            self.su.viewUsers()
            goBack = promptInput("b: back", ['b', 'B'])
            if goBack:
                self.superuserDashboard()
        elif choice == '2':
            self.su.addUser()
            goBack = promptInput("b: back", ['b', 'B'])
            if goBack:
                self.superuserDashboard()
        elif choice == '3':
            status = self.su.deleteUser()
            if status:
                response = promptInput("User deleted successfully, go back to dashboard: [y/n]: ", ["y", "n"])
                if response == "y":
                    self.superuserDashboard()
                else:
                    exit()
        elif choice == '4':
            self.salesDashboard()
        elif choice == '5':
            self.actMgr.getProfileInfo()
            goBack = promptInput("b: back", ['b', 'B'])
            if goBack:
                self.superuserDashboard()
        elif choice == '6':
            self.actMgr.setProfileInfo()
            goBack = promptInput("b: back", ['b', 'B'])
            if goBack:
                self.superuserDashboard()
        elif choice == '7':
            status = self.actMgr.deleteAccount(mode="superuser",accType="superuser", accId=self.actMgr.loginID[1:])
            if status:
                response = promptInput("Account deleted successfully, go back to dashboard: [y/n]: ", ["y", "n"])
                if response == "y":
                    self.dashboard()
                else:
                    exit()
        elif choice == '8':
            self.su.viewUserInfo()
            goBack = promptInput("b: back", ['b', 'B'])
            if goBack:
                self.superuserDashboard()
        elif choice == 'b' or choice == 'B':
            self.su.logout()
            self.dashboard()
        else:
            print("Invalid Choice")

    def adminDashboard(self):
        clearConsole()
        print("Welcome Administrator")
        print("1: View SuperUsers")
        print("2: Add a SuperUser")
        print("3: Delete a SuperUser")
        print("4: View Company information")
        print("5: View my Profile")
        print("6: Update my Profile information")
        print("b: Log Out")
        choice = input("Enter Choice: ")
        if choice == '1':
            self.admin.viewSuperUsers()
            goBack = promptInput("b: back", ['b', 'B'])
            if goBack:
                self.adminDashboard()
        elif choice == '2':
            self.admin.addSuperUser()
            goBack = promptInput("b: back", ['b', 'B'])
            if goBack:
                self.adminDashboard()
        elif choice == '3':
            status = self.admin.deleteSuperUser()
            if status:
                response = promptInput("SuperUser deleted successfully, go back to dashboard: [y/n]: ", ["y", "n"])
                if response == "y":
                    self.adminDashboard()()
                else:
                    exit()
        elif choice == '4':
            self.salesDashboard()
        elif choice == '5':
            self.actMgr.getProfileInfo()
            goBack = promptInput("b: back", ['b', 'B'])
            if goBack:
                self.adminDashboard()
        elif choice == '6':
            self.actMgr.setProfileInfo()
            goBack = promptInput("b: back", ['b', 'B'])
            if goBack:
                self.adminDashboard()
        elif choice == 'b' or choice == 'B':
            self.admin.logout()
            self.dashboard()
        else:
            print("Invalid Choice")


def main():
    create_tables()

    # All the instances are kept track of in the main function
    accountManager = AccountManager()
    superUser = SuperUser(actMgr=accountManager)
    administrator = Admin(actMgr=accountManager)
    companyInfo = CompanyInfo(actMgr=accountManager)
    dashboard = Dashboard(actMgr=accountManager,
                          su=superUser, 
                          admin=administrator,
                          compInfo=companyInfo)

    dashboard.dashboard()


if __name__ == "__main__":
    main()

import csv  # this is a library that when we want to work with CSV file we will use it


# Define User class with no privileges at init
class Operate:

    # when we create initial user object what would be the attributes of this user, we use self object here
    def __init__(self):

        self.username = "user1"
        self.access = ['read', 'write']

    def read_data(self):  # This is function for reading data
        if 'read' in self.access:  # self.access means goes read and write
            with open('sample.csv') as File:
                reader = csv.DictReader(File)
                for row in reader:
                    print(row)
                return "Completed"
        else:
            return "You cant read data"

    def write_data(self,data):  # This is function for writing data
        if 'write' in self.access:

            with open('sample.csv', 'a') as File:
                writer = csv.writer(File)
                writer.writerow(data)
                return "Data Added Successfully"
        else:
            return "You cant write data"


def main():
    user = Operate()
    print(user.access)

    while True:
        try:
            # it store input data in Entry variable
            Entry = input("Enter what you want: ")

            if Entry == "read":
                # this will run Read data for the user object
                print(user.read_data())
                break

            if Entry == "write":  # this will run write data for the user object
                print(user.write_data())
                break
        except IOError as e:
            print("error" + e)


if __name__ == "__main__":
    main()

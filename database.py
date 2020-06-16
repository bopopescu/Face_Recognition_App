import datetime
import mysql.connector
import face_recognition

config = {'user': 'root',
          'password': '',
          'host': '127.0.0.1',
          'port': 3306,
          'database': 'FacesDB'}
useDB = "USE FacesDB; "


class MyDataBase:

    def getEmail(self, username):
        dbConnector = mysql.connector.connect(**config)
        print("Connected: " + str(dbConnector.is_connected()))
        c = dbConnector.cursor()
        # query = 'SELECT email FROM Faces WHERE username = %s'
        # c.execute(useDB + query, (username,))
        query = "SELECT face_img FROM FACES"
        email = c.fetchone()
        c.close()
        print("email: " + str(email))
        if email is None:
            return ""
        return email

    def getPassword(self, username):
        dbConnector = mysql.connector.connect(**config)
        c = dbConnector.cursor()
        query = 'SELECT password FROM Faces WHERE username = %s'
        username = "\'" + username + "\'"
        c.execute(useDB + query, (username,))
        password = c.fetchone()
        c.close()
        if password is None:
            print("password is none")
            return ""
        return password

    def getFaces(self):
        dbConnector = mysql.connector.connect(**config)
        c = dbConnector.cursor()
        query = 'SELECT face_img FROM Faces'
        c.execute(useDB + query)
        data = c.fetchall()
        c.close()
        photos = []
        for img in data:
            photos.append(img)
        return photos

    def addUser(self, firstName, lastName, username, password, email, gender, image):
        # add user
        firstName = "\'" + firstName + "\'"
        lastName = "\'" + lastName + "\'"
        username = "\'" + username + "\'"
        password = "\'" + password + "\'"
        email = "\'" + email + "\'"
        gender = "\'" + gender + "\'"
        image = "\'" + image + "\'"
        columns = "INSERT INTO Faces (username, password, first_name, last_name, gender, face_img, email) "
        data = "VALUES (" + username + ", " + password + ", " + firstName + ", " + lastName + ", " + gender + ", " + \
               image + ", " + email + ")"
        insert = useDB + columns + data
        print(insert)
        try:
            dbConnector = mysql.connector.connect(**config)
            c = dbConnector.cursor()
            c.execute(insert)
            dbConnector.commit()  # this command is apparently out of sync some how
            c.close()
            return True
        except mysql.connector.Error as err:
            print("something went wrong: {}".format(err))
            return False

        # need to store images as the encoded image in SQL
    def validate(self, username, password, photo):
        db = MyDataBase()
        db.getEmail(username)
        stored_password = db.getPassword(username)
        print("stored: " + str(stored_password))
        print("user: " + str(password))
        if stored_password != "" and password != "":
            if stored_password == password:
                # see if face is in database
                faces = db.getFaces()
                login_img = face_recognition.load_image_file(photo)
                encoded_login_img = face_recognition.face_encodings(login_img)[0]
                results = face_recognition.compare_faces(faces, encoded_login_img)
                count = 0
                for value in results:
                    if value:
                        return True
                return False
        else:
            return False


class DataBase:
    def __init__(self, filename, adminFileName):
        self.adminFileName = adminFileName
        self.filename = filename
        self.photos = []
        self.users = None
        self.file = None
        self.faces = []
        self.admins = {}
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}
        count = 0
        for line in self.file:
            if count == 24:
                count = 0
            count += 1
            first_name, last_name, email, gender, image = line.strip().split(";")
            self.users[image] = (first_name, last_name, email, gender, image)
            self.photos.append(image)
            encoding = face_recognition.load_image_file(image)
            encoding = face_recognition.face_encodings(encoding)[0]
            face_distances = face_recognition.face_distance(self.faces, encoding)
            self.faces.append(encoding)
        self.file.close()
        self.file = open(self.adminFileName, "r")
        for line in self.file:
            if line != "" and line is not None:
                username, password = line.strip().split(";")
                self.admins[username] = password
        self.file.close()

    def get_user(self, photo):
        print("users: " + str(self.users))
        if photo in self.users:
            return self.users[photo]
        else:
            return {}

    def add_user(self, first_name, last_name, email, gender, image):
        if image not in self.users:
            self.users[image] = (first_name.strip(), last_name, email, gender, image)
            self.save()
            encoding = face_recognition.load_image_file(image)
            encoding = face_recognition.face_encodings(encoding)[0]
            self.faces.append(encoding)
            return True
        else:
            print("Email exists already")
            return False

    def addAdmin(self, username, password):
        if username in self.admins.keys():
            return False
        self.admins[username] = password
        self.saveAdmin()
        return True

    def adminExists(self, username):
        if username in self.admins.keys():
            return True
        return False

    def searchUser(self, photo):
        print("photo: " + photo)
        login_img = face_recognition.load_image_file(photo)
        encoded_login_img = face_recognition.face_encodings(login_img)[0]
        results = face_recognition.compare_faces(self.faces, encoded_login_img)
        count = 0
        for value in results:
            if value:
                # print("LastTry OEWIFAWOIEFJA;OWEIFLSJAWE;OIFJAWEO;FILJAWEIO;SFLKJAWEIO;LJF")
                # print(str(self.users))
                # print(self.users[self.photos[count]][3])
                return self.photos[count]
            count += 1
        return ""

    def validate(self, username, password):
        if self.adminExists(username):
            if self.admins[username] == password:
                return True
            else:
                return False
            # login_img = face_recognition.load_image_file(live_photo)
            # encoded_login_img = face_recognition.face_encodings(login_img)[0]
            # results = face_recognition.compare_faces(self.faces, encoded_login_img)
            # for value in results:
            #     if value:
            #         return True
            # return False
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + ";" +
                        self.users[user][3] + ";" + self.users[user][4] + "\n")

    def saveAdmin(self):
        with open("admins.txt", "w") as f:
            print(self.admins)
            for key, value in self.admins.items():
                f.write(key + ";" + value + "\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]


import django
import django
from django.conf import settings
from django.http import HttpRequest
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from rest_framework import request
from mysite.myapi.apps import MyapiConfig
from database import DataBase, MyDataBase
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.mysite.settings")
from mysite.myapi.views import PersonViewSet, AdminViewSet, api_root
django.setup()


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()


class Editor(App):
    pass


class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    confirmPassword = ObjectProperty(None)

    def submit(self):
        if self.username.text != "" and self.password.text != "" and self.confirmPassword.text != "":
            if self.password.text == self.confirmPassword.text:
                # SQL DATABASE TODO
                if not db.addAdmin(self.username.text, self.password.text):
                    invalidUsername()
                    self.reset()
                else:
                    self.reset()
                    sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.password.text = ""
        self.confirmPassword.text = ""
        self.username.text = ""


class LoginWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.username.text, self.password.text):
            MainWindow.current = self.username.text
            self.reset()
            sm.current = "main"
        else:
            self.reset()
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.username.text = ""
        self.password.text = ""


class MainWindow(Screen):
    searchImage = ObjectProperty(None)

    def searchPerson(self):
        photo = db.searchUser(self.searchImage.text)
        if photo != "":
            UserWindow.current = photo
            self.reset()
            sm.current = "user"

    def addImageBtn(self):
        self.reset()

    def reset(self):
        self.searchImage.text = ""


class UserWindow(Screen):
    full_name = ObjectProperty(None)
    email = ObjectProperty(None)
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    gender = ObjectProperty(None)
    image = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def backToDB(self):
        sm.current = "main"

    def on_enter(self, *args):
        user = db.get_user(self.current)
        first_name, last_name, email, gender, image = db.get_user(self.current)

        self.full_name.text = "Name: " + first_name + " " + last_name
        self.email.text = "Email: " + email
        self.gender.text = "Gender: " + gender
        self.image.source = image
        # also want to load image onto page


class AddUserWindow(Screen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    email = ObjectProperty(None)
    gender = ObjectProperty(None)
    image = ObjectProperty(None)

    def addUser(self):
        if not db.add_user(self.first_name.text, self.last_name.text, self.email.text, self.gender.text,
                           self.image.text):
            invalidUsername()
        else:
            sm.current = "main"


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


def invalidUsername():
    pop = Popup(title='Invalid Username',
                content=Label(text="That username is already taken, please choose another one.",
                              size_hint=(.2, .2), size=(75, 75), pos_hint={"x": .4, "top": .5}))
    pop.open()


class MyMainApp(App):
    def build(self):
        return sm


unknown = api_root(HttpRequest())
print(str(PersonViewSet().highlight()))

kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase('users.txt', "admins.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"),
           UserWindow(name="user"), AddUserWindow(name="addUser")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"
Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)


if __name__ == "__main__":
    MyMainApp().run()

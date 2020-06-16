from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import os
from kivy.properties import ObjectProperty, StringProperty

Builder.load_string("""
<MyWidget>:
    id: my_widget
    Button
        text: "open"
        on_release: 
            my_widget.open(filechooser.path, filechooser.selection)
            root.nextPage()
    FileChooserIconView:
        id: filechooser
        on_selection: my_widget.selected(filechooser.selection)
        on_release: 
""")


class MyWidget(BoxLayout):

    def open(self, path, filename):
        with open(os.path.join(path, filename[0]), 'rb') as f:
            print(f.read())
        db.add_user(filename[0])

    def selected(self, filename):
        print("selected: %s" % filename[0])

    def nextPage(self):
        sm.current = "main"


class MyApp(App):
    def build(self):
        return MyWidget()


class WindowManager(ScreenManager):
    pass


class FirstWindow(Screen):
    pass


class MainWindow(Screen):
    image = ObjectProperty(rebind=True)

    def on_enter(self):
        print(type(self.image))
        self.image.source = db.getImage()


class DataBase:
    def __init__(self):
        self.users = []

    def add_user(self, image):
        print("made it")
        self.users.append(image)

    def save(self):
        with open("users1.txt", "w") as f:
            for user in self.users:
                print("user: " + str(self.users))
                f.write(self.users[user][0] + "\n")

    def getImage(self):
        return self.users[0]


screens = [FirstWindow(name="first"), MainWindow(name="main")]
db = DataBase()
sm = WindowManager()
for screen in screens:
    sm.add_widget(screen)
sm.current = "first"

if __name__ == '__main__':
    MyApp().run()

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("screens/home.kv")

class HomeScreen(Screen):
    def ir_para_login(self):
        self.manager.current = "login"

    def ir_para_cadastro(self):
        self.manager.current = "cadastro"

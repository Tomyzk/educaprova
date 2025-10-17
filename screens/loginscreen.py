from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("screens/login.kv")

class LoginScreen(Screen):
    def fazer_login(self):
        usuario = self.ids.usuario.text
        senha = self.ids.senha.text

        if usuario == "admin" and senha == "123":
            print("Login bem-sucedido!")
        else:
            print("Usuário ou senha incorretos!")

    def voltar_home(self):
        self.manager.current = "home"

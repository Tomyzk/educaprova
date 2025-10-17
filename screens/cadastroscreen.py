from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("screens/cadastro.kv")

class CadastroScreen(Screen):
    def cadastrar(self):
        usuario = self.ids.usuario.text
        senha = self.ids.senha.text
        print(f"Usuário cadastrado: {usuario}")

    def voltar_home(self):
        self.manager.current = "home"

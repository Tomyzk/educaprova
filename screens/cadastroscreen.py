from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from services.usuarios_service import cadastrar_usuario

class CadastroScreen(MDScreen):
    def cadastrar(self):
        nome = self.ids.nome.text.strip()
        email = self.ids.email.text.strip()
        senha = self.ids.senha.text.strip()

        if not nome or not email or not senha:
            toast("Preencha todos os campos!")
            return

        resultado = cadastrar_usuario(nome, email, senha)
        toast(resultado)

        if "sucesso" in resultado.lower():
            self.manager.current = "login"

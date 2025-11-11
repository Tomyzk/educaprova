from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from services.usuarios_service import verificar_login

class LoginScreen(MDScreen):
    def fazer_login(self):
        email = self.ids.email.text.strip()
        senha = self.ids.senha.text.strip()

        if not email or not senha:
            toast("Preencha todos os campos!")
            return

        if verificar_login(email, senha):
            toast("Login realizado com sucesso!")
            self.manager.current = "criarprova"
        else:
            toast("Usuário ou senha incorretos.")

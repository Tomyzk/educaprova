from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from services.usuarios_service import verificar_login


class LoginScreen(MDScreen):
    def fazer_login(self):
        email = self.ids.email.text.strip()
        senha = self.ids.senha.text.strip()

        usuario = verificar_login(email, senha)

        if usuario:
            toast(f"Bem-vindo, {usuario['nome']}")
            print(f"Login bem-sucedido: {usuario}")
            self.manager.current = "criarprova"
        else:
            toast("Usuário ou senha incorretos")
            print("Falha no login")

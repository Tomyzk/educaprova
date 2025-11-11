from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from services.usuarios_service import cadastrar_usuario


class CadastroScreen(MDScreen):
    def cadastrar(self):
        """
        Coleta os dados do formulário e cadastra o usuário no banco de dados.
        """
        # Acessa os campos do KV
        nome = self.ids.nome.text.strip()
        email = self.ids.email.text.strip()
        senha = self.ids.senha.text.strip()

        if not nome or not email or not senha:
            toast("Preencha todos os campos!")
            return

        # Chama o serviço de banco
        resultado = cadastrar_usuario(nome, email, senha)

        # Exibe a mensagem na tela e no terminal
        toast(resultado)
        print(resultado)

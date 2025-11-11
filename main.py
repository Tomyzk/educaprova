from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen

# -------------------------------
# IMPORTA SUAS TELAS
# -------------------------------
from screens.homescreen import HomeScreen
from screens.loginscreen import LoginScreen
from screens.cadastroscreen import CadastroScreen
from screens.criarprovascreen import CriarProvaScreen

# (Se você ainda não tiver um arquivo específico para LoadingScreen,
# pode deixar ela definida aqui mesmo no main.py)
class LoadingScreen(MDScreen):
    pass


# -------------------------------
# GERENCIADOR DE TELAS
# -------------------------------
class GerenciadorTelas(ScreenManager):
    pass


# -------------------------------
# APLICAÇÃO PRINCIPAL
# -------------------------------
class EducaProvaApp(MDApp):
    def build(self):
        # Define propriedades do app
        self.title = "EducaProva"
        self.icon = "assets/logo1.png"

        # Define tamanho de janela (opcional, apenas para desktop)
        Window.size = (360, 800)

        # Carrega o arquivo KV principal
        return Builder.load_file("educaprova.kv")


if __name__ == "__main__":
    EducaProvaApp().run()

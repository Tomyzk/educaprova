from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

# ---- TELAS ----
class HomeScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class CadastroScreen(Screen):
    pass

class CriarProvaScreen(Screen):
    def abrir_popup_pdf(self):
        print("Importar PDF")

    def importar_jpg(self):
        print("Importar JPG")

    def gerar_prova(self):
        # Mostra tela de carregamento
        self.manager.current = "loading"
        # Simula 2 segundos de geração
        Clock.schedule_once(self.voltar_criarprova, 2)

    def voltar_criarprova(self, dt):
        self.manager.current = "criarprova"


class LoadingScreen(Screen):
    pass


class GerenciadorTelas(ScreenManager):
    pass


class EducaProvaApp(MDApp):
    def build(self):
        self.title = "EducaProva Concurso"
        self.icon = "assets/logoprincipal.png"
        Window.size = (360, 800)
        return Builder.load_file("educaprova.kv")

if __name__ == "__main__":
    EducaProvaApp().run()

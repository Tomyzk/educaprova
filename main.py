from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

# ---- TELAS ----
class HomeScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class CadastroScreen(Screen):
    pass

# ---- GERENCIADOR DE TELAS ----
class GerenciadorTelas(ScreenManager):
    pass

# ---- APP PRINCIPAL ----
class EducaProvaApp(MDApp):
    def build(self):
        self.title = "EducaProva Concurso"
        self.icon = "assets/logoprincipal.png"
        Window.size = (360, 800)
        return Builder.load_file("educaprova.kv")

if __name__ == "__main__":
    EducaProvaApp().run()

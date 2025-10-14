from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

# Define as telas
class HomeScreen(Screen):
    pass

class EducaProvaApp(MDApp):
    def build(self):
        self.title = "EducaProva Concurso"
        self.icon = "assets/logo.png"
        Window.size = (360, 640)  # tamanho padrão de celular
        return Builder.load_file("educaprova.kv")

if __name__ == "__main__":
    EducaProvaApp().run()

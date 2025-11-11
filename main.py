import sys
import os

# 🔧 CAMINHO ABSOLUTO até a pasta principal do seu projeto
sys.path.insert(0, r"C:\Users\gcsbr.terceirizado\educaprova-3")

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen

from screens.homescreen import HomeScreen
from screens.loginscreen import LoginScreen
from screens.cadastroscreen import CadastroScreen
from screens.criarprovascreen import CriarProvaScreen


class LoadingScreen(MDScreen):
    pass


class GerenciadorTelas(ScreenManager):
    pass


class EducaProvaApp(MDApp):
    def build(self):
        self.title = "EducaProva"
        self.icon = "assets/logo1.png"
        Window.size = (360, 800)
        return Builder.load_file("educaprova.kv")


if __name__ == "__main__":
    EducaProvaApp().run()

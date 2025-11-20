from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from kivy.clock import Clock

# importa a função que fala com a IA
from services.rag_generate import gerar_prova as gerar_prova_ia


class CriarProvaScreen(MDScreen):
    def abrir_popup_pdf(self):
        toast("Importar PDF ainda não está disponível nesta versão.")

    def importar_jpg(self):
        toast("Importar JPG ainda não está disponível nesta versão.")

    def gerar_prova(self):
        """
        Lê o texto do campo, chama a IA e (por enquanto) mostra o resultado no console.
        """
        campo = self.ids.get("campo_texto_prova")
        if not campo:
            toast("Erro interno: campo de texto não encontrado.")
            return

        tema = (campo.text or "").strip()
        if not tema:
            toast("Digite um tema ou área da prova.")
            return

        # se você quiser usar a tela de loading:
        if self.manager:
            self.manager.current = "loading"

        Clock.schedule_once(lambda dt: self._chamar_ia(tema), 0)

    def _chamar_ia(self, tema: str):
        try:
            # gera 5 questões nível médio
            resultado = gerar_prova_ia(tema, qtd=5, dificuldade="médio")

            # volta para a tela de criar prova
            if self.manager:
                self.manager.current = "criarprova"

            toast("Prova gerada! (veja no console)")
            print("===== PROVA GERADA =====")
            print(resultado)
            
        except Exception as e:
            if self.manager:
                self.manager.current = "criarprova"
            toast(f"Erro ao gerar prova: {e}")
            print("Erro ao gerar prova:", e)

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder


class CriarProvaScreen(MDScreen):
    dialog_pdf = None

    def abrir_popup_pdf(self):
        if not self.dialog_pdf:
            self.dialog_pdf = MDDialog(
                title="📄 Importar PDF",
                type="custom",
                content_cls=MDBoxLayout(
                    orientation="vertical",
                    spacing="10dp",
                    size_hint_y=None,
                    height="120dp",
                    children=[],
                ),
                buttons=[
                    MDRaisedButton(
                        text="Selecionar arquivo",
                        md_bg_color=(0.1, 0.5, 0.8, 1),
                        on_release=self.importar_pdf
                    ),
                    MDFlatButton(
                        text="Fechar",
                        text_color=(1, 0, 0, 1),
                        on_release=lambda x: self.dialog_pdf.dismiss()
                    ),
                ],
            )

            label_box = MDBoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height="80dp",
                md_bg_color=(0.95, 0.95, 0.95, 1),
                radius=[15],
            )

            from kivymd.uix.label import MDLabel
            label_box.add_widget(
                MDLabel(
                    text="Arraste ou selecione seu arquivo PDF",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=(0.1, 0.1, 0.1, 1)
                )
            )

            self.dialog_pdf.content_cls.add_widget(label_box)

        self.dialog_pdf.open()

    def importar_pdf(self, *args):
        # Aqui você pode colocar o código para abrir o seletor de arquivo
        print("Usuário clicou em 'Selecionar arquivo'")
        self.dialog_pdf.dismiss()

    def importar_jpg(self):
        print("Usuário clicou em Importar JPG")

    def gerar_prova(self):
        print("Gerando prova...")

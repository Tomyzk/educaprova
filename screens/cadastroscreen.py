from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog

import requests

# Mantém a KV separada e sem alterações
Builder.load_file("screens/cadastro.kv")


# Endpoints da API (ajuste aqui se necessário)
API_REGISTER = "http://127.0.0.1:8000/apiregister"


class CadastroScreen(Screen):
    dialog = None
    _wired = False
    _nome_field = None
    _email_field = None
    _senha_field = None

    def on_kv_post(self, base_widget):
        if not self._wired:
            Clock.schedule_once(self._wire_widgets, 0)

    def _wire_widgets(self, *_):
        for w in self.walk(restrict=True):
            if isinstance(w, MDTextField):
                hint = (getattr(w, "hint_text", "") or "").lower()
                if hint.startswith("nome"):
                    self._nome_field = w
                elif hint.startswith("e-mail"):
                    self._email_field = w
                elif hint.startswith("senha"):
                    self._senha_field = w
            if isinstance(w, MDRaisedButton) and (getattr(w, "text", "") or "").strip().upper() in ("CADASTRAR", "CRIAR CONTA"):
                w.unbind(on_release=self._on_press_register)
                w.bind(on_release=self._on_press_register)
        self._wired = True

    def _open_dialog(self, title: str, text: str):
        if self.dialog:
            try:
                self.dialog.dismiss()
            except Exception:
                pass
        self.dialog = MDDialog(title=title, text=text, buttons=[])
        self.dialog.open()

    def _on_press_register(self, *_):
        nome = (self._nome_field.text if self._nome_field else "").strip()
        email = (self._email_field.text if self._email_field else "").strip()
        senha = (self._senha_field.text if self._senha_field else "").strip()

        if not nome or not email or not senha:
            self._open_dialog("Atenção", "Preencha nome, e-mail e senha.")
            return

        try:
            resp = requests.post(
                API_REGISTER,
                json={"nome": nome, "email": email, "senha": senha},
                timeout=15,
            )
        except requests.RequestException as e:
            self._open_dialog("Erro", f"Falha ao conectar: {e}")
            return

        if 200 <= resp.status_code < 300:
            self._open_dialog("Sucesso", "Cadastro realizado com sucesso!")
        else:
            msg = "Erro ao cadastrar."
            try:
                err = resp.json()
                if isinstance(err, dict):
                    msg = next((str(v) for v in err.values() if v), msg)
            except ValueError:
                pass
            self._open_dialog("Erro", msg if isinstance(msg, str) else str(msg))

    # Compatibilidade com método antigo
    def cadastrar(self):
        self._on_press_register()

    def voltar_home(self):
        if self.manager:
            self.manager.current = "home"

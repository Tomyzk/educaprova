from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog

import requests

# Mantém a KV separada e sem alterações
Builder.load_file("screens/login.kv")


# Endpoints da API (ajuste aqui se necessário)
API_LOGIN = "http://127.0.0.1:8000/apilogin"


class LoginScreen(Screen):
    dialog = None
    _wired = False
    _email_field = None
    _senha_field = None

    def on_kv_post(self, base_widget):
        # Faz o binding dos botões/inputs sem precisar alterar os .kv
        if not self._wired:
            Clock.schedule_once(self._wire_widgets, 0)

    def _wire_widgets(self, *_):
        # Localiza campos por hint_text e botão por texto
        for w in self.walk(restrict=True):
            if isinstance(w, MDTextField):
                if (getattr(w, "hint_text", "") or "").lower().startswith("e-mail"):
                    self._email_field = w
                elif (getattr(w, "hint_text", "") or "").lower().startswith("senha"):
                    self._senha_field = w
            if isinstance(w, MDRaisedButton) and (getattr(w, "text", "") or "").strip().upper() == "ENTRAR":
                w.unbind(on_release=self._on_press_login)
                w.bind(on_release=self._on_press_login)
        self._wired = True

    def _open_dialog(self, title: str, text: str):
        if self.dialog:
            try:
                self.dialog.dismiss()
            except Exception:
                pass
        self.dialog = MDDialog(title=title, text=text, buttons=[])
        self.dialog.open()

    def _on_press_login(self, *_):
        email = (self._email_field.text if self._email_field else "").strip()
        senha = (self._senha_field.text if self._senha_field else "").strip()

        if not email or not senha:
            self._open_dialog("Atenção", "Informe e-mail e senha.")
            return

        try:
            resp = requests.post(
                API_LOGIN,
                json={"email": email, "senha": senha},
                timeout=15,
            )
        except requests.RequestException as e:
            self._open_dialog("Erro", f"Falha ao conectar: {e}")
            return

        if 200 <= resp.status_code < 300:
            try:
                data = resp.json() if resp.content else {}
            except ValueError:
                data = {}

            # Tenta chaves comuns de JWT
            token = data.get("access") or data.get("token") or data.get("jwt")
            if not token:
                self._open_dialog("Erro", "Token JWT não retornado pelo servidor.")
                return

            app = App.get_running_app()
            setattr(app, "auth_token", token)

            self._open_dialog("Sucesso", "Login bem-sucedido!")
            # Troca para a tela de criar prova após breve atraso para o usuário ver o diálogo
            Clock.schedule_once(lambda *_: self._go_to_criaprova(), 0.4)
        else:
            msg = "Usuário ou senha incorretos."
            try:
                err = resp.json()
                if isinstance(err, dict):
                    # Mostra primeira mensagem legível, se houver
                    msg = next((str(v) for v in err.values() if v), msg)
            except ValueError:
                pass
            self._open_dialog("Erro", msg if isinstance(msg, str) else str(msg))

    def _go_to_criaprova(self):
        if self.dialog:
            try:
                self.dialog.dismiss()
            except Exception:
                pass
        if self.manager:
            self.manager.current = "criaprova"

    # Mantém compatibilidade com chamadas antigas (não usadas sem ids)
    def fazer_login(self):
        self._on_press_login()

    def voltar_home(self):
        if self.manager:
            self.manager.current = "home"

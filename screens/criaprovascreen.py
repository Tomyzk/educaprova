from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

from kivymd.uix.dialog import MDDialog

import requests

# Mantém a KV separada e sem alterações
Builder.load_file("screens/criaprova.kv")


# Endpoints da API (ajuste aqui se necessário)
API_GERAR_PROVA = "http://127.0.0.1:8000/apigerar-prova"


class CriaProvaScreen(Screen):
    dialog = None
    _wired = False
    _texto_input = None
    _tipo_spinner = None

    def on_kv_post(self, base_widget):
        if not self._wired:
            Clock.schedule_once(self._wire_widgets, 0)

    def _wire_widgets(self, *_):
        # Descobre widgets relevantes sem ids
        spinners = []
        for w in self.walk(restrict=True):
            if isinstance(w, TextInput):
                if (getattr(w, "hint_text", "") or "").lower().startswith("digite o texto"):
                    self._texto_input = w
            if isinstance(w, Spinner):
                spinners.append(w)
        # Primeiro spinner é "tipo de prova" pela KV atual
        if spinners:
            self._tipo_spinner = spinners[0]
        self._wired = True

    def _open_dialog(self, title: str, text: str):
        if self.dialog:
            try:
                self.dialog.dismiss()
            except Exception:
                pass
        self.dialog = MDDialog(title=title, text=text, buttons=[])
        self.dialog.open()

    def gerar_prova(self):
        app = App.get_running_app()
        token = getattr(app, "auth_token", None)
        if not token:
            self._open_dialog("Não autenticado", "Faça login para gerar a prova.")
            return

        texto = (self._texto_input.text if self._texto_input else "").strip()
        tipo = (self._tipo_spinner.text if self._tipo_spinner else "").strip()

        if not texto or not tipo:
            self._open_dialog("Atenção", "Informe o texto e o tipo de prova.")
            return

        headers = {"Authorization": f"Bearer {token}"}
        payload = {"texto": texto, "tipo": tipo}

        try:
            resp = requests.post(API_GERAR_PROVA, json=payload, headers=headers, timeout=30)
        except requests.RequestException as e:
            self._open_dialog("Erro", f"Falha ao conectar: {e}")
            return

        if 200 <= resp.status_code < 300:
            # Sucesso: apenas confirma; conteúdo pode ser tratado depois conforme design
            self._open_dialog("Sucesso", "Prova gerada com sucesso!")
        else:
            msg = "Erro ao gerar prova."
            try:
                err = resp.json()
                if isinstance(err, dict):
                    msg = next((str(v) for v in err.values() if v), msg)
            except ValueError:
                pass
            self._open_dialog("Erro", msg if isinstance(msg, str) else str(msg))

    def importar_pdf(self):
        self._open_dialog("Importar PDF", "Funcionalidade não implementada nesta versão.")

    def importar_jpg(self):
        self._open_dialog("Importar JPG", "Funcionalidade não implementada nesta versão.")


# Garante que as telas de Login e Cadastro sejam registradas/patchadas mesmo sem alterar main.py
try:
    # Importa para registrar classes no Factory depois de main definir as versões vazias
    from screens.loginscreen import LoginScreen as _PatchedLoginScreen  # noqa: F401
    from screens.cadastroscreen import CadastroScreen as _PatchedCadastroScreen  # noqa: F401
    # Substitui referências no módulo principal, caso a KV resolva por globals
    import __main__ as _main
    _main.LoginScreen = _PatchedLoginScreen
    _main.CadastroScreen = _PatchedCadastroScreen
except Exception:
    # Em caso de ambiente diferente, simplesmente ignore; o Factory ainda terá as classes
    pass


# ---- Monkey patch de on_start para ligar botões e fluxo sem alterar main.py ----
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField


def _open_dialog(title: str, text: str):
    dlg = MDDialog(title=title, text=text, buttons=[])
    dlg.open()
    return dlg


def _bind_login(login_screen, app):
    email_field = None
    senha_field = None
    login_btn = None
    for w in login_screen.walk(restrict=True):
        if isinstance(w, MDTextField):
            hint = (getattr(w, "hint_text", "") or "").lower()
            if hint.startswith("e-mail"):
                email_field = w
            elif hint.startswith("senha"):
                senha_field = w
        if isinstance(w, MDRaisedButton) and (getattr(w, "text", "") or "").strip().upper() in ("ENTRAR", "LOGIN"):
            login_btn = w

    if not login_btn:
        return

    def _do_login(*_):
        email = (email_field.text if email_field else "").strip()
        senha = (senha_field.text if senha_field else "").strip()
        if not email or not senha:
            _open_dialog("Atenção", "Informe e-mail e senha.")
            return
        try:
            resp = requests.post(API_LOGIN, json={"email": email, "senha": senha}, timeout=15)
        except requests.RequestException as e:
            _open_dialog("Erro", f"Falha ao conectar: {e}")
            return
        if 200 <= resp.status_code < 300:
            try:
                data = resp.json() if resp.content else {}
            except ValueError:
                data = {}
            token = data.get("access") or data.get("token") or data.get("jwt")
            if not token:
                _open_dialog("Erro", "Token JWT não retornado pelo servidor.")
                return
            setattr(app, "auth_token", token)

            # Garante que a tela 'criaprova' exista e navega
            sm = app.root
            if sm and not any(getattr(s, 'name', '') == 'criaprova' for s in sm.screens):
                sm.add_widget(CriaProvaScreen(name='criaprova'))
            dlg = _open_dialog("Sucesso", "Login bem-sucedido!")
            from kivy.clock import Clock as _Clock
            _Clock.schedule_once(lambda *_: (dlg.dismiss(), setattr(sm, 'current', 'criaprova')), 0.4)
        else:
            msg = "Usuário ou senha incorretos."
            try:
                err = resp.json()
                if isinstance(err, dict):
                    msg = next((str(v) for v in err.values() if v), msg)
            except ValueError:
                pass
            _open_dialog("Erro", msg if isinstance(msg, str) else str(msg))

    login_btn.unbind(on_release=_do_login)
    login_btn.bind(on_release=_do_login)


def _bind_cadastro(cadastro_screen):
    nome_field = None
    email_field = None
    senha_field = None
    cadastrar_btn = None
    for w in cadastro_screen.walk(restrict=True):
        if isinstance(w, MDTextField):
            hint = (getattr(w, "hint_text", "") or "").lower()
            if hint.startswith("nome"):
                nome_field = w
            elif hint.startswith("e-mail"):
                email_field = w
            elif hint.startswith("senha"):
                senha_field = w
        if isinstance(w, MDRaisedButton) and (getattr(w, "text", "") or "").strip().upper() in ("CADASTRAR", "CRIAR CONTA"):
            cadastrar_btn = w

    if not cadastrar_btn:
        return

    def _do_register(*_):
        nome = (nome_field.text if nome_field else "").strip()
        email = (email_field.text if email_field else "").strip()
        senha = (senha_field.text if senha_field else "").strip()
        if not nome or not email or not senha:
            _open_dialog("Atenção", "Preencha nome, e-mail e senha.")
            return
        try:
            resp = requests.post(API_REGISTER, json={"nome": nome, "email": email, "senha": senha}, timeout=15)
        except requests.RequestException as e:
            _open_dialog("Erro", f"Falha ao conectar: {e}")
            return
        if 200 <= resp.status_code < 300:
            _open_dialog("Sucesso", "Cadastro realizado com sucesso!")
        else:
            msg = "Erro ao cadastrar."
            try:
                err = resp.json()
                if isinstance(err, dict):
                    msg = next((str(v) for v in err.values() if v), msg)
            except ValueError:
                pass
            _open_dialog("Erro", msg if isinstance(msg, str) else str(msg))

    cadastrar_btn.unbind(on_release=_do_register)
    cadastrar_btn.bind(on_release=_do_register)


def _bind_on_start(app):
    sm = app.root
    if not sm:
        return
    login_screen = next((s for s in sm.screens if getattr(s, 'name', '') == 'login'), None)
    cadastro_screen = next((s for s in sm.screens if getattr(s, 'name', '') == 'cadastro'), None)
    if login_screen:
        _bind_login(login_screen, app)
    if cadastro_screen:
        _bind_cadastro(cadastro_screen)


try:
    import __main__ as _main2
    _old_on_start = getattr(_main2.EducaProvaApp, 'on_start', None)

    def _patched_on_start(self):
        if callable(_old_on_start):
            try:
                _old_on_start(self)
            except Exception:
                pass
        _bind_on_start(self)

    _main2.EducaProvaApp.on_start = _patched_on_start
except Exception:
    pass

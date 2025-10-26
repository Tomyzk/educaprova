# EducaProva Concurso — Backend (Django)

API REST em Django 5 com DRF + JWT. Suporte a MySQL (prod) e SQLite (dev), senhas com bcrypt e configuração por `.env`.

## Requisitos
- Python 3.10+
- MySQL 8 (ou compatível) — apenas para ambiente com `DB_ENGINE=mysql`
- Pacotes do `requirements.txt`

## Instalação
1. Crie um virtualenv e instale dependências:

   ```bash
   pip install -r educaprova_backend/requirements.txt
   ```

2. Copie o exemplo de variáveis e ajuste:

   - Copie `educaprova_backend/.env.example` para `educaprova_backend/.env`.
   - Em desenvolvimento, use `DB_ENGINE=sqlite` (padrão) para evitar depender do MySQL.
   - Em produção, defina `DB_ENGINE=mysql` e variáveis `MYSQL_*`.

3. Inicialize banco e usuário customizado:

   ```bash
   python educaprova_backend/manage.py makemigrations
   python educaprova_backend/manage.py migrate
   ```

4. Suba o servidor (dev):

   ```bash
   python educaprova_backend/manage.py runserver 0.0.0.0:8000
   ```

## Apps e funcionalidades
- `users`: cadastro, login JWT por e-mail, perfil, planos (Free/Premium)
- `provas`: CRUD de provas do usuário com limites para plano Free
- `core`: healthcheck (`/api/health/`)

## Endpoints principais
Base: `http://localhost:8000/api/`

- Healthcheck
  - `GET /api/health/` → `{ status: "ok", app: "EducaProva Concurso API" }`

- Autenticação/Usuários
  - `POST /api/users/register/` → cria usuário `{ username, email, password }`
  - `POST /api/users/token/` → `{ email, password }` → `{ access, refresh }`
  - `POST /api/users/token/refresh/` → `{ refresh }` → `{ access }`
  - `GET /api/users/profile/` (Bearer) → dados do usuário

- Provas (Bearer obrigatório)
  - `GET /api/provas/` → lista do usuário
  - `POST /api/provas/` → `{ titulo, descricao?, questoes? }`
  - `GET /api/provas/{id}/`
  - `DELETE /api/provas/{id}/`

## Integração com Kivy (exemplos)
```python
import requests
BASE = "http://127.0.0.1:8000/api"

# Registrar
requests.post(f"{BASE}/users/register/", json={
    "username": "henrique",
    "email": "h@example.com",
    "password": "SenhaForte123",
})

# Login
r = requests.post(f"{BASE}/users/token/", json={"email": "h@example.com", "password": "SenhaForte123"})
access = r.json()["access"]
headers = {"Authorization": f"Bearer {access}"}

# Perfil
requests.get(f"{BASE}/users/profile/", headers=headers).json()

# Criar prova
requests.post(f"{BASE}/provas/", json={"titulo": "Simulado 1", "descricao": "Teste"}, headers=headers)
```

## Observações
- `AUTH_USER_MODEL = 'users.User'` — use sempre este modelo.
- Hash de senha: `BCryptSHA256PasswordHasher` (requer `bcrypt`).
- JWT: `djangorestframework-simplejwt` (`/api/users/token/`).
- Banco: SQLite em dev (padrão) ou MySQL em prod (`PyMySQL` ou `mysqlclient`).

## Ambientes
- Dev: `DJANGO_SETTINGS_MODULE=educaprova_backend.settings.dev` (padrão do `manage.py`).
- Prod: `DJANGO_SETTINGS_MODULE=educaprova_backend.settings.prod` (padrão de `wsgi/asgi` se não setado).

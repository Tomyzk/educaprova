from database import conectar
import bcrypt


def cadastrar_usuario(nome, email, senha):
    conexao = conectar()
    if not conexao:
        return "Erro de conexão"

    cursor = conexao.cursor()
    try:
        # Criptografa a senha antes de salvar
        senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

        sql = "INSERT INTO usuarios (nome, email, senha_hash, tipo) VALUES (%s, %s, %s, %s)"
        dados = (nome, email, senha_hash, "professor")
        cursor.execute(sql, dados)
        conexao.commit()
        return "Usuário cadastrado com sucesso!"
    except Exception as e:
        conexao.rollback()
        if "Duplicate entry" in str(e):
            return "E-mail já cadastrado!"
        return f"Erro ao cadastrar: {e}"
    finally:
        cursor.close()
        conexao.close()


def verificar_login(email, senha):
    conexao = conectar()
    if not conexao:
        return False

    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT * FROM usuarios WHERE email = %s"
    cursor.execute(sql, (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()

    if usuario and bcrypt.checkpw(senha.encode("utf-8"), usuario["senha_hash"].encode("utf-8")):
        print(f"✅ Bem-vindo, {usuario['nome']}")
        return True
    else:
        print("❌ Usuário ou senha incorretos")
        return False

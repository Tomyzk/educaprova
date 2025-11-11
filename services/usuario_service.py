from database import conectar
import bcrypt


def cadastrar_usuario(nome, email, senha, tipo="professor"):
    """Cadastra novo usuário no banco com senha criptografada."""
    conexao = conectar()
    if not conexao:
        return "Erro de conexão ao banco."

    cursor = conexao.cursor()
    try:
        senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

        sql = """
        INSERT INTO usuarios (nome, email, senha_hash, tipo)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nome, email, senha_hash.decode("utf-8"), tipo))
        conexao.commit()

        return "Usuário cadastrado com sucesso!"
    except Exception as e:
        conexao.rollback()
        return f"Erro ao cadastrar: {e}"
    finally:
        cursor.close()
        conexao.close()


def verificar_login(email, senha):
    """Valida login comparando senha com o hash salvo no banco."""
    conexao = conectar()
    if not conexao:
        return None

    cursor = conexao.cursor(dictionary=True)
    try:
        sql = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        usuario = cursor.fetchone()

        if not usuario:
            return None

        senha_hash = usuario["senha_hash"].encode("utf-8")

        if bcrypt.checkpw(senha.encode("utf-8"), senha_hash):
            return usuario
        else:
            return None
    except Exception as e:
        print("Erro ao verificar login:", e)
        return None
    finally:
        cursor.close()
        conexao.close()

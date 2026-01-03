import sqlite3
import hashlib  # Para hashing de senhas

def criar_banco():
    conn = sqlite3.connect('lembretes.db')
    cursor = conn.cursor()
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    # Tabela de lembretes com user_id e recorrencia
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lembretes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mensagem TEXT NOT NULL,
            hora TEXT NOT NULL,
            recorrencia TEXT NOT NULL DEFAULT 'unico',
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_lembrete(mensagem, hora, recorrencia='unico', user_id=None):
    if user_id is None:
        raise ValueError("user_id é obrigatório para multi-usuários")
    conn = sqlite3.connect('lembretes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO lembretes (mensagem, hora, recorrencia, user_id) VALUES (?, ?, ?, ?)', (mensagem, hora, recorrencia, user_id))
    conn.commit()
    conn.close()

def listar_lembretes_com_id(user_id):
    conn = sqlite3.connect('lembretes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, mensagem, hora, recorrencia FROM lembretes WHERE user_id = ?', (user_id,))
    lembretes = cursor.fetchall()
    conn.close()
    return lembretes

def deletar_lembrete(id_lembrete, user_id):
    conn = sqlite3.connect('lembretes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lembretes WHERE id = ? AND user_id = ?', (id_lembrete, user_id))
    conn.commit()
    conn.close()

def registrar_usuario(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('lembretes.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verificar_login(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('lembretes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM usuarios WHERE username = ? AND password_hash = ?', (username, password_hash))
    usuario = cursor.fetchone()
    conn.close()
    return usuario[0] if usuario else None
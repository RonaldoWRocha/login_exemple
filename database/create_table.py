import sqlite3

def create_users_table():
    # Conecta ao banco de dados (ou cria um novo banco de dados se ele não existir)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Cria a tabela users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Salva as mudanças e fecha a conexão
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_users_table()
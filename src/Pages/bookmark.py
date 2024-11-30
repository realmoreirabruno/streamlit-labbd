import mysql.connector

# Função de conexão
def conectar_banco():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        port=3306,
        database='censo_escolar'
    )
    return conn

# Criar um bookmark de escola
def criar_bookmark_escola(conn, titulo, url):
    cursor = conn.cursor()
    query = "INSERT INTO bookmark (id_usuario, id_escola) VALUES (%s, %s)"
    valores = (titulo, url)
    cursor.execute(query, valores)
    conn.commit()
    cursor.close()

# Listar todos os bookmarks
def listar_bookmarks_escolas(conn):
    cursor = conn.cursor()
    query = "SELECT id, id_usuario, id_escola FROM bookmark WHERE id_escola LIKE 'Escola%'"
    cursor.execute(query)
    bookmarks = cursor.fetchall()
    cursor.close()
    return bookmarks

# Atualizar um bookmark de escola
def atualizar_bookmark_escola(conn, bookmark_id, novo_titulo, novo_url):
    cursor = conn.cursor()
    query = "UPDATE bookmark SET id_usuario = %s, id_escola = %s WHERE id = %s"
    valores = (novo_titulo, novo_url, bookmark_id)
    cursor.execute(query, valores)
    conn.commit()
    cursor.close()

# Deletar um bookmark de escola
def deletar_bookmark_escola(conn, bookmark_id):
    cursor = conn.cursor()
    query = "DELETE FROM bookmark WHERE id = %s"
    cursor.execute(query, (bookmark_id,))
    conn.commit()
    cursor.close()
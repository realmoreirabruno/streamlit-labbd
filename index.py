import streamlit as st
import mysql.connector

# Configuração da página
st.set_page_config(page_title="Login", initial_sidebar_state="collapsed")

# Conexão com o banco de dados
def conectar_banco():
    if "conn" not in st.session_state or not st.session_state.conn.is_connected():
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            port=3306,
            database='censo_escolar'
        )
        # Armazena a conexão no estado da sessão
        st.session_state.conn = conn
    return st.session_state.conn

# Função para validar login
def validar_login(email, senha):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    query = "SELECT id, nome FROM usuario WHERE email = %s AND senha = SHA(%s)"
    valores = (email, senha)
    cursor.execute(query, valores)
    resultado = cursor.fetchone()
    
    cursor.close()
    
    return resultado  # Retorna o ID e o nome do usuário, ou None se inválido

# Página de login
def pagina_login():
    if "logado" not in st.session_state or not st.session_state["logado"]:
        st.title("Login")
        email = st.text_input("Email:")
        senha = st.text_input("Senha:", type="password")
        login = st.button("Entrar")
        
        if login:
            usuario = validar_login(email, senha)
            if usuario:
                user_id, nome = usuario
                # Atualiza o estado para refletir que o login foi bem-sucedido
                st.session_state["logado"] = True
                st.session_state["nome_usuario"] = nome
                st.session_state["user_id"] = user_id
                st.success(f"Bem-vindo, {nome}!")
            else:
                st.error("Email ou senha inválidos!")

# Página principal (após login)
def pagina_principal():
    if "logado" in st.session_state and st.session_state["logado"]:
        st.write(f"Bem-vindo, {st.session_state['nome_usuario']}!")
    else:
        pagina_login()

pagina_principal()

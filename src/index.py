import streamlit as st
import mysql.connector

# Esconde a barra lateral e não exibe navegação inicialmente
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

# Função para validar login e obter o nome do usuário
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
    # Exibe o formulário de login
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
            else:
                st.error("Email ou senha inválidos!")

# Página principal (após o login bem-sucedido)
def pagina_principal():
    if st.session_state.get("logado", False):
        # Exibe a barra lateral apenas se o usuário estiver logado
        st.sidebar.title("Menu")
        st.sidebar.write("Opções de navegação aqui")

        # Exibe o título e a saudação do usuário
        st.title(f"Bem-vindo, {st.session_state['nome_usuario']}!")
        st.subheader("Censo Escolar")
    else:
        pagina_login()  # Exibe o formulário de login caso o usuário não tenha feito login ainda

# Controle de navegação
pagina_principal()  # Sempre chama a função principal, que controla se está logado ou não

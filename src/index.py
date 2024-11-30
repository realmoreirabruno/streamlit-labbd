import streamlit as st
import mysql.connector
from Pages.bookmark import criar_bookmark_escola, listar_bookmarks_escolas, atualizar_bookmark_escola, deletar_bookmark_escola

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
    
    query = "SELECT id, NOME FROM usuario WHERE email = %s AND senha = %s"
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

        # Função para a página de configurações
        def pagina_bookmark():
            st.title("Bookmarks")
    
            # Recupera os dados dos bookmarks
            bookmarks = listar_bookmarks()
            
            if bookmarks:
                for bookmark in bookmarks:
                    st.subheader(f"Id_Escola: {bookmark[2]}")
                    st.write("---")  # Separador entre os bookmarks
            else:
                st.write("Nenhum bookmark encontrado.")

        # Função para a página de configurações
        def pagina_IDEB():
            st.title("Página de Notas")

        # Função para a página de configurações
        def pagina_docentes():
            st.title("Página de Docentes")

        # Função para controle de navegação
        def controle_navegacao():
            # Sidebar com opções de navegação
            pagina = st.sidebar.radio("Escolha uma página", ["Principal", "Bookmark", "IDEB", "Docentes"])

            if pagina == "Bookmark":
                pagina_bookmark()
            elif pagina == "Principal":
                pagina_principal
            elif pagina == "IDEB":
                pagina_IDEB()
            elif pagina == "Docentes":
                pagina_docentes()

        # Chama o controle de navegação
        controle_navegacao()

        
    else:
        pagina_login()  # Exibe o formulário de login caso o usuário não tenha feito login ainda

# Controle de navegação
pagina_principal()  # Sempre chama a função principal, que controla se está logado ou não

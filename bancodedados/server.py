from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import sqlite3
import os

# Porta do servidor
PORT = 8080

# Caminho base (para facilitar achar os arquivos HTML)
BASE_DIR = os.path.dirname(__file__)

# --- Criação e atualização do banco de dados ---
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Criação da tabela de usuários com campo CPF
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(255) NOT NULL,
        cpf CHAR(11) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE,
        senha VARCHAR(30) NOT NULL
    )
''')

conn.commit()
conn.close()


# --- Classe do servidor ---
class SimpleServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            # Página de cadastro
            self._enviar_html(os.path.join(BASE_DIR, "../paginas/cadastro.html"))

        elif self.path == "/login":
            # Página de login
            self._enviar_html(os.path.join(BASE_DIR, "../paginas/login.html"))

        elif self.path.startswith("/conta?"):
            # Página da conta do usuário (após login)
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            email = params.get("email", [""])[0]
            senha = params.get("senha", [""])[0]

            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute("SELECT nome, cpf, email FROM usuarios WHERE email=? AND senha=?", (email, senha))
            usuario = cursor.fetchone()
            conn.close()

            if usuario:
                conteudo = f"""
                <h1>Bem-vindo, {usuario[0]}!</h1>
                <p><strong>CPF:</strong> {usuario[1]}</p>
                <p><strong>Email:</strong> {usuario[2]}</p>
                <a href="/login">Sair</a>
                """
                self._enviar_resposta(conteudo)
            else:
                self._enviar_resposta("<h1>Usuário não encontrado ou senha incorreta!</h1><a href='/login'>Voltar</a>")
        else:
            self.send_response(404)
            self.end_headers()

    # --- Requisições POST ---
    def do_POST(self):
        if self.path == "/cadastrar":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            dados = urllib.parse.parse_qs(post_data)

            nome = dados.get("nome", [""])[0]
            cpf = dados.get("cpf", [""])[0]
            email = dados.get("email", [""])[0]
            senha = dados.get("senha", [""])[0]

            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO usuarios (nome, cpf, email, senha) VALUES (?, ?, ?, ?)",
                    (nome, cpf, email, senha)
                )
                conn.commit()
                resposta = "<h1>Cadastro realizado com sucesso!</h1><a href='/login'>Ir para login</a>"
            except sqlite3.IntegrityError as e:
                if "cpf" in str(e).lower():
                    resposta = "<h1>CPF já cadastrado!</h1><a href='/'>Voltar</a>"
                elif "email" in str(e).lower():
                    resposta = "<h1>Email já cadastrado!</h1><a href='/'>Voltar</a>"
                else:
                    resposta = "<h1>Erro ao cadastrar!</h1><a href='/'>Voltar</a>"
            conn.close()

            self._enviar_resposta(resposta)

        elif self.path == "/login":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            dados = urllib.parse.parse_qs(post_data)

            email = dados.get("email", [""])[0]
            senha = dados.get("senha", [""])[0]

            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
            usuario = cursor.fetchone()
            conn.close()

            if usuario:
                self.send_response(302)
                self.send_header("Location", f"/conta?email={email}&senha={senha}")
                self.end_headers()
            else:
                self._enviar_resposta("<h1>Login inválido!</h1><a href='/login'>Tentar novamente</a>")
        else:
            self.send_response(404)
            self.end_headers()

    # --- Função para enviar HTML ---
    def _enviar_html(self, arquivo):
        try:
            with open(arquivo, "rb") as f:
                conteudo = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(conteudo)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    # --- Função para enviar resposta HTML simples ---
    def _enviar_resposta(self, conteudo):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(conteudo.encode("utf-8"))


# --- Inicia o servidor ---
with HTTPServer(("", PORT), SimpleServer) as server:
    print(f"Servidor rodando em http://localhost:{PORT}")
    server.serve_forever()
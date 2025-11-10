from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import sqlite3

PORT = 8080

# Criação/atualização do banco de dados
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Tabela com campo CPF
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
''')

conn.commit()
conn.close()


class SimpleServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self._enviar_html("cadastro.html")

        elif self.path == "/login":
            self._enviar_html("login.html")

        elif self.path.startswith("/conta?"):
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
                cursor.execute("INSERT INTO usuarios (nome, cpf, email, senha) VALUES (?, ?, ?, ?)",
                               (nome, cpf, email, senha))
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

    def _enviar_resposta(self, conteudo):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(conteudo.encode("utf-8"))


with HTTPServer(("", PORT), SimpleServer) as server:
    print(f"Servidor rodando em http://localhost:{PORT}")
    server.serve_forever()
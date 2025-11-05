// Importando módulos necessários
const express = require("express");
const mysql = require("mysql2");
const bcrypt = require("bcrypt");
const app = express();

// Configuração para receber dados em JSON
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Conexão com o banco de dados MySQL
const db = mysql.createConnection({
  host: "localhost",
  user: "root", // altere se o seu usuário for diferente
  password: "", // se tiver senha no MySQL, coloque aqui
  database: "AtivaMentee_db"
});

// Testar conexão com o banco
db.connect((err) => {
  if (err) {
    console.error("Erro ao conectar ao banco:", err);
  } else {
    console.log("Conexão com o MySQL bem-sucedida!");
  }
});

// Rota para cadastrar usuário
app.post("/cadastro", async (req, res) => {
  const { nome, cpf, email, senha } = req.body;

  // Criptografar a senha antes de salvar
  const hash = await bcrypt.hash(senha, 10);

  const sql = "INSERT INTO usuarios (nome, cpf, email, senha) VALUES (?, ?, ?, ?)";
  db.query(sql, [nome, cpf, email, hash], (err, result) => {
    if (err) {
      console.error("Erro ao cadastrar:", err);
      return res.status(500).send("Erro ao cadastrar usuário");
    }
    res.send("Usuário cadastrado com sucesso!");
  });
});

// Rota para login
app.post("/login", (req, res) => {
  const { email, senha } = req.body;

  const sql = "SELECT * FROM usuarios WHERE email = ?";
  db.query(sql, [email], async (err, results) => {
    if (err) return res.status(500).send("Erro no servidor");

    if (results.length === 0) {
      return res.status(401).send("Usuário não encontrado");
    }

    const user = results[0];
    const senhaCorreta = await bcrypt.compare(senha, user.senha);

    if (!senhaCorreta) return res.status(401).send("Senha incorreta");

    res.send("Login bem-sucedido!");
  });
});

// Rota para Fale Conosco
app.post("/faleconosco", (req, res) => {
  const { nome, email, telefone, assunto, mensagem } = req.body;

  const sql = "INSERT INTO fale_conosco (nome, email, telefone, assunto, mensagem) VALUES (?, ?, ?, ?, ?)";
  db.query(sql, [nome, email, telefone, assunto, mensagem], (err, result) => {
    if (err) {
      console.error("Erro ao enviar mensagem:", err);
      return res.status(500).send("Erro ao enviar mensagem");
    }
    res.send("Mensagem enviada com sucesso!");
  });
});

// Iniciar o servidor
app.listen(3000, () => {
  console.log("Servidor rodando em http://localhost:3000");
});

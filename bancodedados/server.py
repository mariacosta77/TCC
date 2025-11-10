from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

import os
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'html'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'styles')
)
app.secret_key = 'chave_secreta_segura'


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123abc",
    database="ativamente__db"
)
cursor = db.cursor(dictionary=True)


@app.route('/')
def index():
    return "Servidor Python rodando!"


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        senha = request.form['senha']

        cursor.execute("INSERT INTO usuarios (nome, cpf, email, senha) VALUES (%s, %s, %s, %s)",
                       (nome, cpf, email, senha))
        db.commit()
        flash("✅ Cadastro realizado com sucesso!")
        return redirect(url_for('login'))
    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor.execute("SELECT * FROM usuarios WHERE email=%s AND senha=%s", (email, senha))
        user = cursor.fetchone()

        if user:
            flash("✅ Login realizado com sucesso!")
            return redirect(url_for('index'))
        else:
            flash("❌ Email ou senha incorretos!")
    return render_template('login.html')

@app.route('/faleconosco', methods=['GET', 'POST'])
def faleconosco():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        cursor.execute("""
            INSERT INTO fale_conosco (nome, email, telefone, assunto, mensagem)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, email, telefone, assunto, mensagem))
        db.commit()
        flash("✅ Mensagem enviada com sucesso!")
        return redirect(url_for('faleconosco'))
    return render_template('faleconosco.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'chave-secreta-ativamente' 


def conectar_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',       
        password='123abc',        
        database='ativamente__db'
    )


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        senha = request.form['senha']

        conexao = conectar_banco()
        cursor = conexao.cursor()

        try:
            cursor.execute("INSERT INTO usuarios (nome, cpf, email, senha) VALUES (%s, %s, %s, %s)",
                           (nome, cpf, email, senha))
            conexao.commit()
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            flash(f'Erro ao cadastrar: {err}')
        finally:
            cursor.close()
            conexao.close()

    return render_template('cadastro.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email=%s AND senha=%s", (email, senha))
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()

    if usuario:
        flash(f"Bem-vindo(a), {usuario['nome']}!")
        return redirect(url_for('fale_conosco'))
    else:
        flash('E-mail ou senha incorretos!')
        return redirect(url_for('index'))


@app.route('/faleconosco', methods=['GET', 'POST'])
def fale_conosco():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO fale_conosco (nome, email, telefone, assunto, mensagem) VALUES (%s, %s, %s, %s, %s)",
            (nome, email, telefone, assunto, mensagem)
        )
        conexao.commit()
        cursor.close()
        conexao.close()

        flash('Mensagem enviada com sucesso!')
        return redirect(url_for('fale_conosco'))

    return render_template('faleconosco.html')


if __name__ == '__main__':
    app.run(debug=True)
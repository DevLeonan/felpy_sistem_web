from flask import Flask, render_template, redirect, request, flash, session
import sqlite3 as db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'leonanadm'

# Função para verificar se o usuário está logado
def verificar_login():
    if 'usuario' not in session:
        return redirect('/')
    
    else:
        return redirect('/usuarios')

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        email = request.form.get('email')
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')

        # conectar na tabela.
        conn = db.connect("Felpysistem.db")
        cursor = conn.cursor()
        # Verificar se os dados do usuário já existem no banco de dados
        cursor.execute("SELECT * FROM login WHERE email = ? OR usuario = ?", (email, usuario))
        if cursor.fetchone():
            flash('Usuário ou email já cadastrado', 'error')
        else:
            # Verificar se a senha foi confirmada corretamente
            if senha == confirmar_senha:
                # Inserir o usuário no banco de dados
                cursor.execute("INSERT INTO login (email, usuario, senha) VALUES (?, ?, ?)", (email, usuario, senha))
                conn.commit()
                conn.close()
                flash('Usuário criado com sucesso', 'success')
                return redirect('/login') # Redirecionar para a página de login após criar o usuário
            else:
                flash('As senhas não coincidem', 'error')

    return render_template('cadastrar.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        # Verificar se o email, usuario e senha estão corretos e existem no banco de dados
        with db.connect("Felpysistem.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login WHERE usuario = ? AND senha = ?", (usuario, senha))
            if cursor.fetchall():
                session['usuario'] = usuario  # Armazenar o email do usuário na sessão
                return redirect('/usuarios')
            else:
                flash('Login inválido', 'error')

    return render_template('login.html')


@app.route('/usuarios')
def usuarios():
    verificar_login()
    return render_template('usuarios.html')

@app.route('/logout')
def logout():
    if 'usuario' in session:
        flash('Você Saiu!', 'success')
        session.pop('usuario')
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)

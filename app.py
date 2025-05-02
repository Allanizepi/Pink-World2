from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Inicialização do Flask e do banco de dados
app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'  # Necessário para sessões de login

# Inicializando o banco de dados
db = SQLAlchemy(app)

# Inicializando o LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Modelo de Cliente
class Cliente(UserMixin, db.Model):  # Agora herda de UserMixin
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    agendamentos = db.relationship('Agendamento', backref='cliente', lazy=True)


class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    hora = db.Column(db.String(5), nullable=False)


# Modelo de Administrador
class Administrador(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)


# Função de carregamento de usuário
@login_manager.user_loader
def load_user(user_id):
    # Primeiramente, tenta carregar o cliente
    cliente = Cliente.query.get(int(user_id))
    if cliente:
        return cliente
    # Caso não seja encontrado como cliente, tenta como administrador
    return Administrador.query.get(int(user_id))


# Página inicial
@app.route('/')
def index():
    return render_template('index.html')


# Cadastro de Administrador
@app.route('/cadastro_admin', methods=['GET', 'POST'])
def cadastro_admin():
    if request.method == 'POST':
        username = request.form['username']
        senha = generate_password_hash(request.form['senha'], method='pbkdf2:sha256')  # Hash da senha

        novo_admin = Administrador(username=username, senha=senha)
        db.session.add(novo_admin)
        db.session.commit()

        return redirect(url_for('login_admin'))  # Redireciona para a página de login do admin

    return render_template('cadastro_admin.html')


# Cadastro de Clientes
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'], method='pbkdf2:sha256')  # Mudança aqui
        novo_cliente = Cliente(nome=nome, telefone=telefone, email=email, senha=senha)
        db.session.add(novo_cliente)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('cadastro.html')


# Login de Administrador
@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        # Verifica se o usuário é um administrador
        administrador = Administrador.query.filter_by(username=username).first()

        # Verifica se o administrador existe e a senha está correta
        if administrador and check_password_hash(administrador.senha, senha):
            login_user(administrador)
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard do admin

        flash("Credenciais inválidas. Tente novamente.", "danger")

    return render_template('login_admin.html')


# Login de Usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verifica se o usuário é um cliente
        cliente = Cliente.query.filter_by(email=email).first()

        # Verifica se o cliente existe e a senha está correta
        if cliente and check_password_hash(cliente.senha, senha):
            login_user(cliente)
            return redirect(url_for('agendamento'))  # Redireciona o cliente para a página de agendamento

    return render_template('login.html')


# Agendamento dos Clientes
@app.route('/agendamento', methods=['GET', 'POST'])
@login_required
def agendamento():
    if request.method == 'POST':
        data = request.form['data']
        hora = request.form['hora']

        novo_agendamento = Agendamento(cliente_id=current_user.id, data=data, hora=hora)
        db.session.add(novo_agendamento)
        db.session.commit()

        return redirect(url_for('agendamento'))

    return render_template('agendamento.html')


# Dashboard para Administradores
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # if isinstance(current_user, Administrador):
    # Busca todos os agendamentos e seus respectivos clientes
    agendamentos = Agendamento.query.all()

    # Exibe a dashboard com os agendamentos
    return render_template('dashboard.html', agendamentos=agendamentos)


# Caso o usuário não seja administrador, redireciona para a página inicial
#  return redirect(url_for('index'))

# Se necessário o Administrador poderá excluir um agendamento
@app.route('/excluir_agendamento/<int:id>', methods=['GET'])
@login_required
def excluir_agendamento(id):
    # if isinstance(current_user, Administrador):
    agendamento = Agendamento.query.get_or_404(id)
    db.session.delete(agendamento)
    db.session.commit()

    flash('Agendamento excluído com sucesso!', 'success')
    return redirect(url_for('dashboard'))


# return redirect(url_for('index'))

# Logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

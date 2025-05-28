from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

# Inicializando o aplicativo Flask
app = Flask(__name__)

# Configurando o banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
app.config['SECRET_KEY'] = 'mysecretkey'  # Para gerenciar sessões de login

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Definir a página de login


# Definindo o modelo de dados para tarefas
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    prazo = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pendente')
    categoria = db.Column(db.String(50))
    data_criacao = db.Column(db.Date, nullable=False)


# Definindo o modelo de dados para o usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        """Define a senha, armazenando o hash"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha informada corresponde ao hash armazenado"""
        return check_password_hash(self.password, password)


# Criar as tabelas no banco de dados (executar uma vez)
with app.app_context():
    db.create_all()


# Carregar o usuário (Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):  # Usando o método de verificação
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Login Inválido! Tente novamente.", 'danger')

    return render_template('login.html')


# Rota para logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# Rota para cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']

        # Verificando se as senhas coincidem
        if password != password_confirmation:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('register'))

        # Verificando se o nome de usuário já existe
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Nome de usuário já existe!', 'danger')
            return redirect(url_for('register'))

        # Criando novo usuário
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Rota inicial (com login obrigatório)
@app.route('/', methods=['GET'])
@login_required  # Certificando-se de que o usuário está logado
def index():
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    prazo_filter = request.args.get('prazo', '')
    page = request.args.get('page', 1, type=int)  # Captura a página atual
    per_page = 5  # Número de tarefas por página

    query = Task.query.filter(Task.status != 'concluída')

    if search:
        query = query.filter((Task.titulo.contains(search)) | (Task.categoria.contains(search)))

    if status_filter:
        query = query.filter(Task.status == status_filter)

    if prazo_filter:
        if prazo_filter == 'atrasada':
            query = query.filter(Task.prazo < datetime.now().date())  # Tarefas com prazo anterior a hoje
        elif prazo_filter == 'vencendo':
            query = query.filter(Task.prazo <= (datetime.now().date() + timedelta(days=7)))  # Tarefas vencendo em 7 dias

    tarefas = query.paginate(page=page, per_page=per_page, error_out=False)

    notificacoes = []
    for tarefa in tarefas.items:
        if tarefa.prazo - datetime.now().date() <= timedelta(days=2) and tarefa.status != 'concluída':
            notificacoes.append(tarefa)

    return render_template('index.html', tarefas=tarefas, notificacoes=notificacoes)


# Rota para adicionar uma nova tarefa
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        prazo = datetime.strptime(request.form['prazo'], '%Y-%m-%d')
        categoria = request.form['categoria']
        nova_tarefa = Task(titulo=titulo, descricao=descricao, prazo=prazo, categoria=categoria,
                           data_criacao=datetime.now())
        db.session.add(nova_tarefa)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_task.html')


# Rota para editar uma tarefa
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    tarefa = Task.query.get(id)
    if request.method == 'POST':
        tarefa.titulo = request.form['titulo']
        tarefa.descricao = request.form['descricao']
        tarefa.prazo = datetime.strptime(request.form['prazo'], '%Y-%m-%d')
        tarefa.categoria = request.form['categoria']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_task.html', tarefa=tarefa)


# Rota para concluir uma tarefa
@app.route('/concluir/<int:id>')
@login_required
def concluir_task(id):
    tarefa = Task.query.get(id)
    tarefa.status = 'concluída'  # Alterando o status para "concluída"
    db.session.commit()  # Salvando a alteração no banco de dados
    return redirect(url_for('index'))  # Redirecionando para a página inicial


# Rota para deletar uma tarefa
@app.route('/deletar/<int:id>')
@login_required
def deletar_task(id):
    tarefa = Task.query.get(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

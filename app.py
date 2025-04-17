from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sua_senha'
app.config['MYSQL_DB'] = 'sistema'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuario")
    usuarios = cur.fetchall()
    return render_template('index.html', usuarios=usuarios)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        mysql.connection.commit()
        return redirect('/')
    return render_template('create.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cur.execute("UPDATE usuario SET nome=%s, email=%s, senha=%s WHERE id=%s", (nome, email, senha, id))
        mysql.connection.commit()
        return redirect('/')
    cur.execute("SELECT * FROM usuario WHERE id=%s", [id])
    usuario = cur.fetchone()
    return render_template('update.html', usuario=usuario)


@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuario WHERE id=%s", [id])
    mysql.connection.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

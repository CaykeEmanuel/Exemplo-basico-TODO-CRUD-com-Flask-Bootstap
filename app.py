from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nota = db.Column(db.String(40), nullable=False)
    descr = db.Column(db.String(400), nullable=True)
    topico = db.Column(db.String(9), nullable=False)
    prazo = db.Column(db.String(20), nullable=False)
    data_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        nota = request.form['nota']
        descr = request.form['descr']
        topico = request.form['topico']
        prazo = request.form['prazo']
        nova_nota = Todo(nota=nota, descr=descr, topico=topico, prazo=prazo)
        try:
            db.session.add(nova_nota)
            db.session.commit()
            return redirect('/')
        except:
            return 'erro'

    else:
        banco = Todo.query.order_by(Todo.data_pub).all()
        return render_template('index.html',banco=banco)
    


if __name__ == "__main__":
    app.run(debug=True)

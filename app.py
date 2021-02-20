from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text
import datetime

app = Flask(__name__)

engine = create_engine("postgresql+psycopg2://postgres:maruto35170@/utilities", pool_size=10, max_overflow=20)

@app.route("/")
def index():
    banco = engine.execute(text("SELECT * FROM Todo_list;"))
    return render_template("index.html", banco=banco)

@app.route("/adding", methods=["POST"])
def adding():
    nota = request.form.get("nota")
    descr = request.form.get("descr")
    topico = request.form.get("topico")
    prazo = request.form.get("prazo")
    status = "Pendente"
    data_registro = datetime.datetime.now()
    engine.execute(text("INSERT INTO Todo_list (nota, descr, topico, prazo, data_registro, status) VALUES (:n, :d, :t, :p, :dt, :s);"), {'n':nota, 'd':descr, 't':topico, 'p':prazo, 'dt':data_registro,'s':status})
    banco = engine.execute(text("SELECT * FROM Todo_list;"))
    return render_template("index.html", banco=banco)


@app.route("/detalhes/<nota>")
def detalhes(nota):
    banco = engine.execute(text("SELECT * FROM Todo_list WHERE nota=:n;"), {'n':nota}).fetchall()
    return render_template('detalhes.html', banco=banco)

@app.route("/delete/<int:id>")
def delete(id):
    engine.execute(text("DELETE FROM Todo_list WHERE id=:n;"), {'n':id})
    banco = engine.execute(text("SELECT * FROM Todo_list;"))
    return render_template('index.html', banco=banco)


app.run(debug=True)
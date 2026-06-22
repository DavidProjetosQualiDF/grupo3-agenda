# # SCRIPT SUGERIDO COPILOT 2

from flask import Flask, render_template, request, redirect, url_for
import banco  # importa todas as funções de banco.py

app = Flask(__name__)

# ---------------- INDEX ----------------


@app.route("/")
def index():
    consultas_hoje = banco.listar_consultas()
    total_pacientes = len(banco.listar_pacientes())
    total_medicos = len(banco.listar_medicos())
    return render_template("index.html",
                           total_pacientes=total_pacientes,
                           total_medicos=total_medicos,
                           consultas_hoje=consultas_hoje,
                           hoje="Hoje")

# ---------------- PACIENTES ----------------


@app.route("/pacientes")
def pacientes():
    pacientes = banco.listar_pacientes()
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/cadastrar_paciente", methods=["GET", "POST"])
def cadastrar_paciente():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        banco.inserir_paciente(nome, telefone)
        return redirect(url_for("pacientes"))
    return render_template("cadastrar_paciente.html")

@app.route("/editar_paciente/<int:id>", methods=["GET", "POST"])
def editar_paciente(id):
    paciente = banco.buscar_paciente(id)
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        banco.atualizar_paciente(id, nome, telefone)
        return redirect(url_for("pacientes"))
    return render_template("editar_paciente.html", paciente=paciente)

@app.route("/deletar_paciente/<int:id>", methods=["GET", "POST"])
def deletar_paciente(id):
    paciente = banco.buscar_paciente(id)
    if request.method == "POST":
        banco.deletar_paciente(id)
        return redirect(url_for("pacientes"))
    return render_template("deletar_paciente.html", paciente=paciente)


# ---------------- MÉDICOS ----------------


@app.route("/medicos")
def medicos():
    medicos = banco.listar_medicos()
    return render_template("medicos.html", medicos=medicos)

@app.route("/cadastrar_medico", methods=["GET", "POST"])
def cadastrar_medico():
    if request.method == "POST":
        nome = request.form["nome"]
        especialidade = request.form["especialidade"]
        banco.inserir_medico(nome, especialidade)
        return redirect(url_for("medicos"))
    return render_template("cadastrar_medico.html")

@app.route("/editar_medico/<int:id>", methods=["GET", "POST"])
def editar_medico(id):
    medico = banco.buscar_medico(id)
    if request.method == "POST":
        nome = request.form["nome"]
        especialidade = request.form["especialidade"]
        banco.atualizar_medico(id, nome, especialidade)
        return redirect(url_for("medicos"))
    return render_template("editar_medico.html", medico=medico)

@app.route("/deletar_medico/<int:id>", methods=["GET", "POST"])
def deletar_medico(id):
    medico = banco.buscar_medico(id)
    if request.method == "POST":
        banco.deletar_medico(id)
        return redirect(url_for("medicos"))
    return render_template("deletar_medico.html", medico=medico)


# ---------------- CONSULTAS ----------------


@app.route("/consultas")
def consultas():
    consultas = banco.listar_consultas()
    return render_template("consultas.html", consultas=consultas)

@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    pacientes = banco.listar_pacientes()
    medicos = banco.listar_medicos()
    if request.method == "POST":
        paciente_id = request.form["paciente"]
        medico_id = request.form["medico"]
        data = request.form["data"]
        horario = request.form["hora"]
        banco.inserir_consulta(paciente_id, medico_id, data, horario)
        return redirect(url_for("consultas"))
    return render_template("agendar.html", pacientes=pacientes, medicos=medicos)

@app.route("/editar_consulta/<int:id>", methods=["GET", "POST"])
def editar_consulta(id):
    consulta = banco.buscar_consulta(id)
    pacientes = banco.listar_pacientes()
    medicos = banco.listar_medicos()
    if request.method == "POST":
        paciente_id = request.form["paciente"]
        medico_id = request.form["medico"]
        data = request.form["data"]
        horario = request.form["hora"]
        banco.atualizar_consulta(id, paciente_id, medico_id, data, horario)
        return redirect(url_for("consultas"))
    return render_template("editar_consulta.html", consulta=consulta,
                           pacientes=pacientes, medicos=medicos)

@app.route("/deletar_consulta/<int:id>", methods=["GET", "POST"])
def deletar_consulta(id):
    consulta = banco.buscar_consulta(id)
    if request.method == "POST":
        banco.deletar_consulta(id)
        return redirect(url_for("consultas"))
    return render_template("deletar_consulta.html", consulta=consulta)



# ---------------- MAIN ----------------
if __name__ == "__main__":
    banco.criar_tabelas()
    app.run(debug=True)


# # SCRIPT SUGERIDO COPILOT 1

# from flask import Flask, render_template, request, redirect, url_for
# import sqlite3
# from datetime import date

# app = Flask(__name__)

# # --- Função para inicializar o banco ---
# def init_db():
#     conn = sqlite3.connect("agenda.db")
#     cursor = conn.cursor()

#     # Pacientes
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS pacientes (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome TEXT NOT NULL,
#             idade INTEGER,
#             cpf TEXT UNIQUE,
#             telefone TEXT
#         )
#     """)

#     # Médicos
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS medicos (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome TEXT NOT NULL,
#             especialidade TEXT,
#             crm TEXT UNIQUE
#         )
#     """)

#     # Consultas
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS consultas (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             data TEXT NOT NULL,
#             hora TEXT NOT NULL,
#             paciente_id INTEGER,
#             medico_id INTEGER,
#             FOREIGN KEY(paciente_id) REFERENCES pacientes(id),
#             FOREIGN KEY(medico_id) REFERENCES medicos(id)
#         )
#     """)

#     conn.commit()
#     conn.close()

# # --- Rotas principais ---
# @app.route("/")
# def index():
#     conn = sqlite3.connect("agenda.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT COUNT(*) FROM pacientes")
#     total_pacientes = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM medicos")
#     total_medicos = cursor.fetchone()[0]

#     hoje = date.today().strftime("%d/%m/%Y")
#     cursor.execute("""
#         SELECT hora, p.nome, m.nome, m.especialidade
#         FROM consultas c
#         JOIN pacientes p ON c.paciente_id = p.id
#         JOIN medicos m ON c.medico_id = m.id
#         WHERE c.data = ?
#     """, (date.today().isoformat(),))
#     consultas_hoje = cursor.fetchall()

#     conn.close()
#     return render_template("index.html",
#                            total_pacientes=total_pacientes,
#                            total_medicos=total_medicos,
#                            consultas_hoje=consultas_hoje,
#                            hoje=hoje)

# # --- Pacientes ---
# @app.route("/pacientes")
# def pacientes():
#     conn = sqlite3.connect("agenda.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM pacientes")
#     pacientes = cursor.fetchall()
#     conn.close()
#     return render_template("pacientes.html", pacientes=pacientes)

# @app.route("/cadastrar_paciente", methods=["GET", "POST"])
# def cadastrar_paciente():
#     if request.method == "POST":
#         nome = request.form["nome"]
#         idade = request.form["idade"]
#         cpf = request.form["cpf"]
#         telefone = request.form["telefone"]

#         conn = sqlite3.connect("agenda.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO pacientes (nome, idade, cpf, telefone) VALUES (?, ?, ?, ?)",
#                        (nome, idade, cpf, telefone))
#         conn.commit()
#         conn.close()
#         return redirect(url_for("pacientes"))
#     return render_template("cadastrar_paciente.html")

# @app.route("/editar_paciente/<int:id>", methods=["GET", "POST"])
# def editar_paciente(id):
#     conn = sqlite3.connect("agenda.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM pacientes WHERE id=?", (id,))
#     paciente = cursor.fetchone()

#     if request.method == "POST":
#         nome = request.form["nome"]
#         idade = request.form["idade"]
#         cpf = request.form["cpf"]
#         telefone = request.form["telefone"]

#         cursor.execute("UPDATE pacientes SET nome=?, idade=?, cpf=?, telefone=? WHERE id=?",
#                        (nome, idade, cpf, telefone, id))
#         conn.commit()
#         conn.close()
#         return redirect(url_for("pacientes"))

#     conn.close()
#     return render_template("editar.html", paciente=paciente)

# @app.route("/deletar_paciente/<int:id>", methods=["GET", "POST"])
# def deletar_paciente(id):
#     conn = sqlite3.connect("agenda.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM pacientes WHERE id=?", (id,))
#     paciente = cursor.fetchone()

#     if request.method == "POST":
#         cursor.execute("DELETE FROM pacientes WHERE id=?", (id,))
#         conn.commit()
#         conn.close()
#         return redirect(url_for("pacientes"))

#     conn.close()
#     return render_template("deletar.html", paciente=paciente)

# # --- Médicos ---
# @app.route("/medicos")
# def medicos():
#     conn = sqlite3.connect("agenda.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM medicos")
#     medicos = cursor.fetchall()
#     conn.close()
#     return render_template("medicos.html", medicos=medicos)

# @app.route("/cadastrar_medico", methods=["GET", "POST"])
# def cadastrar_medico():
#     if request.method == "POST":
#         nome = request.form["nome"]
#         especialidade = request.form["especialidade"]
#         crm = request.form["crm"]

#         conn = sqlite3.connect("agenda.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO medicos (nome, especialidade, crm) VALUES (?, ?, ?)",
#                        (nome, especialidade, crm))
#         conn.commit()
#         conn.close()
#         return redirect(url_for("medicos"))
#     return render_template("cadastrar_medico.html")

# # --- Consultas ---
# @app.route("/consultas")
# def consultas():
#     conn = sqlite3.connect("agenda.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT c.id, c.data, c.hora, p.nome, m.nome, m.especialidade
#         FROM consultas c
#         JOIN pacientes p ON c.paciente_id = p.id
#         JOIN medicos m ON c.medico_id = m.id
#     """)
#     consultas = cursor.fetchall()
#     conn.close()
#     return render_template("consultas.html", consultas=consultas)

# @app.route("/agendar", methods=["GET", "POST"])
# def agendar():
#     conn = sqlite3.connect("agenda.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM pacientes")
#     pacientes = cursor.fetchall()
#     cursor.execute("SELECT * FROM medicos")
#     medicos = cursor.fetchall()

#     if request.method == "POST":
#         data = request.form["data"]
#         hora = request.form["hora"]
#         paciente_id = request.form["paciente"]
#         medico_id = request.form["medico"]

#         cursor.execute("INSERT INTO consultas (data, hora, paciente_id, medico_id) VALUES (?, ?, ?, ?)",
#                        (data, hora, paciente_id, medico_id))
#         conn.commit()
#         conn.close()
#         return redirect(url_for("consultas"))

#     conn.close()
#     return render_template("agendar.html", pacientes=pacientes, medicos=medicos)

# # --- Inicialização ---
# if __name__ == "__main__":
#     init_db()
#     app.run(debug=True)


# old SCRIPT 1


# from flask import Flask, render_template, request, redirect
# from banco import conectar, criar_tabelas


# app = Flask(__name__)
# criar_tabelas()

# # Cole aqui todas as rotas dos passos acima

# # ── Rota 1: Página inicial ───────────────────────────────────────────────


# @app.route("/")
# def index():
#     from datetime import date
#     hoje = str(date.today())

#     con = conectar()
#     cur = con.cursor()

#     total_pacientes = cur.execute(
#         "SELECT COUNT(*) FROM pacientes").fetchone()[0]
#     total_medicos = cur.execute("SELECT COUNT(*) FROM medicos").fetchone()[0]

#     # Consultas de hoje que não foram canceladas
#     consultas_hoje = cur.execute("""
#         SELECT c.horario, p.nome, m.nome, m.especialidade
#         FROM consultas c
#         JOIN pacientes p ON c.paciente_id = p.id
#         JOIN medicos   m ON c.medico_id   = m.id
#         WHERE c.data = ? AND c.cancelada = 0
#         ORDER BY c.horario
#     """, (hoje,)).fetchall()

#     con.close()
#     return render_template("index.html",
#                            total_pacientes=total_pacientes,
#                            total_medicos=total_medicos,
#                            consultas_hoje=consultas_hoje,
#                            hoje=hoje
#                            )


# # verficar esta parte

# # OLd script


# # @app.route("/pacientes")
# # def listar_pacientes():
# #     con = conectar()
# #     cur = con.cursor()
# #     pacientes = cur.execute("SELECT * FROM pacientes ORDER BY nome").fetchall()
# #     con.close()
# #     return render_template("pacientes.html", pacientes=pacientes)


# # @app.route("/cadastrar-paciente", methods=["GET", "POST"])
# # def cadastrar_paciente():
# #     if request.method == "POST":
# #         nome = request.form["nome"]
# #         telefone = request.form["telefone"]

# #         con = conectar()
# #         cur = con.cursor()
# #         cur.execute(
# #             "INSERT INTO pacientes (nome, telefone) VALUES (?, ?)",
# #             (nome, telefone)
# #         )
# #         con.commit()
# #         con.close()
# #         return redirect("/pacientes")

# #     return render_template("cadastrar_paciente.html")


# # --- Pacientes - SUGERIDO PELO COPILOT--
# @app.route("/pacientes")
# def pacientes():
#     conn = sqlite3.connect("agenda.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM pacientes")
#     pacientes = cursor.fetchall()
#     conn.close()
#     return render_template("pacientes.html", pacientes=pacientes)


# @app.route("/cadastrar_paciente", methods=["GET", "POST"])
# def cadastrar_paciente():
#     if request.method == "POST":
#         nome = request.form["nome"]
#         idade = request.form["idade"]
#         cpf = request.form["cpf"]
#         telefone = request.form["telefone"]

#         conn = sqlite3.connect("agenda.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO pacientes (nome, idade, cpf, telefone) VALUES (?, ?, ?, ?)",
#                        (nome, idade, cpf, telefone))
#         conn.commit()
#         conn.close()
#         return redirect(url_for("pacientes"))
#     return render_template("cadastrar_paciente.html")


# @app.route("/editar_paciente/<int:id>", methods=["GET", "POST"])
# def editar_paciente(id):
#     conn = sqlite3.connect("agenda.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM pacientes WHERE id=?", (id,))
#     paciente = cursor.fetchone()

#     if request.method == "POST":
#         nome = request.form["nome"]
#         idade = request.form["idade"]
#         cpf = request.form["cpf"]
#         telefone = request.form["telefone"]

#         cursor.execute("UPDATE pacientes SET nome=?, idade=?, cpf=?, telefone=? WHERE id=?",
#                        (nome, idade, cpf, telefone, id))
#         conn.commit()
#         conn.close()
#         return redirect(url_for("pacientes"))

#     conn.close()
#     return render_template("editar.html", paciente=paciente)


# @app.route("/deletar_paciente/<int:id>", methods=["GET", "POST"])
# def deletar_paciente(id):
#     conn = sqlite3.connect("agenda.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM pacientes WHERE id=?", (id,))
#     paciente = cursor.fetchone()

#     if request.method == "POST":
#         cursor.execute("DELETE FROM pacientes WHERE id=?", (id,))
#         conn.commit()
#         conn.close()
#         return redirect(url_for("pacientes"))

#     conn.close()
#     return render_template("deletar.html", paciente=paciente)


# @app.route("/medicos")
# def listar_medicos():
#     con = conectar()
#     cur = con.cursor()
#     medicos = cur.execute(
#         "SELECT * FROM medicos ORDER BY especialidade, nome").fetchall()
#     con.close()
#     return render_template("medicos.html", medicos=medicos)


# @app.route("/cadastrar-medico", methods=["GET", "POST"])
# def cadastrar_medico():
#     if request.method == "POST":
#         nome = request.form["nome"]
#         especialidade = request.form["especialidade"]

#         con = conectar()
#         cur = con.cursor()
#         cur.execute(
#             "INSERT INTO medicos (nome, especialidade) VALUES (?, ?)",
#             (nome, especialidade)
#         )
#         con.commit()
#         con.close()
#         return redirect("/medicos")

#     return render_template("cadastrar_medico.html")


# @app.route("/agendar", methods=["GET", "POST"])
# def agendar():
#     if request.method == "POST":
#         paciente_id = int(request.form["paciente_id"])
#         medico_id = int(request.form["medico_id"])
#         data = request.form["data"]
#         horario = request.form["horario"]

#         con = conectar()
#         cur = con.cursor()

#         # Verifica se o médico já tem consulta nesse horário
#         conflito = cur.execute("""
#             SELECT id FROM consultas
#             WHERE medico_id = ? AND data = ? AND horario = ? AND cancelada = 0
#         """, (medico_id, data, horario)).fetchone()

#         if conflito:
#             pacientes = cur.execute(
#                 "SELECT id, nome FROM pacientes ORDER BY nome").fetchall()
#             medicos = cur.execute(
#                 "SELECT id, nome, especialidade FROM medicos ORDER BY nome").fetchall()
#             con.close()
#             return render_template("agendar.html",
#                                    pacientes=pacientes, medicos=medicos,
#                                    erro="Este médico já tem uma consulta neste horário!"
#                                    )

#         cur.execute(
#             "INSERT INTO consultas (paciente_id, medico_id, data, horario) VALUES (?, ?, ?, ?)",
#             (paciente_id, medico_id, data, horario)
#         )
#         con.commit()
#         con.close()
#         return redirect("/consultas")

#     con = conectar()
#     cur = con.cursor()
#     pacientes = cur.execute(
#         "SELECT id, nome FROM pacientes ORDER BY nome").fetchall()
#     medicos = cur.execute(
#         "SELECT id, nome, especialidade FROM medicos ORDER BY nome").fetchall()
#     con.close()
#     return render_template("agendar.html", pacientes=pacientes, medicos=medicos, erro=None)


# @app.route("/consultas")
# def listar_consultas():
#     con = conectar()
#     cur = con.cursor()
#     consultas = cur.execute("""
#         SELECT c.id, p.nome, m.nome, m.especialidade, c.data, c.horario
#         FROM consultas c
#         JOIN pacientes p ON c.paciente_id = p.id
#         JOIN medicos   m ON c.medico_id   = m.id
#         WHERE c.cancelada = 0
#         ORDER BY c.data, c.horario
#     """).fetchall()
#     con.close()
#     return render_template("consultas.html", consultas=consultas)


# @app.route("/cancelar/<int:cons_id>", methods=["POST"])
# def cancelar(cons_id):
#     con = conectar()
#     cur = con.cursor()
#     cur.execute(
#         "UPDATE consultas SET cancelada = 1 WHERE id = ?", (cons_id,)
#     )
#     con.commit()
#     con.close()
#     return redirect("/consultas")


# if __name__ == "__main__":
#     app.run(debug=True)

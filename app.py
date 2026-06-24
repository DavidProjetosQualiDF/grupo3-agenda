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
        idade = request.form["idade"]
        cpf = request.form["cpf"]
        telefone = request.form["telefone"]

        banco.inserir_paciente(
            nome,
            idade,
            cpf,
            telefone
        )

        return redirect(url_for("pacientes"))

    return render_template("cadastrar_paciente.html")
        
    # return render_template("cadastrar_paciente.html")

@app.route("/editar_paciente/<int:id>", methods=["GET", "POST"])
def editar_paciente(id):
    paciente = banco.buscar_paciente(id)
    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        cpf= request.form["cpf"]
        telefone = request.form["telefone"]

        banco.atualizar_paciente(id, nome, telefone, idade, cpf)
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



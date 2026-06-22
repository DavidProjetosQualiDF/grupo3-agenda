# SCRIPT DO COPILOT

import sqlite3

DB_NAME = "agenda.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    # Pacientes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nome     TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
    """)

    # Médicos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicos (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            nome          TEXT NOT NULL,
            especialidade TEXT NOT NULL
        )
    """)

    # Consultas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            medico_id   INTEGER NOT NULL,
            data        TEXT    NOT NULL,
            horario     TEXT    NOT NULL,
            cancelada   INTEGER DEFAULT 0,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
            FOREIGN KEY (medico_id)   REFERENCES medicos(id)
        )
    """)

    con.commit()
    con.close()

# ---------------- PACIENTES ----------------
def listar_pacientes():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM pacientes")
    dados = cur.fetchall()
    con.close()
    return dados

def inserir_paciente(nome, telefone):
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO pacientes (nome, telefone) VALUES (?, ?)", (nome, telefone))
    con.commit()
    con.close()

def buscar_paciente(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM pacientes WHERE id=?", (id,))
    dado = cur.fetchone()
    con.close()
    return dado

def atualizar_paciente(id, nome, telefone):
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE pacientes SET nome=?, telefone=? WHERE id=?", (nome, telefone, id))
    con.commit()
    con.close()

def deletar_paciente(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM pacientes WHERE id=?", (id,))
    con.commit()
    con.close()

# ---------------- MÉDICOS ----------------
def listar_medicos():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM medicos")
    dados = cur.fetchall()
    con.close()
    return dados

def inserir_medico(nome, especialidade):
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO medicos (nome, especialidade) VALUES (?, ?)", (nome, especialidade))
    con.commit()
    con.close()

def buscar_medico(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM medicos WHERE id=?", (id,))
    dado = cur.fetchone()
    con.close()
    return dado

def atualizar_medico(id, nome, especialidade):
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE medicos SET nome=?, especialidade=? WHERE id=?", (nome, especialidade, id))
    con.commit()
    con.close()

def deletar_medico(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM medicos WHERE id=?", (id,))
    con.commit()
    con.close()

# ---------------- CONSULTAS ----------------
def listar_consultas():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        SELECT c.id, c.paciente_id, c.medico_id, c.data, c.horario,
               p.nome, m.nome, m.especialidade
        FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        JOIN medicos m ON c.medico_id = m.id
        WHERE c.cancelada = 0
    """)
    dados = cur.fetchall()
    con.close()
    return dados

def inserir_consulta(paciente_id, medico_id, data, horario):
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO consultas (paciente_id, medico_id, data, horario) VALUES (?, ?, ?, ?)",
                (paciente_id, medico_id, data, horario))
    con.commit()
    con.close()

def buscar_consulta(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM consultas WHERE id=?", (id,))
    dado = cur.fetchone()
    con.close()
    return dado

def atualizar_consulta(id, paciente_id, medico_id, data, horario):
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE consultas SET paciente_id=?, medico_id=?, data=?, horario=? WHERE id=?",
                (paciente_id, medico_id, data, horario, id))
    con.commit()
    con.close()

def deletar_consulta(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM consultas WHERE id=?", (id,))
    con.commit()
    con.close()



# OLD SCRIPT
# import sqlite3

# def conectar():
#     return sqlite3.connect("agenda.db")

# def criar_tabelas():
#     con = conectar()
#     cur = con.cursor()

#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS pacientes (
#             id       INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome     TEXT NOT NULL,
#             telefone TEXT NOT NULL
#         )
#     """)

#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS medicos (
#             id            INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome          TEXT NOT NULL,
#             especialidade TEXT NOT NULL
#         )
#     """)

#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS consultas (
#             id          INTEGER PRIMARY KEY AUTOINCREMENT,
#             paciente_id INTEGER NOT NULL,
#             medico_id   INTEGER NOT NULL,
#             data        TEXT    NOT NULL,
#             horario     TEXT    NOT NULL,
#             cancelada   INTEGER DEFAULT 0,
#             FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
#             FOREIGN KEY (medico_id)   REFERENCES medicos(id)
#         )
#     """)

#     con.commit()
#     con.close()
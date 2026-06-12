# 🗓️ Agenda de Consultas — Grupo 3

> **Projeto Final · Qualifica DF · Programador de Sistemas · 2026**

Sistema web para gerenciar pacientes, médicos e consultas agendadas.
Desenvolvido com **Python + Flask + SQLite + HTML/CSS**.

---

## 🎯 Objetivo

Criar uma aplicação web funcional que permita:
- Cadastrar pacientes e médicos
- Agendar consultas vinculando paciente + médico + data
- Cancelar agendamentos
- Listar as consultas do dia e todos os agendamentos ativos

---

## 🗂️ Estrutura de pastas

```
grupo3-agenda/
│
├── app.py                      ← arquivo principal Flask
├── banco.py                    ← funções do banco de dados
├── requirements.txt            ← dependências do projeto
│
├── templates/
│   ├── base.html               ← layout base (navbar, estilo)
│   ├── index.html              ← página inicial com resumo
│   ├── pacientes.html          ← lista de pacientes
│   ├── cadastrar_paciente.html
│   ├── medicos.html            ← lista de médicos
│   ├── cadastrar_medico.html
│   ├── consultas.html          ← todos os agendamentos ativos
│   └── agendar.html            ← formulário de agendamento
│
└── static/
    └── style.css               ← estilos da aplicação
```

---

## 🗃️ Banco de Dados

### Tabelas

#### `pacientes`
| Coluna     | Tipo    | Descrição                        |
|------------|---------|----------------------------------|
| `id`       | INTEGER | Chave primária (auto incremento) |
| `nome`     | TEXT    | Nome completo do paciente        |
| `telefone` | TEXT    | Telefone de contato              |

#### `medicos`
| Coluna         | Tipo    | Descrição                        |
|----------------|---------|----------------------------------|
| `id`           | INTEGER | Chave primária (auto incremento) |
| `nome`         | TEXT    | Nome do médico                   |
| `especialidade`| TEXT    | Especialidade médica             |

#### `consultas`
| Coluna        | Tipo    | Descrição                          |
|---------------|---------|------------------------------------|
| `id`          | INTEGER | Chave primária (auto incremento)   |
| `paciente_id` | INTEGER | Referência ao paciente             |
| `medico_id`   | INTEGER | Referência ao médico               |
| `data`        | TEXT    | Data da consulta (YYYY-MM-DD)      |
| `horario`     | TEXT    | Horário da consulta (ex: 14:30)    |
| `cancelada`   | INTEGER | 0 = ativa · 1 = cancelada         |

### Código do banco (`banco.py`)

```python
import sqlite3

def conectar():
    return sqlite3.connect("agenda.db")

def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nome     TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicos (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            nome          TEXT NOT NULL,
            especialidade TEXT NOT NULL
        )
    """)

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
```

---

## 🚀 Rotas da aplicação

### Passo 1 — Página inicial

**Rota:** `GET /`

Exibe resumo: total de pacientes, médicos, consultas do dia e próximas consultas.

```python
@app.route("/")
def index():
    from datetime import date
    hoje = str(date.today())

    con = conectar()
    cur = con.cursor()

    total_pacientes = cur.execute("SELECT COUNT(*) FROM pacientes").fetchone()[0]
    total_medicos   = cur.execute("SELECT COUNT(*) FROM medicos").fetchone()[0]

    # Consultas de hoje que não foram canceladas
    consultas_hoje = cur.execute("""
        SELECT c.horario, p.nome, m.nome, m.especialidade
        FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        JOIN medicos   m ON c.medico_id   = m.id
        WHERE c.data = ? AND c.cancelada = 0
        ORDER BY c.horario
    """, (hoje,)).fetchall()

    con.close()
    return render_template("index.html",
        total_pacientes=total_pacientes,
        total_medicos=total_medicos,
        consultas_hoje=consultas_hoje,
        hoje=hoje
    )
```

**Template `index.html`:**
```html
{% extends "base.html" %}
{% block conteudo %}
  <h1>🗓️ Agenda de Consultas</h1>
  <div class="cards">
    <div class="card">
      <h2>{{ total_pacientes }}</h2><p>Pacientes</p>
    </div>
    <div class="card">
      <h2>{{ total_medicos }}</h2><p>Médicos</p>
    </div>
    <div class="card">
      <h2>{{ consultas_hoje|length }}</h2><p>Consultas hoje</p>
    </div>
  </div>

  <h2>📅 Consultas de hoje ({{ hoje }})</h2>
  {% if consultas_hoje %}
    <table>
      <thead>
        <tr><th>Horário</th><th>Paciente</th><th>Médico</th><th>Especialidade</th></tr>
      </thead>
      <tbody>
        {% for c in consultas_hoje %}
        <tr>
          <td>{{ c[0] }}</td><td>{{ c[1] }}</td>
          <td>{{ c[2] }}</td><td>{{ c[3] }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p class="vazio">Nenhuma consulta agendada para hoje.</p>
  {% endif %}
{% endblock %}
```

---

### Passo 2 — Cadastrar e listar pacientes

**Rotas:** `GET /pacientes` | `GET /cadastrar-paciente` | `POST /cadastrar-paciente`

```python
@app.route("/pacientes")
def listar_pacientes():
    con = conectar()
    cur = con.cursor()
    pacientes = cur.execute("SELECT * FROM pacientes ORDER BY nome").fetchall()
    con.close()
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/cadastrar-paciente", methods=["GET", "POST"])
def cadastrar_paciente():
    if request.method == "POST":
        nome     = request.form["nome"]
        telefone = request.form["telefone"]

        con = conectar()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO pacientes (nome, telefone) VALUES (?, ?)",
            (nome, telefone)
        )
        con.commit()
        con.close()
        return redirect("/pacientes")

    return render_template("cadastrar_paciente.html")
```

---

### Passo 3 — Cadastrar e listar médicos

**Rotas:** `GET /medicos` | `GET /cadastrar-medico` | `POST /cadastrar-medico`

```python
@app.route("/medicos")
def listar_medicos():
    con = conectar()
    cur = con.cursor()
    medicos = cur.execute("SELECT * FROM medicos ORDER BY especialidade, nome").fetchall()
    con.close()
    return render_template("medicos.html", medicos=medicos)

@app.route("/cadastrar-medico", methods=["GET", "POST"])
def cadastrar_medico():
    if request.method == "POST":
        nome          = request.form["nome"]
        especialidade = request.form["especialidade"]

        con = conectar()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO medicos (nome, especialidade) VALUES (?, ?)",
            (nome, especialidade)
        )
        con.commit()
        con.close()
        return redirect("/medicos")

    return render_template("cadastrar_medico.html")
```

---

### Passo 4 — Agendar consulta

**Rotas:** `GET /agendar` → formulário com pacientes e médicos | `POST /agendar` → salva

```python
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if request.method == "POST":
        paciente_id = int(request.form["paciente_id"])
        medico_id   = int(request.form["medico_id"])
        data        = request.form["data"]
        horario     = request.form["horario"]

        con = conectar()
        cur = con.cursor()

        # Verifica se o médico já tem consulta nesse horário
        conflito = cur.execute("""
            SELECT id FROM consultas
            WHERE medico_id = ? AND data = ? AND horario = ? AND cancelada = 0
        """, (medico_id, data, horario)).fetchone()

        if conflito:
            pacientes = cur.execute("SELECT id, nome FROM pacientes ORDER BY nome").fetchall()
            medicos   = cur.execute("SELECT id, nome, especialidade FROM medicos ORDER BY nome").fetchall()
            con.close()
            return render_template("agendar.html",
                pacientes=pacientes, medicos=medicos,
                erro="Este médico já tem uma consulta neste horário!"
            )

        cur.execute(
            "INSERT INTO consultas (paciente_id, medico_id, data, horario) VALUES (?, ?, ?, ?)",
            (paciente_id, medico_id, data, horario)
        )
        con.commit()
        con.close()
        return redirect("/consultas")

    con = conectar()
    cur = con.cursor()
    pacientes = cur.execute("SELECT id, nome FROM pacientes ORDER BY nome").fetchall()
    medicos   = cur.execute("SELECT id, nome, especialidade FROM medicos ORDER BY nome").fetchall()
    con.close()
    return render_template("agendar.html", pacientes=pacientes, medicos=medicos, erro=None)
```

**Template `agendar.html`:**
```html
{% extends "base.html" %}
{% block conteudo %}
  <h1>📅 Agendar Consulta</h1>

  {% if erro %}
    <div class="erro">{{ erro }}</div>
  {% endif %}

  <form method="POST">
    <label>Paciente</label>
    <select name="paciente_id" required>
      {% for p in pacientes %}
        <option value="{{ p[0] }}">{{ p[1] }}</option>
      {% endfor %}
    </select>

    <label>Médico</label>
    <select name="medico_id" required>
      {% for m in medicos %}
        <option value="{{ m[0] }}">{{ m[1] }} — {{ m[2] }}</option>
      {% endfor %}
    </select>

    <label>Data</label>
    <input type="date" name="data" required>

    <label>Horário</label>
    <input type="time" name="horario" required>

    <button type="submit">Agendar</button>
  </form>
{% endblock %}
```

---

### Passo 5 — Listar consultas ativas

**Rota:** `GET /consultas`

Lista todas as consultas não canceladas usando JOIN com as três tabelas.

```python
@app.route("/consultas")
def listar_consultas():
    con = conectar()
    cur = con.cursor()
    consultas = cur.execute("""
        SELECT c.id, p.nome, m.nome, m.especialidade, c.data, c.horario
        FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        JOIN medicos   m ON c.medico_id   = m.id
        WHERE c.cancelada = 0
        ORDER BY c.data, c.horario
    """).fetchall()
    con.close()
    return render_template("consultas.html", consultas=consultas)
```

---

### Passo 6 — Cancelar consulta

**Rota:** `POST /cancelar/<int:cons_id>`

Marca a consulta como cancelada sem apagar do banco (boa prática: nunca deletar registros médicos).

```python
@app.route("/cancelar/<int:cons_id>", methods=["POST"])
def cancelar(cons_id):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE consultas SET cancelada = 1 WHERE id = ?", (cons_id,)
    )
    con.commit()
    con.close()
    return redirect("/consultas")
```

No template `consultas.html`, adicione o botão de cancelamento em cada linha:
```html
<form action="/cancelar/{{ c[0] }}" method="POST" style="display:inline">
  <button type="submit" class="btn vermelho"
    onclick="return confirm('Cancelar esta consulta?')">
    Cancelar
  </button>
</form>
```

---

## 📄 Arquivo principal (`app.py`)

```python
from flask import Flask, render_template, request, redirect
from banco import conectar, criar_tabelas

app = Flask(__name__)
criar_tabelas()

# Cole aqui todas as rotas dos passos acima

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 📦 Dependências (`requirements.txt`)

```
flask
gunicorn
```

---

## 🎨 Estilo base (`static/style.css`)

```css
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Arial, sans-serif; background: #f5f5f5; color: #333; }
nav { background: #534ab7; padding: 1rem 2rem; }
nav a { color: white; text-decoration: none; margin-right: 1.5rem; font-weight: bold; }
.container { max-width: 900px; margin: 2rem auto; padding: 0 1rem; }
h1 { margin-bottom: 1.5rem; color: #534ab7; }
h2 { margin: 1.5rem 0 1rem; color: #3c3489; }
table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }
th { background: #534ab7; color: white; padding: 0.75rem 1rem; text-align: left; }
td { padding: 0.75rem 1rem; border-bottom: 1px solid #eee; }
.btn { display: inline-block; padding: 0.5rem 1rem; background: #534ab7; color: white;
       text-decoration: none; border-radius: 6px; border: none; cursor: pointer; margin-bottom: 1rem; }
.btn.vermelho { background: #c0392b; }
.badge { padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; }
.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.card { background: white; padding: 2rem; border-radius: 8px; text-align: center; border-left: 4px solid #534ab7; }
.card h2 { font-size: 2rem; color: #534ab7; margin: 0; }
.card p { color: #666; margin-top: 0.5rem; }
form label { display: block; margin: 1rem 0 0.25rem; font-weight: bold; }
form input, form select { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; }
form button { margin-top: 1.5rem; }
.erro { background: #f8d7da; color: #721c24; padding: 0.75rem 1rem; border-radius: 4px; margin-bottom: 1rem; }
.vazio { color: #888; font-style: italic; margin: 1rem 0; }
```

---

## 🌐 Layout base (`templates/base.html`)

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Agenda de Consultas</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <nav>
    <a href="/">🏠 Início</a>
    <a href="/pacientes">👤 Pacientes</a>
    <a href="/medicos">🩺 Médicos</a>
    <a href="/consultas">📋 Consultas</a>
    <a href="/agendar">➕ Agendar</a>
  </nav>
  <div class="container">
    {% block conteudo %}{% endblock %}
  </div>
</body>
</html>
```

---

## ☁️ Deploy no Render

1. Suba o projeto no GitHub (faça fork deste repo e implemente nele)
2. Acesse [render.com](https://render.com) e crie uma conta gratuita
3. Clique em **New > Web Service** e conecte seu repositório
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Clique em **Deploy**!

---

## ✅ Checklist de entrega

- [ ] Cadastro de pacientes funcionando
- [ ] Cadastro de médicos funcionando
- [ ] Agendamento com validação de conflito de horário
- [ ] Lista de consultas do dia na página inicial
- [ ] Listagem de todas as consultas ativas com JOIN triplo
- [ ] Cancelamento atualiza o banco sem deletar o registro
- [ ] Aplicação rodando no Render com URL pública
- [ ] README atualizado com a URL do deploy

---

*Qualifica DF · 2026 · Programador de Sistemas*

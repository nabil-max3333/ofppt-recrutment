from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ofppt_secret_2026'

DB = 'candidatures.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidatures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prenom TEXT,
        nom TEXT,
        date_naissance TEXT,
        filiere TEXT,
        situation_familiale TEXT,
        telephone TEXT,
        email TEXT,
        cin TEXT,
        nom_formateur TEXT,
        bourse TEXT,
        date_soumission TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''INSERT INTO candidatures 
        (prenom, nom, date_naissance, filiere, situation_familiale, telephone, email, cin, nom_formateur, bourse, date_soumission)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (
            data.get('prenom', ''),
            data.get('nom', ''),
            data.get('date_naissance', ''),
            data.get('filiere', ''),
            data.get('situation_familiale', ''),
            data.get('telephone', ''),
            data.get('email', ''),
            data.get('cin', ''),
            data.get('nom_formateur', ''),
            data.get('bourse', ''),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/dashboard')
def dashboard():
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('SELECT * FROM candidatures ORDER BY date_soumission DESC')
        rows = c.fetchall()
        conn.close()
        return render_template('dashboard.html', candidatures=rows)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('DELETE FROM candidatures WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

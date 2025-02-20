from flask import Flask, request, render_template, redirect, url_for # type: ignore
import os
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    try:
        # Use an absolute path to ensure it’s in the correct directory
        db_path = os.path.join(os.getcwd(), 'database.db')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                date TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Banco de dados inicializado e tabela 'images' criada com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT filename, date, latitude, longitude FROM images ORDER BY date DESC')
    images = cursor.fetchall()
    conn.close()
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    if file.filename == '' or not latitude or not longitude:
        return redirect(request.url)
    
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + '_' + file.filename

    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO images (filename, date, latitude, longitude) VALUES (?, ?, ?, ?)',
                   (filename, datetime.now().isoformat(), latitude, longitude))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.before_request
def before_request():
    init_db()

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
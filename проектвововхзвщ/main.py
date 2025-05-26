from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import bcrypt
import subprocess
import datetime
import pandas as pd
import os
from matplotlib.figure import Figure
from io import BytesIO
import base64
import platform
import socket
import time
import requests
import threading
import webbrowser

app = Flask(__name__)
app.secret_key = 'supersecretsupershh'
DATABASE = 'network_diagnostics.db'

# Ensure the database exists
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            test_type TEXT NOT NULL,
            result TEXT,
            date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()

def is_logged_in():
    return 'user_id' in session

@app.route('/')
def index():
    if is_logged_in():
        return redirect(url_for('main'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Не указано имя пользователя.'
        elif not password:
            error = 'Не указан пароль.'
        elif query_db('SELECT id FROM users WHERE username = ?', [username], one=True) is not None:
            error = f'Пользователь {username} уже зарегистрирован.'

        if error is None:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            execute_db('INSERT INTO users (username, password_hash) VALUES (?, ?)', [username, hashed_password])
            flash('Успешная регистрация! Теперь вы можете войти в систему.')
            return redirect(url_for('login'))
        flash(error)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)

        if user is None:
            error = 'Пользователь не найден.'
        elif not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            error = 'Неверный пароль.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('main'))
        flash(error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/main')
def main():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('main.html')

@app.route('/check_internet')
def check_internet():
    if not is_logged_in():
        return redirect(url_for('login'))

    connected = False
    try:
        # Определяем параметры ping в зависимости от ОС
        if platform.system().lower() == 'windows':
            ping_cmd = ['ping', '-n', '1', '-w', '2000', '8.8.8.8']
        else:
            ping_cmd = ['ping', '-c', '1', '-W', '2', '8.8.8.8']
        subprocess.check_call(ping_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        connected = True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        try:
            if platform.system().lower() == 'windows':
                ping_cmd = ['ping', '-n', '1', '-w', '2000', 'google.com']
            else:
                ping_cmd = ['ping', '-c', '1', '-W', '2', 'google.com']
            subprocess.check_call(ping_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            connected = True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            connected = False

    result = "Подключено" if connected else "Нет подключения"
    execute_db('INSERT INTO tests (user_id, test_type, result) VALUES (?, ?, ?)', [session['user_id'], 'Проверка интернета', result])
    return render_template('check_internet.html', result=result)

def ping_host(host):
    try:
        # Resolve the host to an IP address
        ip = socket.gethostbyname(host)
        
        # Create a socket and measure the round-trip time
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            start_time = time.time()
            s.settimeout(1)
            s.connect((ip, 80))  # Port 80 is used for HTTP
            end_time = time.time()
            
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        return f"Пинг до {host} ({ip}): {latency:.2f} мс"
    except socket.gaierror:
        return f"Ошибка: Не удалось разрешить имя хоста {host}"
    except socket.timeout:
        return f"Ошибка: Время ожидания истекло для {host}"
    except Exception as e:
        return f"Ошибка: {e}"

@app.route('/ping', methods=['GET', 'POST'])
def ping_test():
    if not is_logged_in():
        return redirect(url_for('login'))

    results = []
    if request.method == 'POST':
        address = request.form['address']
        result = ping_host(address)
        results.append(result)
        execute_db('INSERT INTO tests (user_id, test_type, result) VALUES (?, ?, ?)', [session['user_id'], f'Пинг {address}', result])

    return render_template('ping.html', results=results)

def measure_speed():
    download_url = 'https://files.testfile.org/ZIPC/15MB-Corrupt-Testfile.Org.zip'
    upload_url = 'https://cloudcdn-kiv-02.cdn.yandex.net/cdnrphoszsa2sp7ilm7a/upload?mid=kjaoywbgjfjqgdha&rid=y38hepgiyq4qudwg'
    download_speed = None
    upload_speed = None
    error = None
    try:
        start_time = time.time()
        response = requests.get(download_url, stream=True, timeout=30, verify=False)
        total_downloaded = 0
        for chunk in response.iter_content(chunk_size=1024 * 256):
            total_downloaded += len(chunk)
        end_time = time.time()
        if total_downloaded > 0 and end_time > start_time:
            download_speed = (total_downloaded * 8 / (end_time - start_time)) / 1_000_000  # Mbps
        else:
            error = 'Ошибка при измерении скорости загрузки.'
    except Exception as e:
        error = f'Ошибка при измерении скорости загрузки: {e}'

    if not error:
        try:
            upload_data = os.urandom(5 * 1024 * 1024)  # 5 MB
            start_time = time.time()
            requests.post(upload_url, data=upload_data, timeout=30, verify=False)
            end_time = time.time()
            upload_speed = (len(upload_data) * 8 / (end_time - start_time)) / 1_000_000  # Mbps
        except Exception as e:
            error = f'Ошибка при измерении скорости отдачи: {e}'

    return download_speed, upload_speed, error

@app.route('/speedtest', methods=['GET'])
def speed_test():
    if not is_logged_in():
        return redirect(url_for('login'))

    download_speed, upload_speed, error = measure_speed()
    download = f"{download_speed:.2f} Мбит/с" if download_speed else None
    upload = f"{upload_speed:.2f} Мбит/с" if upload_speed else None
    execute_db('INSERT INTO tests (user_id, test_type, result) VALUES (?, ?, ?)', [session['user_id'], 'Измерение скорости', f'Скорость загрузки: {download or "-"}, Скорость отдачи: {upload or "-"}'])
    return render_template('speedtest.html', download=download, upload=upload, error=error)

@app.route('/history')
def history():
    if not is_logged_in():
        return redirect(url_for('login'))

    tests = query_db('SELECT test_type, result, date_time FROM tests WHERE user_id = ? ORDER BY date_time DESC', [session['user_id']])
    return render_template('history.html', tests=tests)

@app.route('/export_history')
def export_history():
    if not is_logged_in():
        return redirect(url_for('login'))

    tests_data = query_db('SELECT test_type, result, date_time FROM tests WHERE user_id = ? ORDER BY date_time DESC', [session['user_id']])
    if not tests_data:
        flash("Нет данных для экспорта.")
        return redirect(url_for('history'))

    df = pd.DataFrame([dict(row) for row in tests_data])
    filename = f"network_diagnostics_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    file_path = os.path.join(os.getcwd(), filename)

    # Save the DataFrame to an Excel file
    df.to_excel(file_path, index=False)

    # Send the file as a response
    response = app.response_class(
        open(file_path, 'rb').read(),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

    # Clean up the file after sending
    os.remove(file_path)

    return response

@app.route('/visualize')
def visualize():
    if not is_logged_in():
        return redirect(url_for('login'))

    speed_tests = query_db("SELECT result, date_time FROM tests WHERE user_id = ? AND test_type = 'Измерение скорости' ORDER BY date_time", [session['user_id']])

    if not speed_tests:
        return render_template('visualize.html', plot_url=None, error="Нет данных для визуализации скорости.")

    dates = []
    download_speeds = []
    upload_speeds = []

    for test in speed_tests:
        try:
            parts = test['result'].split(', ')
            download_str = next(p for p in parts if 'Скорость загрузки' in p).split(': ')[1].split(' ')[0]
            upload_str = next(p for p in parts if 'Скорость отдачи' in p).split(': ')[1].split(' ')[0]
            # Проверяем, что значения скоростей корректны
            if download_str.replace('.', '', 1).isdigit() and upload_str.replace('.', '', 1).isdigit():
                dates.append(datetime.datetime.strptime(test['date_time'], '%Y-%m-%d %H:%M:%S'))
                download_speeds.append(float(download_str))
                upload_speeds.append(float(upload_str))
            else:
                continue
        except Exception as e:
            print(f"Error parsing speed test result: {test['result']} - {e}")
            continue

    if not dates:
        return render_template('visualize.html', plot_url=None, error="Нет корректных данных о скорости для визуализации.")

    fig = Figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.plot(dates, download_speeds, label='Скорость загрузки (Мбит/с)')
    ax.plot(dates, upload_speeds, label='Скорость отдачи (Мбит/с)')
    ax.set_xlabel('Дата и время')
    ax.set_ylabel('Скорость (Мбит/с)')
    ax.set_title('История скорости интернет-соединения')
    ax.legend()
    ax.grid(True)
    fig.autofmt_xdate()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render_template('visualize.html', plot_url=plot_url, error=None)

from flask import g, flash

if __name__ == '__main__':
    # Автоматически открыть браузер с URL приложения
    webbrowser.open('http://127.0.0.1:5000')
    # Запуск приложения Flask без предупреждения "WARNING: This is a development server"
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
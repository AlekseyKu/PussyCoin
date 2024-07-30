from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reset', methods=['POST'])
def reset_counter():
    user_id = request.form.get('user_id')
    with sqlite3.connect('db.sqlite3') as conn:
        conn.execute('REPLACE INTO counters (user_id, counter, last_reset) VALUES (?, ?, ?)',
                     (user_id, 0, datetime.now()))
    return jsonify({'status': 'success'})


@app.route('/get_state', methods=['GET'])
def get_state():
    user_id = request.args.get('user_id')
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT counter, last_reset FROM counters WHERE user_id=?', (user_id,))
        row = cursor.fetchone()
        if row is not None:
            counter, last_reset = row
            elapsed_time = datetime.now() - last_reset
            counter += int(elapsed_time.total_seconds() / 72)
            conn.execute('UPDATE counters SET counter=? WHERE user_id=?', (counter, user_id))
            conn.commit()
            return jsonify({'counter': counter})
        else:
            return jsonify({'counter': 0})

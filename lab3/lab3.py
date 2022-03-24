from crypt import methods
import sqlite3
from flask import Flask, Response, request
import uuid

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['POST', 'DELETE', 'PUT'])
def index():
    conn = get_db_connection()
    word = request.get_json()
    newId = str(uuid.uuid4())
    key, value = word['key'], word['value']
    if request.method == 'POST':
        try:
            conn.execute('INSERT INTO table1 (id, key, value) VALUES (?, ?, ?)', (newId, key, value))
            conn.commit()
            conn.close()
            return {'word': {
                'key': word['key'],
                'value': word['value'],
            }, 'message': 'success'}, 201
        except:
            return {'error': 'Invalid JSON Body', 'status': 400}, 400
    elif request.method == 'DELETE':
        try:
            check = conn.execute('SELECT * FROM table1 WHERE key = ?', (key,)).fetchone()
            conn.execute('DELETE FROM table1 WHERE key = ?',(word['key'],))
            conn.commit()
            conn.close()
            if check is None:
                return {'error': 'Invalid key', 'status': 404}, 404
            return {'word': {
                    'key': word['key'],
                }, 'message': 'success'}, 200
        except:
            return {'error': 'Invalid JSON Body', 'status': 400}, 400
    else:
        try:
            conn.execute('UPDATE table1 SET key = ?, value = ? WHERE key = ? OR value = ?', (word['key'],word['value'],word['key'],word['value'],))
            conn.commit()
            conn.close()
            return {'word': {
                    'key': word['key'],
                    'value': word['value'],
                }, 'message': 'success'}, 201
        except:
            return {'error': 'Invalid JSON Body', 'status': 400}, 400


@app.route('/<key>/', methods=['GET'])
def ggetByKey(key):
    conn = get_db_connection()
    word = conn.execute('SELECT * FROM table1 WHERE key = ?',
                        (key,)).fetchone()
    conn.close()
    if word is None:
        return {'error': 'Invalid key', 'status': 404}, 404
    return {'word': {
                'id': word['id'],
                'key': word['key'],
                'value': word['value'],
            }}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
import sqlite3
import uuid

newId = str(uuid.uuid4())

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO table1 (id, key, value) VALUES (?, ?, ?)",
            (newId, 'the_key', 'the_value')
            )

connection.commit()
connection.close()
from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='db',
        user='user',
        password='password',
        database='mydatabase'
    )
    return connection

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT userid, username FROM users')
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(users)

@app.route('/add', methods=['POST'])
def add_user():
    username = request.json['username']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username) VALUES (%s)', (username,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'User added successfully'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

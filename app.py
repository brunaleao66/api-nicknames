from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')  # Coloque a URL de conexão do seu banco Neon aqui

# Função para conectar ao banco de dados
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Rota para buscar todos os nicknames
@app.route('/nicknames', methods=['GET'])
def get_nicknames():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nicknames;')
    nicknames = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convertendo os dados para um formato mais fácil de manipular
    return jsonify([{'id': row[0], 'nickname': row[1]} for row in nicknames])

# Rota para adicionar um novo nickname
@app.route('/nicknames', methods=['POST'])
def add_nickname():
    new_nickname = request.json.get('nickname')
    
    if not new_nickname:
        return jsonify({'error': 'No nickname provided'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO nicknames (nickname) VALUES (%s);', (new_nickname,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': f'Nickname {new_nickname} added successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)

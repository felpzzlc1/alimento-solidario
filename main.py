from flask import Flask, request, jsonify
import pymysql
import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

app = Flask(__name__)

# Banco de dados
def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

# Login
@app.route('/usuarios', methods=['GET'])
def login():
    cpf = request.args.get('cpf')
    senha = request.args.get('senha')

    if not cpf or not senha:
        return jsonify({'error': 'CPF e senha são obrigatórios'}), 400

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE cpf=%s AND senha=%s", (cpf, senha))
            result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({'message': 'CPF ou senha inválidos'}), 401

        return jsonify({'message': 'Login realizado com sucesso', 'usuario': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Cadastro
@app.route('/usuarios', methods=['POST'])
def cadastrar():
    data = request.json
    required = ['nome', 'cpf', 'data_nascimento', 'telefone', 'senha']

    if not all(k in data for k in required):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO usuarios (nome, cpf, data_nascimento, telefone, senha)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                data['nome'], data['cpf'], data['data_nascimento'],
                data['telefone'], data['senha']
            ))
            conn.commit()
        conn.close()
        return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()

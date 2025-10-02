from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Simulação de um banco de dados em memória
movies = {}
ratings = {}

@app.route('/')
def index():
    return render_template('index.html', movies=movies)

@app.route('/filme', methods=['POST'])
def add_movie():
    data = request.get_json()
    movie_id = str(len(movies) + 1)
    movies[movie_id] = {'title': data['title'], 'genre': data['genre']}
    return jsonify({'id': movie_id}), 201

@app.route('/avaliacao', methods=['POST'])
def add_rating():
    data = request.get_json()
    movie_id = data['movie_id']
    if movie_id not in movies:
        return jsonify({'error': 'Filme não encontrado'}), 404

    user_id = data['user_id']
    rating = int(data['rating'])

    if movie_id not in ratings:
        ratings[movie_id] = []

    ratings[movie_id].append({'user_id': user_id, 'rating': rating})
    return jsonify({'message': 'Avaliação adicionada com sucesso'}), 201

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
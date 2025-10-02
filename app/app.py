import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# O caminho para nosso "Data Lake" simulado
DATA_LAKE_PATH = '../data_lake_raw/ratings.csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Pega dados do formulário
        user_id = request.form['user_id']
        movie_title = request.form['movie_title']
        rating = request.form['rating']
        
        # Cria um novo DataFrame com os dados
        new_rating = pd.DataFrame({
            'userId': [user_id],
            'movie_title': [movie_title],
            'rating': [rating],
            'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })

        # Salva o novo rating no nosso "Data Lake" (append no CSV)
        # Verifica se o arquivo existe para adicionar ou não o cabeçalho
        if not os.path.exists(DATA_LAKE_PATH):
            new_rating.to_csv(DATA_LAKE_PATH, index=False)
        else:
            new_rating.to_csv(DATA_LAKE_PATH, mode='a', header=False, index=False)
            
        return redirect(url_for('index'))

    # Exibe as últimas 10 avaliações
    ratings_df = pd.DataFrame(columns=['userId', 'movie_title', 'rating', 'timestamp'])
    if os.path.exists(DATA_LAKE_PATH):
        ratings_df = pd.read_csv(DATA_LAKE_PATH)
        
    return render_template('index.html', ratings=ratings_df.tail(10).to_dict('records'))

if __name__ == '__main__':
    # Garante que o diretório do Data Lake exista
    os.makedirs(os.path.dirname(DATA_LAKE_PATH), exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
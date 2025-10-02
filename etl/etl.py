import pandas as pd
from sqlalchemy import create_engine, text
import time
import os

# Aguardar o Postgres iniciar
time.sleep(5) # Reduzido para 5 segundos, geralmente é suficiente

# Configurações do Banco de Dados
DB_USER = 'user'
DB_PASSWORD = 'password'
DB_HOST = 'postgres_dw'
DB_PORT = '5432'
DB_NAME = 'movieflix_dw'

# String de conexão
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URL)

# Caminhos para os arquivos do Data Lake
MOVIES_CSV = '/app/data_lake_raw/movies.csv'
USERS_CSV = '/app/data_lake_raw/users.csv'
RATINGS_CSV = '/app/data_lake_raw/ratings.csv'

def load_data():
    try:
        # ===== NOVA SEÇÃO: Limpa as tabelas antes de inserir =====
        # A ordem é importante por causa das chaves estrangeiras (ratings depende de users)
        with engine.connect() as connection:
            print("Limpando tabelas existentes...")
            # Usamos 'TRUNCATE ... RESTART IDENTITY CASCADE' para resetar as tabelas e suas sequências
            connection.execute(text("TRUNCATE TABLE ratings, users, movies RESTART IDENTITY CASCADE;"))
            connection.commit() # Efetiva a transação
            print("Tabelas limpas com sucesso.")
        # =========================================================

        # Carregar users
        if os.path.exists(USERS_CSV):
            users_df = pd.read_csv(USERS_CSV)
            users_df.rename(columns={'userId': 'user_id'}, inplace=True)
            users_df.to_sql('users', engine, if_exists='append', index=False)
            print("Dados de usuários carregados com sucesso.")

        # Carregar movies
        if os.path.exists(MOVIES_CSV):
            movies_df = pd.read_csv(MOVIES_CSV)
            movies_df.rename(columns={'movieId': 'movie_id'}, inplace=True)
            # Remove a coluna movie_id original se não for serial
            if 'movie_id' in movies_df.columns and movies_df['movie_id'].dtype != 'int64':
                 movies_df.drop(columns=['movie_id'], inplace=True)
            movies_df.to_sql('movies', engine, if_exists='append', index=False)
            print("Dados de filmes carregados com sucesso.")
        
        # Carregar ratings
        if os.path.exists(RATINGS_CSV):
            ratings_df = pd.read_csv(RATINGS_CSV)
            ratings_df.rename(columns={'userId': 'user_id', 'timestamp': 'rated_at'}, inplace=True)
            if 'movieId' in ratings_df.columns:
                ratings_df = ratings_df.drop(columns=['movieId'])
            if 'movie_title' not in ratings_df.columns:
                 ratings_df['movie_title'] = 'Unknown'
            
            ratings_df.to_sql('ratings', engine, if_exists='append', index=False)
            print("Dados de avaliações carregados com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro durante o ETL: {e}")

if __name__ == '__main__':
    load_data()
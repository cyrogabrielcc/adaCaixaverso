import pandas as pd  
from sqlalchemy import create_engine  

print("Iniciando o processo de ETL...")

db_string = "postgresql://user:password@localhost:5432/movieflix_dw"

engine = create_engine(db_string)
print("Conexão com o Data Warehouse estabelecida.")

movies_path = '../datalake/movies.csv'
users_path = '../datalake/users.csv'
ratings_path = '../datalake/ratings.csv'

df_movies = pd.read_csv(movies_path)
df_users = pd.read_csv(users_path)
df_ratings = pd.read_csv(ratings_path)
print("Dados extraídos do Data Lake com sucesso.")

try:
    df_movies.to_sql('movies', engine, if_exists='replace', index=False)
    df_users.to_sql('users', engine, if_exists='replace', index=False)
    df_ratings.to_sql('ratings', engine, if_exists='replace', index=False)
    print("Dados carregados no Data Warehouse com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro durante a carga dos dados: {e}")

print("Processo de ETL concluído.")
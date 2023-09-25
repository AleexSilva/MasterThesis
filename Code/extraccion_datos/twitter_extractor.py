import numpy as np
import tweepy
import time
import yaml #---> Importar parámetros
from decouple import config #---> Para esconder credenciales
import pickle as pk # ---> Para guardar los tweets almacenados


def leer_yaml(path):
    with open(path) as read_file:
        contents = yaml.load(read_file,Loader=yaml.FullLoader)
        return contents


# Parámetros
YAML = leer_yaml('../../utility/parametros.yaml')
q= YAML['Query']
start=YAML['Fecha-Inicio']
end= YAML['Fecha-Fin']

#Credenciales Ocultas
BEARER_TOKEN = config('BEARER_TOKEN')

# Conexión a la API de Twitter
client = tweepy.Client(BEARER_TOKEN,wait_on_rate_limit=True)

tweets=[]

for response in tweepy.Paginator(client.search_all_tweets,
                                query=q,
                                start_time = start,
                                end_time = end,
                                user_fields = YAML['User_fields'],
                                tweet_fields = YAML['Tweet_fields'],
                                expansions = YAML['Expansions'],
                                max_results=500):
    time.sleep(1)
    tweets.append(response)


result = []
user_dict = {}
# Bucle a través de cada objeto de respuesta
for response in tweets:
    # Toma todos los usuarios y los coloca en un diccionario de diccionarios con la información se busca conservar
    for user in response.includes['users']:
        user_dict[user.id] = {'Usuario': user.username, 
                                'Seguidores': user.public_metrics['followers_count'],
                                'cant_tweets': user.public_metrics['tweet_count'],
                                'descripcion': user.description,
                                'locacion': user.location
                            }
    for tweet in response.data:
        # Para cada tweet, encuentra la información del autor.
        author_info = user_dict[tweet.author_id]
        # Poner toda la información que queremos guardar en un solo diccionario para cada tweet
        result.append({'Autor_id': tweet.author_id, 
                        'Usuario': author_info['Usuario'],
                        'Seguidores_autor': author_info['Seguidores'],
                        'Tweets_autor': author_info['cant_tweets'],
                        'Descripcion_autor': author_info['descripcion'],
                        'Locacion_autor': author_info['locacion'],
                        'Texto': tweet.text,
                        'Fecha': tweet.created_at,
                        'Retweets': tweet.public_metrics['retweet_count'],
                        'Respuestas': tweet.public_metrics['reply_count'],
                        'Likes': tweet.public_metrics['like_count'],
                        'Cant_citas': tweet.public_metrics['quote_count'],
                        'Fuente':tweet.source
                        })


Archivo = open('../../data/data_a_procesar/Tweets','wb')
pk.dump(result,Archivo)
Archivo.close()
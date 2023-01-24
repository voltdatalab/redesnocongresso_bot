import tweepy, time, sys
import hashlib  # hash do tweet
import json     # escrever JSON
import os.path  # paths do sistema
import os       # ler variaveis de ambiente
import time     # sleep
import normalize_tweets
from dotenv import load_dotenv # ler variaveis de ambiente do arquivo .env
def main():
    load_dotenv()

    if not os.path.exists('dados/.dummy'):
        print("Faltando pasta ./dados/ (arquivo .dummy nao existe)")
        raise

    if not os.path.exists('dados/tweets.json'):
        print("Faltando arquivo ./dados/tweets.json [execute primeiro o script @elasnacamara.py")
        raise

    if not os.getenv("CONSUMER_KEY"):
        print("Faltando configurar ENV CONSUMER_KEY")
        raise
    if not os.getenv("CONSUMER_SECRET"):
        print("Faltando configurar ENV CONSUMER_SECRET")
        raise
    if not os.getenv("ACCESS_KEY"):
        print("Faltando configurar ENV ACCESS_KEY")
        raise
    if not os.getenv("ACCESS_SECRET"):
        print("Faltando configurar ENV ACCESS_SECRET")
        raise

    dirName = 'dados/tweets-enviados/'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Diretorio " , dirName ,  " criado")

    with open('dados/tweets.json') as f:
        tweets = json.load(f)

        consumer_key= os.getenv("CONSUMER_KEY")
        consumer_secret= os.getenv("CONSUMER_SECRET")
        access_token= os.getenv("ACCESS_KEY")
        access_token_secret= os.getenv("ACCESS_SECRET")

        client = tweepy.Client(consumer_key= consumer_key,consumer_secret= consumer_secret,access_token= access_token,access_token_secret= access_token_secret)

        for tweet in tweets:
            text = tweet['tweet']

            result = hashlib.md5(text.encode())
            fileName = f'{dirName}/{result.hexdigest()}'
            if os.path.exists( fileName ):
                print ("\n/////--- tweet '", text, "' ja foi tweetado")
                continue

            try:

                print ("tweetando '", text, "'...\n\n")
                response = client.create_tweet(text=normalize_tweets.norm(text))
                if response[0]['id'] == None:
                    print("Erro ao enviar tweet")
                    continue

                with open(fileName, 'w') as outfile:
                    json.dump(response[0], outfile)

            except Exception as e:
                print("Erro ao enviar tweet")
                print(e)
                
                if "duplicate" in str(e):
                    print("Tweet duplicado")
                    continue
                if "text is too long" in str(e):
                    print("Tweet muito longo")
                    continue
                continue

            if bool(os.getenv("RANDOM_SLEEP_BETWEEN_TWEETS")):
                time.sleep(300) # espera 5 minutos

if __name__ == "__main__":
    main()
    print ("Todos tweets enviados com sucesso!")
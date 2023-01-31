import tweepy, time, sys
import hashlib  # hash do tweet
import json     # escrever JSON
import os.path  # paths do sistema
import os       # ler variaveis de ambiente
import time     # sleep
import normalize_tweets
from dotenv import load_dotenv # ler variaveis de ambiente do arquivo .env
import utils
import ia
load_dotenv()
import asyncio

async def main():

    if not os.path.exists('dados/.dummy'):
        print("Faltando pasta ./dados/ (arquivo .dummy nao existe)")
        raise

    if not os.path.exists('dados/tweets.json'):
        print("Faltando arquivo ./dados/tweets.json [execute primeiro o script @nocongresso.py")
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

        auth = tweepy.OAuth1UserHandler(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
        )

        api = tweepy.API(auth)

        # client = tweepy.Client(consumer_key= consumer_key,consumer_secret= consumer_secret,access_token= access_token,access_token_secret= access_token_secret)

        for tweet in tweets:
            
            text = tweet['tweet']
            titulo = tweet['titulo']

            result = hashlib.md5(text.encode())
            fileName = f'{dirName}/{result.hexdigest()}'
            if os.path.exists( fileName ):
                print ("\n/////--- tweet '", text, "' ja foi tweetado")
                continue
            
            try:
                titulo = ia.summarize_text(titulo)
            except Exception as e:
                print("Erro ao resumir a descrição: ", e)

            try:

                print ("tweetando '", text, "'...\n\n")

                

                await utils.text_to_image(normalize_tweets.removeNone(text), titulo)
                # response = api.update_status_with_media(status=normalize_tweets.norm(text), filename='html/out.png')

                res = api.media_upload("html/out.png")
                text_no_emoji = normalize_tweets.removeEmoji(text)
                api.create_media_metadata(res.media_id, alt_text=titulo+'\n\n'+text_no_emoji)
                status = api.update_status(media_ids = [res.media_id], status=normalize_tweets.norm(text))
             
                with open(fileName, 'w') as outfile:
                    json.dump(status._json, outfile)

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

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print ("Todos tweets enviados com sucesso!")
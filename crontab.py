#main do nocongresso.py

import nocongresso
import enviar_tweets
import os

if __name__ == "__main__":
    nocongresso.main()
    enviar_tweets.main()

    try:
        os.remove('dados/tweets.json')
    except Exception as e:
        print(e)
        


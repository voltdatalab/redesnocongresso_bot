#main do nocongresso.py

import nocongresso
import enviar_tweets
import os
import hashlib

if __name__ == "__main__":

    try:
        nocongresso.main()
        enviar_tweets.main()
    except Exception as e:
        print(e)
        


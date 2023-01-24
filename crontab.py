#main do nocongresso.py

import nocongresso
import enviar_tweets
import os
import hashlib

if __name__ == "__main__":
    nocongresso.main()
    enviar_tweets.main()

    try:
        # renomear arquivo de tweets
        hash_file = hashlib.md5(open('dados/tweets.json', 'rb').read()).hexdigest()
        os.rename('dados/tweets.json', 'dados/tweets-' + hash_file + '.json')
    except Exception as e:
        print(e)
        


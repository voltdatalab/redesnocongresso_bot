import nocongresso
import enviar_tweets

if __name__ == "__main__":

    try:
        nocongresso.main()
        enviar_tweets.main()
    except Exception as e:
        print(e)
        
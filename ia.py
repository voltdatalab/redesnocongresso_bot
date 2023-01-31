import openai
import os.path  # paths do sistema
import os       # ler variaveis de ambiente
import time
from dotenv import load_dotenv # ler variaveis de ambiente do arquivo .env
load_dotenv()

def summarize_text(text):
    time.sleep(2)
    openai.api_key = os.getenv("OPEN_IA_KEY")

    # Set up the model and prompt
    model_engine = "text-davinci-003"
    prompt = "Summarize the main points in up to 130 characters in the following text:" + text

    try:
        # Generate a response
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response = completion.choices[0].text
        # print(response)
        # print('\n\n')
        # print(len(response))
        # print('\n\n')
        # print(completion)

        return response

    except Exception as e:
        print(e)
        if type(e) == openai.error.RateLimitError:
            print("You exceeded your current quota,")
            print("please wait a few minutes and try again.")

        return ''


import os, requests
from dotenv import load_dotenv

def cria_link(url_antiga, congresso=False, senado=False, dou=False):
    load_dotenv()

    headers = {
        'accept': 'application/json',
        'X-Api-Key': os.getenv("API_SHLINK"),
        'Content-Type': 'application/json',
    }

    tags = ['legislaredes_bot']
    if congresso: tags.append('congresso')
    if senado: tags.append('senado')
    if dou: tags.append('dou')

    json_data = {
        'longUrl': url_antiga,
        'tags': tags,
        'crawlable': True,
        'forwardQuery': True,
        'findIfExists': True,
        'shortCodeLength': 5,
    }

    response = requests.post('https://nucle.ooo/rest/v3/short-urls', headers=headers, json=json_data)
    print("LINK, ", url_antiga)
    print(response.status_code)
    try:
        if len(response.json()['shortUrl']) > 0:
            return response.json()['shortUrl']
    except Exception as e:
        print("ERRO", e)
        return url_antiga

# Usado para testar o módulo
if __name__ == '__main__':
    url_inicial = 'https://nucleo.jor.br/bedelbot/'

    print('Criando URL de teste a partir de', url_inicial)
    link = cria_link(url_inicial, congresso=True, senado=True, dou=True)
    print('Shlink retornado:', link)

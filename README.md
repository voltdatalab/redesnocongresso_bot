# Legisla Redes

Robô do @nucleojor para monitoramento das tramitações de proposições que tratam sobre redes sociais no Congresso. 

Código Fonte e Inspiração @elasnocongresso
Elas no Congresso no Twitter: https://twitter.com/elasnocongresso

# o robô (https://twitter.com/legislaredes)

Essa aplicação em Python utiliza a API de proposições da Câmara dos Deputados e do Senado para monitorar projetos de interesse que tratam sobre redes sociais. 

# links de referência

Legisla Redes no Twitter: https://twitter.com/legislaredes

API da Câmara dos Deputados: https://dadosabertos.camara.leg.br/swagger/api.html (Proposições).

API do Senado: https://www12.senado.leg.br/dados-abertos/conjuntos?grupo=projetos-e-materias&portal=legislativo

# instalando dependencias

> Primeiro verificar se o pip para o python3 está instalado (sudo apt install python3-pip em debian-like)

    $ python3 -m pip --version

Deve exibir: `pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)` ou semelhante

    $ python3 -m pip install -r requirements.txt

# executando

Para baixar as proposições, basta executar o arquivo `elasnocongresso.py`, o resultado dos tweets será salvo em ./dados/tweets.json, você pode visualizar este arquivo para conferir o contéudo.

Caso esteja tudo OK com o conteudo, você deve executar o script `enviar_tweets.py` para fazer o envio.

Para executar `enviar_tweets.py`, será necessário configurar o arquivo .env com a chave do twitter:

    $ cp .env.sample .env

Edite o conteudo do .env com a chave, e então poderá ser possível executar o envio.

ou executar geral `python crontab.py`

# Créditos

A licença é creative commons e ele pode ser usado e replicado à vontade, mesmo sem pedir permissão e sem citação de fonte (mas se você utilizar e for uma pessoa legal e transparente, pode dar crédito para a Revista AzMina).

https://github.com/institutoazmina/elasnocongressobot

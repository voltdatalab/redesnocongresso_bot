from datetime import date
import requests
import os
from dotenv import load_dotenv

load_dotenv()

login = os.getenv('DOU_LOGIN')
senha = os.getenv('DOU_SENHA')

tipo_dou="DO1 DO2 DO3 DO1E DO2E DO3E" # Seções separadas por espaço
# Opções DO1 DO2 DO3 DO1E DO2E DO3E

url_login = "https://inlabs.in.gov.br/logar.php"
url_download = "https://inlabs.in.gov.br/index.php?p="

payload = {"email" : login, "password" : senha}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
s = requests.Session()
s.verify=False

def download(day=date.today()):
    if s.cookies.get('inlabs_session_cookie'):
        cookie = s.cookies.get('inlabs_session_cookie')
    else:
        print("Falha ao obter cookie. Verifique suas credenciais");
        exit(37)
    
    # Montagem da URL:
    ano = day.strftime("%Y")
    mes = day.strftime("%m")
    dia = day.strftime("%d")
    data_completa = ano + "-" + mes + "-" + dia
    
    for dou_secao in tipo_dou.split(' '):
        print("Aguarde Download...")
        url_arquivo = url_download + data_completa + "&dl=" + data_completa + "-" + dou_secao + ".zip"
        cabecalho_arquivo = {'Cookie': 'inlabs_session_cookie=' + cookie, 'origem': '736372697074'}
        response_arquivo = s.request("GET", url_arquivo, headers = cabecalho_arquivo)
        if response_arquivo.status_code == 200:
            with open(data_completa + "-" + dou_secao + ".zip", "wb") as f:
                f.write(response_arquivo.content)
                print("Arquivo %s salvo." % (data_completa + "-" + dou_secao + ".zip"))
            del response_arquivo
            del f
        elif response_arquivo.status_code == 404:
            print("Arquivo não encontrado: %s" % (data_completa + "-" + dou_secao + ".zip"))
    
    print("Busca encerrada")

def inlabs_dou(day=date.today()):
    try:
        response = s.request("POST", url_login, data=payload, headers=headers)
        download(day)
    except requests.exceptions.ConnectionError:
        inlabs_dou(day)

if __name__ == '__main__':
    inlabs_dou()


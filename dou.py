#!/usr/bin/env python
# coding: utf-8

# -*- coding: utf-8
# Código Original de (https://azmina.com.br/) Reinaldo Chaves (reichaves@gmail.gom) & Bárbara Libório
# Script para ler as APIs da Câmara e Senado
# Procurar proposições do dia anterior e corrente
# Filtrar aquelas de interesse para os direitos da mulheres
# Criar frases com os resumos da tramitação
# E tweetar no @elasnocongresso

# Modificação Núcleo - Henrique Rieger (henrique@voltdata.info)

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import os
import json
import random

import glob
from zipfile import ZipFile, BadZipFile
from inlabs import inlabs_dou 
from bs4 import BeautifulSoup

from dotenv import load_dotenv
load_dotenv()

def salva_json_antigos():
    with open('dados/tweets-dou.json') as f:
        tweets = json.load(f)
        with open('dados/t_salvos.json', 'w') as f:
            json.dump(tweets, f, indent=2)

def cria_link(url_antiga):
    headers = {
        'accept': 'application/json',
        'X-Api-Key': os.getenv("API_SHLINK"),
        'Content-Type': 'application/json',
    }

    json_data = {
        'longUrl': url_antiga,
        'tags': [
            'legislaredes_bot',
            'dou',
        ],
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

# Carrega lista de termos de interesse
def carrega_termos():
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSGZoyvn_NamWZG7DqXInBYsinKaIjuQDJiJ_L4iBsXZO7rdV0lCke817l7nthVzxRImPkQjPzQVI5y/pub?gid=0&single=true&output=csv")
    search_list = []
    for i in df.values:
        search_list.append(i[0])
    return search_list

# Define termos de interesse
try:
    search_list = carrega_termos()
    print('\\\\\\\\\\\\\\\\\\\\ Termos de interesse carregados: ', len(search_list), ' \\\\\\\\\\\\\\\\\\ \n')
except Exception as e:
    print("Erro ao carregar termos de interesse")
    print(e)
    search_list = ["plataformas digitais", "plataforma digital", "redes sociais", "rede social", "políticas digitais", "política digital", "facebook", "twitter", "google", "youTube", "gettr", "bytedance", "tiktok", "telegram", "rumble", "regulação de redes", "regulação de plataformas", "regulação de redes sociais", "big tech", "regulação de big techs"]

# Transforma em maiúsculas
search_list = [x.upper() for x in search_list]

# FUNÇÃO DE DELAY
def delay(inicio = 1, fim = 2):
    tempo = random.randint(inicio, fim)
    print("Tempo de espera: %s" % tempo)
    time.sleep(tempo)

# FUNÇÃO DO DIARIO OFICIAL DA UNIAO
def dou():
    today = datetime.now()
    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = (today - timedelta(days=1)).strftime('%Y-%m-%d')

    for i in range(0, 1):
        date = today-timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        inlabs_dou(date)

        # Descompacta arquivos obtidos pelo inlabs
        for filename in glob.glob(f'./{date_str}-*.zip', recursive=False):
            try:
                with ZipFile(filename, 'r') as zip_ref:
                    zip_ref.extractall('dou/'+date_str)
            except BadZipFile:
                print(f'Arquivo .zip com erro: {filename}')
            finally:
                os.remove(filename)

    diarios = []
    for filename in glob.glob(r'dou/*/*.xml'):
        with open(filename, 'r') as f:
            soup = BeautifulSoup(f.read(), 'xml')
            article = soup.find('article')
            article_id = article['id']
            nome = article['name']
            data = article['pubDate']
            link = article['pdfPage']
            identifica = " ".join(soup.find('Identifica').contents)
            
            internal_soup = BeautifulSoup(soup.find('Texto').text, 'html.parser')
            texto = internal_soup.find_all(text=True, recursive=True)
            texto = "\n".join(texto)

            dicionario = {
                    'id': article_id,
                    'nome': nome,
                    'data': data,
                    # 'link': cria_link(link),
                    'link': link,
                    'identifica': identifica,
                    'texto': texto
            }
            diarios.append(dicionario)

    return redes(pd.DataFrame(diarios), 'dou')
    # return pd.DataFrame(diarios)

# FUNÇÃO PARA TERMOS DE INTERESSE
def redes(dados, origem):
    print(search_list)
    mask = dados['texto'].str.contains('|'.join(search_list))


    seleciona = dados[mask]

    print(dados[mask])
    return seleciona

# CRIA FRASES
def frases(dados, origem):
    lista_sentencas = []

    conta = 1
    for num, row in dados.iterrows():

        if origem == 'senado':
                    proposicao_ementa = row['ementa_minuscula']
                    proposicao_tipo = row['SiglaSubtipoMateria']
                    proposicao_numero = row['NumeroMateria']
                    proposicao_ano = row['AnoMateria']
                    tramitacao = row['NomeLocal']
                    status = row['DescricaoSituacao']
                    endereco = row['UrlTexto']
                    nome = row['NomeAutor']
                    data_status = None
                    casa = 'SENADO'
        elif origem == 'camara':
                    proposicao_ementa = row['ementa_minuscula']
                    proposicao_tipo = row['siglaTipo']
                    proposicao_numero = row['numero']
                    proposicao_ano = row['ano']
                    tramitacao = row['statusProposicao_descricaoTramitacao']
                    status = row['statusProposicao_descricaoSituacao']
                    endereco = row['urlInteiroTeor']
                    nome = str(row['autor']).replace("[", "")
                    nome = nome.replace("]", "")
                    nome = nome.replace("'", "")
                    data_status = row['statusProposicao_dataHora']
                    data_status = datetime.strptime(data_status, '%Y-%m-%dT%H:%M')
                    data_status = data_status.strftime('%d/%m/%Y %H:%M')
                    casa = 'CÂMARA'

        try:
            if len(nome) > 80:
                nome = nome[:80] + '...'
        except Exception as e:
            print('Erro ao cortar nome do autor.')
            print(e)

        endereco = cria_link(endereco)

        sentencas = {}

        search_list_lower = [ s.lower() for s in search_list]

        for s in range(len(search_list_lower)):
            if search_list_lower[s] in proposicao_ementa:
                texto = f'{casa}: {proposicao_tipo} {proposicao_numero}/{proposicao_ano}.\n🕙 Última atualização: {data_status}.\n📕 Nome: {nome}.\n💡 Tema: {search_list_lower[s].upper()}.\n🔈 Tramitação: {tramitacao}.\n↪️ Situação: {status}.\n🔗 {endereco}'
                # adicionar proposicao_ementa e texto dentro de sentencas
                sentencas['texto'+str(s)+'/' + str(conta)] = {'tweet': texto,'titulo':proposicao_ementa}


    
        # Testa se dicionario veio vazio
        res = not bool(sentencas)
        if res == False:
            lista_sentencas.append(sentencas)

        conta = conta + 1

    df_lista_sentencas = pd.DataFrame(lista_sentencas)

    return df_lista_sentencas

GLOBAL_lista_para_tweetar = []

# TWEETA AS FRASES
def tweeta(dados):

    # Isola apenas primeiras linhas
    df = dados.bfill().iloc[[0]]
    columns = list(df)

    # Itera nas colunas de cada frase
    for i in columns:
        texto = df[i][0]
        GLOBAL_lista_para_tweetar.append( { "tweet": texto['tweet'], "titulo":texto['titulo'].title() })

# DEFINIR BLOCO DE EXECUÇÃO PRINCIPAL
def main():

    # Captura diarios oficiais
    prop_dou = dou()
    tamanho = len(prop_dou.index)
    print("\n\nQuantidade de DOUs de interesse: ", tamanho)
    prop_dou.info()
    prop_dou.to_csv('teste.csv')
    quit()

    # Cria frases do DOU
    if tamanho != 0:
        df_lista_sentencas = frases(prop_dou, 'camara')
        print(df_lista_sentencas)

         # Faz Tweets
        #tam_frases = len(df_lista_sentencas.index)
        #if tam_frases > 0:
        #    tweeta(df_lista_sentencas)


# executar bloco principal
if __name__ == '__main__':
    main()

    with open('dados/tweets-dou.json', 'w') as outfile:
        json.dump(GLOBAL_lista_para_tweetar, outfile)

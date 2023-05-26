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
from datetime import datetime, date, timedelta
import os
import json
import random

import glob
from zipfile import ZipFile, BadZipFile
from inlabs import inlabs_dou 
from bs4 import BeautifulSoup

from shlink import cria_link

from dotenv import load_dotenv
load_dotenv()

def salva_json_antigos():
    with open('dados/tweets-dou.json') as f:
        tweets = json.load(f)
        with open('dados/t_salvos.json', 'w') as f:
            json.dump(tweets, f, indent=2)

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

# ROTINA DO DIARIO OFICIAL DA UNIAO
def dou():
    today = date.today()
    get_dou_xml(today, today)
    return get_info_from_xml()

# OBTEM ARQUIVOS XML DOS DOU 
def get_dou_xml(from_date: date, to_date: date):
    day = to_date
    while day >= from_date:
        inlabs_dou(day)

        # Descompacta arquivos obtidos pelo inlabs
        day_str = day.strftime('%Y-%m-%d')
        for filename in glob.glob(f'./{day_str}-*.zip', recursive=False):
            try:
                with ZipFile(filename, 'r') as zip_ref:
                    zip_ref.extractall('dou/'+day_str)
            except BadZipFile:
                print(f'Arquivo .zip com erro: {filename}')
            finally:
                os.remove(filename)
        day -= timedelta(days=1)

# RETORNA JSON COM DADOS 
def get_info_from_xml():
    diarios = []
    for filename in glob.glob(r'dou/*/*.xml'):
        with open(filename, 'r') as f:
            soup = BeautifulSoup(f.read(), 'xml')
            article = soup.find('article')
            internal_soup = BeautifulSoup(soup.find('Texto').text, 'html.parser')

            texto = internal_soup.find_all(text=True, recursive=True)
            texto = "\n".join(texto)

            identifica = soup.find('Identifica').text.strip()

            dicionario = {
                    'id': article['id'],
                    'nome': article['name'],
                    'id_oficio': article.get('idOficio'),
                    'nome_pub': article['pubName'],
                    'tipo_art': article.get('artType'),
                    'data': datetime.strptime(article['pubDate'], '%d/%m/%Y'),
                    'classe_art': article.get('artClass'),
                    'categoria_art': article.get('artCategory'),
                    'tam_art': article.get('artSize'),
                    'notas_art': article.get('artNotes'),
                    'num_pagina': article.get('numberPage'),
                    #'link': cria_link(article['pdfPage'], dou=True),
                    'link': article['pdfPage'],
                    'num_edicao': article.get('editionNumber'),
                    'tipo_destaque': article.get('highlightType'),
                    'prioridade_destaque': article.get('highlightPriority'),
                    'destaque': article.get('highlight'),
                    'img_destaque': article.get('highlightimage'),
                    'nome_img_destaque': article.get('highlightimagename'),
                    'id_materia': article.get('idMateria'),
                    'texto': texto,
                    'identifica': identifica
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

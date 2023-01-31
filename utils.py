from PIL import Image
import imgkit

import os
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
async def text_to_image(texto, descricao):

    titulo = texto.split('\n')[0]
    url = texto.split('\n')[-1].replace('🔗 ', '')
    new_texto = [t.split(': ') for t in texto.split('\n')[1:-1]]
    valores = {}
    valores['titulo'] = titulo
    for tipo, texto in new_texto:
        if tipo == '🕙 Última atualização':
            valores['data'] = texto
        elif tipo == '📕 Nome':
            valores['nome'] = texto
        elif tipo == '💡 Tema':
            valores['tema'] = texto
        elif tipo == '🔈 Tramitação':
            valores['tramitacao'] = texto
        elif tipo == '↪️ Situação':
            valores['situacao'] = texto

    valores['url'] = url

    insert_html = ""

    for k, v in valores.items():
        if k == 'titulo':
            new_titulo = v.split(': ')
            insert_html += f"  <b> {new_titulo[0]}:  <span class='valor'>{new_titulo[1]}</span> </b></br>"
        elif k == 'data':
            insert_html += f"  <small>ATUALIZAÇÃO: {v}</small>  "
        elif k == 'nome':
            if len(v) > 130:
                v = v[:127] + '...'
            insert_html += f"</br>AUTOR/RELATOR: <span class='nome'>{v}</span>"
        elif k == 'tema':
            insert_html += f"</br>TEMA:<span class='tema'>{v}</span>"
        elif k == 'tramitacao':
            insert_html += f"</br>TRAMITAÇÃO: <span class='redeytgoogle'>{v}</span>"
        elif k == 'situacao':
            insert_html += f"</br>SITUAÇÃO: <span class='redeytgoogle'>{v}</span>"
        elif k == 'url':
            new_link = v.replace('https://', '')
            insert_html += f"</br> Link: <b>{new_link}</b>"
    
    
    if len(descricao) < 130:
        descricao = f'<div class="titulo"> {descricao} </div>'
    else:
        descricao = f'<div class="titulo"> {descricao[:127]}... </div>'

    html = """

    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="css/styles.css">

        <script src="js/twemoji.min.js"></script>
        <script>window.onload = function () {}</script>

    </head>
    <body>
    <p>
    {}
    {}
    <img src='landing-nucleo_logo-header.png'><br>
    <url>nucleo.jor.br/legislaredes</url>
    </body>
    </html>
    """.format("{twemoji.parse(document.body);}", insert_html, descricao)

    with open('html/tmp.html', 'w') as f:
        f.write(html)

    kitoptions = {  "enable-local-file-access": None , "encoding": 'UTF-8'}
    imgkit.from_url("file://" + os.getcwd() + "/html/tmp.html", output_path='html/out.png', options=kitoptions)
    
    img = Image.open('html/out.png')
    height = img.size[1]

    img2 = img.crop((0, 0, 600, height))
    img2.save('html/out.png')

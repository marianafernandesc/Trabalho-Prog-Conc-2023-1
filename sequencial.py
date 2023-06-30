import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup
import os
from time import sleep
# import pdfkit
import time
from weasyprint import HTML

# abrir os links
# abrir cada site e fazer a leitura do html
# escrever o html
# pegar o tetxo do html

# coin free
# transformar em pdf

def get_numerical_part(filename):
    # Extrai a primeira parte numérica do nome do arquivo
    numerical_part = ""
    for char in filename:
        if char.isdigit():
            numerical_part += char
        elif numerical_part:
            break
    
    # Tenta converter a parte numérica em um inteiro
    try:
        return int(numerical_part)
    except ValueError:
        return 0

def novelChapter(index, tittle, novel, link=""):
        if len(link) != 0:
            #processador_atual = os.sched_getaffinity(0)
            #print(processador_atual)
            grab_page = requests.get(link) 
            parse_page = BeautifulSoup(grab_page.content, "html.parser")
            #print(parse_page)
            mychapters = parse_page.find_all("div", {"class": "chr-c"})
            #print(mychapters)
            filename = f'{tittle}/{index}.html'
            
        else:
            novel = re.sub(r'\d', '', novel)
            grab_page = requests.get(novel+str(index)) 
            parse_page = BeautifulSoup(grab_page.content, "html.parser")
            mychapters = parse_page.find_all("div", {"class": "reading-content"})
            filename = f'{tittle}/{index}.html'
        with open(filename,  "w", encoding='utf-8') as novels:
            novels.write(str(mychapters))
        sleep(5)

def converter_html_para_pdf(nome_arquivo_html, nome_arquivo_pdf):
    HTML(nome_arquivo_html).write_pdf(nome_arquivo_pdf)

def verificarLista():
    novelsABaixar = []
    with open('novelLinks.txt', 'r') as novels:
        for novel in novels:
            novelsABaixar.append(novel.strip()) 
    return novelsABaixar


start = time.time()
novels = verificarLista()
createdPaths =[]
for novel in novels:
    qnt = re.findall(r'\d+', novel)
     #break
    #  https://wordexcerpt.com/series/daddy-i-dont-want-to-marry/chapter-99
    
    tittle = (novel.split('/'))[4]
    print(f"Novel {tittle} com {qnt[0]} capítulos")
    if "159.223.185.88" in novel or "novelbank" in novel:            
            #print(novelsLinks)
            novelsLinks={}
            tittle = tittle.rsplit('-', 1)[0]
    pathTittle = Path(tittle)
    if not pathTittle.exists():
        pathTittle.mkdir()
    createdPaths.append(tittle)
     
    if "159.223.185.88" in novel or "novelbank" in novel:            
            #print(novelsLinks)
            #print(tittle)
            ajaxFile= f"https://novelbank.net/ajax/chapter-archive?novelId={(tittle)}"
            #print(ajaxFile)
            wafProtectionOff = True
            grab_page = requests.get(ajaxFile) 
            parse_page = BeautifulSoup(grab_page.content, "html.parser")
            links = parse_page.find_all("a")
            for link in links:
                title = link.text.strip()
                href = link.get("href")
                novelsLinks[title] = href
            for chave, valor in novelsLinks.items():
                valor = valor.replace("https://novelbank.net", "http://159.223.185.88:3004")
                novelChapter(chave, tittle, novel,valor)
            break
    for index in range(1,int(qnt[0])):
            novelChapter(index, tittle, novel)
#createdPaths.append("daddy-i-dont-want-to-marry")
conteudo=""
for path in createdPaths:
    for nome_arquivo in sorted(os.listdir(path)):
        
        caminho_arquivo = os.path.join(path, nome_arquivo)
        if os.path.isfile(caminho_arquivo) and path not in nome_arquivo:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo += arquivo.read()
                #print( f"{caminho_arquivo}")
                # Faça algo com o conteúdo do arquivo
    filename = f'{path}/{path}Completed.html'
    with open(filename,  "w", encoding='utf-8') as novels:
            novels.write((conteudo))

    #for nome_arquivo in os.listdir(path):
    #    caminho_arquivo = os.path.join(path, nome_arquivo)
    #    if os.path.isfile(caminho_arquivo) and path not in nome_arquivo:
    #        os.remove(caminho_arquivo)

    converter_html_para_pdf(filename, f'{path}.pdf')

print(novels)
print(" {} seconds".format( time.time() - start))

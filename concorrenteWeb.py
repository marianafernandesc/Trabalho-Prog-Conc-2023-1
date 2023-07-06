import requests
import streamlit as st 
import multiprocessing
import re
from pathlib import Path
from bs4 import BeautifulSoup
import os
import sys
from time import sleep
# import pdfkit
import time
from weasyprint import HTML
from tqdm import tqdm
import psutil
import webbrowser

# abrir os links
# abrir cada site e fazer a leitura do html
# escrever o html
# pegar o tetxo do html

# coin free
# transformar em pdf

    # More Code

#with tqdm(total=100, desc='cpu%', position=1) as cpubar, tqdm(total=100, desc='ram%', position=0) as rambar:
 #   while True:
  #      rambar.n=psutil.virtual_memory().percent
   #     cpubar.n=psutil.cpu_percent()
    #    rambar.refresh()
     #   cpubar.refresh()
      #  sleep(0.5)


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

def converter_html_para_pdf(nome_arquivo_html, nome_arquivo_pdf):
    HTML(nome_arquivo_html).write_pdf(nome_arquivo_pdf)
    webbrowser.open(nome_arquivo_pdf)

def verificarLista():
    novelsABaixar = []
    with open('novelLinks.txt', 'r') as novels:
        for novel in novels:
            novelsABaixar.append(novel.strip()) 
    return novelsABaixar


start = time.time()
novelsInit = verificarLista()
createdPaths =[]

def simpleRequest(index, tittle, novel, link=""):
        #print(link)
        if len(link) != 0:
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

def leituraNovels(qntProcessadores, novels=novelsInit):
        print(novels)
        for novel in novels:
        # novel = "http://159.223.185.88:3004/novelbank/the-guidebook-for-villainesses-nov1162750819/181-chapter-181"
        # https://novelbank.net/ajax/chapter-archive?novelId=the-guidebook-for-villainesses
            tittle = (novel.split('/'))[4]
            qnt = re.findall(r'\d+', novel)
            print(f"Novel {tittle} com {qnt[0]} capítulos")
            wafProtectionOff = False
            novelsLinks = {}
            if "159.223.185.88" in novel or "novelbank" in novel:
                tittle = tittle.rsplit('-', 1)[0]
                ajaxFile = f"https://novelbank.net/ajax/chapter-archive?novelId={(tittle)}"
                wafProtectionOff = True
                grab_page = requests.get(ajaxFile)
                parse_page = BeautifulSoup(grab_page.content, "html.parser")
                links = parse_page.find_all("a")
                for link in links:
                    title = link.text.strip()
                    href = link.get("href")
                    novelsLinks[title] = href
            pathTittle = Path(tittle)
            if not pathTittle.exists():
                pathTittle.mkdir()
            createdPaths.append(tittle)

            pool = multiprocessing.Pool(processes=qntProcessadores)
            if "159.223.185.88" in novel or "novelbank" in novel:
                for chave, valor in novelsLinks.items():
                    valor = valor.replace("https://novelbank.net", "http://159.223.185.88:3004")
                    pool.apply_async(simpleRequest, (chave, tittle, novel, valor,))
            else:
                for index in range(1, int(qnt[0])):
                    pool.apply_async(simpleRequest, (index, tittle, novel,))
                    
            
            pool.close()
            pool.join()


        parteConcorrente =(" {} seconds".format( time.time() - start))
        parteSequencialInit = time.time()
        sequencialPart()
        parteSequencial = (" {} seconds".format( time.time() - parteSequencialInit))
        total =(" {} seconds".format( time.time() - start))

#createdPaths.append("daddy-i-dont-want-to-marry")

def sequencialPart():
    
    print(createdPaths)
    for path in createdPaths:
        conteudo=""
        for nome_arquivo in sorted(os.listdir(path), key=get_numerical_part):
            
            caminho_arquivo = os.path.join(path, nome_arquivo)
            if os.path.isfile(caminho_arquivo) and path not in nome_arquivo:
                with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                    conteudo += arquivo.read()
                    print( f"{caminho_arquivo}")
                    # Faça algo com o conteúdo do arquivo
        
        filename = f'{path}/{path}Completed.html'
        print(filename)
        with open(filename,  "w", encoding='utf-8') as novels:
                novels.write((conteudo))

        #for nome_arquivo in os.listdir(path):
        #    caminho_arquivo = os.path.join(path, nome_arquivo)
        #   if os.path.isfile(caminho_arquivo) and path not in nome_arquivo:
        #       os.remove(caminho_arquivo)

        converter_html_para_pdf(filename, f'{path}.pdf')


def main():
    st.title("Novel Scraper")

    # Input field for URLs
    urls = st.text_area("Enter URLs (one per line)", height=200)

    # Input field for processor count
    qntProcessadores = st.number_input("Enter processor count", min_value=1, step=1, value=5)

    # Button to start the process
    if st.button("Start"):
        novels = urls.split('\n')
        leituraNovels(qntProcessadores, novels)

    # Progress bar
    progress_bar = st.progress(0)

    # Elapsed time

    start_time = time.time()

    
    print(" {} seconds".format( time.time() - start))

if __name__ == '__main__':
    main()
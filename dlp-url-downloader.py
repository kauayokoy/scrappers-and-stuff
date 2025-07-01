from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import getpass
import yt_dlp
import time
import os

def login(driver, email, senha):
    try:
        campousuario = driver.find_element(By.NAME, "email")
        campousuario.send_keys(email)
        time.sleep(0.5)

        camposenha = driver.find_element(By.NAME, "password")
        camposenha.send_keys(senha)
        camposenha.send_keys(Keys.RETURN)
        time.sleep(1)
    except Exception as e:
        print("login error", e)
        driver.quit()

def scrap_aulas():
    driver = webdriver.Chrome()

    url = input("url_login ").strip()
    next_url = input("url_first_class").strip()
    email = input("email ").strip()
    senha = getpass.getpass("passwd ")

    driver.get(url)
    time.sleep(1)
    
    login(driver, email, senha)
    driver.get(next_url)

    while True:
        try:
            urlatual = driver.current_url
            with open("saco.txt", 'a', encoding='utf-8') as arquivo:
                arquivo.write(url_atual + "\n")
            print("url", url_atual)

            try:
                botao = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Ir para a proxima aula"]'))
                )
            except TimeoutException:
                botao = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Ir para o próximo módulo"]'))
                )

            botao.click()
            print("going to next class)
            time.sleep(2)
        except Exception as e:
            print("error", e)
            break

    driver.quit()

def organizer():
    urls_salvas = set()

    try:
        with open("saco.txt", 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                url = linha.strip()
                urls_salvas.add(url)

        with open("urls.txt", 'w', encoding='utf-8') as arquivo:
            for url in sorted(urls_salvas):
                partes = url.split("/")
                if len(partes) > 5:
                    nome_formatado = partes[5].replace("-", " ").capitalize()
                    arquivo.write(f"{nome_formatado}\n{url}\n")
    except FileNotFoundError:
        print("file 'txt' not found.")

def downloaderdlp():
    if not os.path.exists("videos"):
        os.makedirs("videos")

    try:
        with open("urls.txt", 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            for i in range(0, len(linhas), 2):
                titulo = linhas[i].strip().replace(" ", "_")
                url = linhas[i+1].strip()

                print(f"⬇️ Baixando: {titulo}")
                ydl_opts = {
                    'outtmpl': f'videos/{titulo}.mp4',
                    'quiet': False,
                    'format': 'bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4',
                    'noplaylist': True,
                    'ignoreerrors': True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
    except FileNotFoundError:
        print("url not found")
    except Exception as e:
        print(f"download error {e}")

if __name__ == "__main__":
    print("""
    [1] Scrap with selenium
    [2] organize urls on .txt for manual digging
    [3] yt-dlp video downloader
    """)
    opcao = input("option ").strip()

    if opcao == "1":
        scrap_aulas()
    elif opcao == "2":
        organizer()
    elif opcao == "3":
        baixar_videos()
    else:
        print("invalid option.")

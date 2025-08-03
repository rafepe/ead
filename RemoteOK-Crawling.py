# RODAR EM UM ARQUIVO .py EM AMBIENTE LOCAL

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

options = Options()
# Headless moderno (Chrome ≥ 109)
options.add_argument('--headless=new')

langs = ['TypeScript',
 'C_Sharp',
 'Rust',
 'HTML',
 'Python',
 'JavaScript',
 'Java',
 'C',
 'C_Plus_Plus',
 'SQL']

urls = ['https://remoteok.com/remote-typescript-jobs?order_by=date',
        'https://remoteok.com/remote-c-sharp-jobs?order_by=date',
        'https://remoteok.com/remote-rust-jobs?order_by=date',
        'https://remoteok.com/remote-html-jobs?order_by=date',
        'https://remoteok.com/remote-python-jobs?order_by=date',
        'https://remoteok.com/remote-javascript-jobs?order_by=date',
        'https://remoteok.com/remote-java-jobs?order_by=date',
        'https://remoteok.com/remote-c-jobs?order_by=date',
        'https://remoteok.com/remote-c-plus-plus-jobs?order_by=date',
        'https://remoteok.com/remote-sql-jobs?order_by=date'          
]

dados = []  # Lista para armazenar os dados coletados

for lang, url in zip(langs, urls): # Iterando sobre as linguagens e URLs (zip cria pares)
    print(f"Coletando dados para {lang}...")
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        PAUSE_TIME = 3
        time.sleep(PAUSE_TIME)

        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Rola até o final
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Espera carregar
            time.sleep(PAUSE_TIME)

            # Verifica nova altura
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # Se a altura não mudou, chegamos ao final
            if new_height == last_height:
                print(f"Chegou ao final da página para {lang}.")
                break
            last_height = new_height

        # Coleta os elementos de tempo
        time_elements = driver.find_elements(By.TAG_NAME, 'time')
        datetimes = [el.get_attribute('datetime') for el in time_elements]

        # Fecha o navegador
        driver.quit() 
    
        print(f"Salvando dados para {lang}...")
        
        # Cria um DataFrame com coluna lang e date
        for dt in datetimes:
            dados.append({'lang': lang, 'datetime': dt})
        df = pd.DataFrame(dados, columns=['lang', 'datetime'])      


print("Todos os dados foram coletados e salvos.")
df.to_csv(f'datas.csv', index=False, encoding='utf-8')



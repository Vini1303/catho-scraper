from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template, request, jsonify, send_file
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify
from flask_cors import CORS


chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")  # Recomendado para containers
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Backend funcionando!"

@app.route('/test')
def test():
    return jsonify({"status": "success", "message": "Teste bem-sucedido"})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
import subprocess
import os
import threading
import time
import pandas as pd
import re

EMAIL = 'fernanda.fontes@plataformahubbie.com.br'
SENHA = 'Hubbie2901!'
URL_LOGIN = 'https://www.catho.com.br/area-recrutador-v2/'

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(URL_LOGIN)
time.sleep(4)

# Login
driver.find_element(By.NAME, 'email').send_keys(EMAIL)
driver.find_element(By.NAME, 'password').send_keys(SENHA)
time.sleep(4)
driver.find_element(By.TAG_NAME, 'button').click()
time.sleep(2)

# Vai para candidaturas
driver.get("https://www.catho.com.br/curriculos/busca/?q=Vendedor&pais_id=31&estado_id[25]=25&regiaoId[14]=14&cidade_id[314]=314&zona_id[-1]=-1&page=1&onde_buscar=todo_curriculo&como_buscar=todas_palavras&tipoBusca=busca_palavra_chave")
time.sleep(2)

# Cria a planilha
df = pd.DataFrame(columns=["Nome", "Idade", "Bairro", "Pretensão", "Telefone", "Experiências", "Currículo"])

def coletar_telefone(candidato):
    try:
        # Localiza o botão "Ver telefone" dentro do candidato específico
        botao_telefone = candidato.find_element(
            By.XPATH, ".//button[.//*[local-name()='svg' and @data-testid='SmartphoneIcon']]")
        
        # Rola até o botão e clica
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_telefone)
        botao_telefone.click()
        time.sleep(2)  # Aguarda o popup aparecer
        html = candidato.get_attribute('innerHTML')
        reg = re.compile(r'\(\d{2}\) \d{4,5}-\d{4}')
        match = reg.findall(html)

        telefone = "; ".join(match) if match else ""
        return telefone
    except Exception as e:
        print(f"Erro ao coletar telefone: {str(e)}")
        return ""

while True:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.Card__CardWrapper-sc-om5cci-0"))
    )
    candidatos = driver.find_elements(By.CSS_SELECTOR, "article.Card__CardWrapper-sc-om5cci-0")
    print(f"Encontrados {len(candidatos)} candidatos nesta página.")

    for candidato in candidatos:
        # Coleta o telefone primeiro
        telefone = coletar_telefone(candidato)
        
        # Nome
        try:
            nome = candidato.find_element(By.CSS_SELECTOR, "h2 a b.gtm-class").text
        except Exception as e:
            nome = ""
            print("Erro ao pegar nome:", e)
        
        # Idade, estado, cidade
        try:
            try:
                info = candidato.find_element(By.CSS_SELECTOR, "p.sc-eZkCL").text.split(", ")
                if len(info) < 3:
                    continue
                else:
                    idade, bairro = info[0].split(" ")[0], info[2].split(" - ")[1]
            except Exception as e:
                info = candidato.find_element(By.CSS_SELECTOR, "p.sc-dCFHLb").text.split(", ")
                if len(info) < 3:
                    continue
                else:
                    idade, bairro = info[0].split(" ")[0], info[2].split(" - ")[1]
        except Exception as e:
            info = []
            bairro, idade = "", ""
            print("Erro ao pegar info:", e)
        
        # Filtra por idade
        try:
            idade_num = int(''.join(filter(str.isdigit, idade)))
            if idade_num < 18 or idade_num > 43:
                print(f"Idade fora do intervalo: {idade_num} anos. Ignorando candidato {nome}.")
                continue
        except Exception as e:
            print("Erro ao converter idade:", e)
            continue
        
        # Pretensão salarial
        try:
            try:
                pretensao = candidato.find_element(By.CSS_SELECTOR, "p.sc-bypJrT strong").text
            except:
                pretensao = candidato.find_element(By.CSS_SELECTOR, "p.sc-iHGNWf strong").text
        except Exception as e:
            pretensao = ""
            print("Erro ao pegar pretensão:", e)
        
        # Experiências
        experiencias = []
        try:
            exp_blocks = candidato.find_elements(By.CSS_SELECTOR, "div.sc-kdBSHD p.sc-lcIPJg")
            for exp in exp_blocks:
                cargo = exp.find_element(By.CSS_SELECTOR, "h3").text
                tempo = exp.find_elements(By.CSS_SELECTOR, "span")
                tempo_texto = " ".join([t.text.strip() for t in tempo])
                experiencias.append(f"{cargo} {tempo_texto}")
        except Exception as e:
            print("Erro ao pegar experiências:", e)

        curriculo = ""
        original_window = driver.current_window_handle
        try:
            but = None
            try:
                but = candidato.find_element(
                    By.CSS_SELECTOR, "svg.sc-eoVZPG.igYwyZ")
            except:
                but = candidato.find_element(
                    By.CSS_SELECTOR, "svg.sc-kCMKrZ.jKJtUC")
            but.click()
            time.sleep(2)

            driver.switch_to.window(driver.window_handles[-1])
            curriculo = driver.current_url
            driver.close()

            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print("Erro ao pegar botão de currículo:", e)

        print(f"Salvando: {nome}, {idade}, {bairro}, {pretensao}, {telefone}, {experiencias}, {curriculo}")
        df = pd.concat([df, pd.DataFrame([{
            "Nome": nome,
            "Idade": idade,
            "Bairro": bairro,
            "Pretensão": pretensao,
            "Telefone": telefone,
            "Experiências": "\n".join(experiencias),
            "Currículo": curriculo
        }])], ignore_index=True)
        df.to_csv("candidatos.csv", index=False)
        df.to_excel("candidatos.xlsx", index=False)

    # Tenta clicar no botão "Próxima"
    try:
        botao_proxima = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Próxima' and not(@aria-disabled='true')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", botao_proxima)
        botao_proxima.click()
        time.sleep(3)
    except Exception as e:
        print("Não encontrou botão próxima ou erro:", e)
        break

df.to_csv("candidatos.csv", index=False)
df.to_excel("candidatos.xlsx", index=False)
print("Planilha final salva com sucesso!")
driver.quit()
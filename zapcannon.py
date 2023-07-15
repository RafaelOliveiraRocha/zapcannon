from flask import Flask, render_template, request, send_file, send_from_directory
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import urllib.parse
import os
import csv

app = Flask(__name__, template_folder=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates'))


# Configura o caminho completo para o executável do geckodriver
executable_path = "/home/rocha/Área de Trabalho/geckodriver-v0.32.0-linux64/geckodriver"


class WhatsAppBot:
    def __init__(self):
        # Configura o driver do Selenium
        service = Service(executable_path=executable_path)
        self.driver = webdriver.Firefox(service=service)

    def conectar_whatsapp_web(self):
        driver = self.driver
        driver.get("https://web.whatsapp.com/")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "side")))

    def enviar_mensagens(self, csv_file, mensagem):
        driver = self.driver
        df = pd.read_csv(csv_file)

        # Verifica se a coluna "Status" já existe
        if "Status" not in df.columns:
            # Adiciona a coluna "Status" ao DataFrame
            df["Status"] = ""

        # Cria uma cópia do DataFrame original
        df_copy = df.copy()

        # Envia a mensagem para cada número de telefone na planilha
        total_tentativas = len(df)
        envios_bem_sucedidos = 0
        erros = 0
        for i in range(total_tentativas):
            try:
                nome = df.loc[i, "Nome"]
                numero = df.loc[i, "Número"]
                if pd.isna(nome):
                    texto = mensagem
                else:
                    texto = f"{nome}\n{mensagem}"
                link = f"https://web.whatsapp.com/send?phone={numero}&text={urllib.parse.quote(texto)}"
                driver.get(link)
                sleep(2)
                btn_enviar = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
                try:
                    driver.execute_script("arguments[0].click();", btn_enviar)
                    sleep(6)
                    envios_bem_sucedidos += 1
                    # Atualiza o status na cópia do DataFrame
                    df_copy.loc[i, "Status"] = 'Enviada'
                except NoSuchElementException:
                    pass
                    return NoSuchElementException
            except:
                erros += 1
                df_copy.loc[i, "Status"] = 'Falha'
                pass

        # Salva a planilha atualizada com a coluna "Status" no arquivo original
        csv_filename = os.path.basename(csv_file.filename)
        updated_csv_file = os.path.join('uploads', csv_filename)
        df_copy.to_csv(updated_csv_file, index=False)

        # Fecha a janela do WhatsApp Web
        driver.quit()

        return {
            'total_tentativas': total_tentativas,
            'envios_bem_sucedidos': envios_bem_sucedidos,
            'erros': erros,
            'filename': csv_filename
        }


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('zapcannon', path)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/templates/instrucoes.html')
def instrucoes():
    return render_template('instrucoes.html')


@app.route('/templates/comece_agora.html')
def comece_agora():
    return render_template('comece_agora.html')


@app.route('/enviar_mensagens', methods=['POST'])
def enviar_mensagens():
    # Obtém o arquivo CSV enviado pelo usuário
    csv_file = request.files['csv_file']
    # Obtém a mensagem digitada no formulário
    mensagem = request.form['mensagem']

    # Inicializa o WhatsAppBot
    bot = WhatsAppBot()

    # Conecta ao WhatsApp Web
    bot.conectar_whatsapp_web()

    # Envia as mensagens e retorna o resultado
    resultado = bot.enviar_mensagens(csv_file, mensagem)

    return render_template('result.html', resultado=resultado)


@app.route('/')
def result():
    return render_template('result.html')


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Obter o caminho completo para o diretório "uploads"
    upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    # Obter o caminho completo para o arquivo
    file_path = os.path.join(upload_dir, filename)

    # Verificar se o arquivo existe
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Arquivo não encontrado"


if __name__ == '__main__':
    app.run()

import numpy as np
import websocket
import time
import json
from datetime import datetime, timedelta
from regressao import LinearRegression
from msgTelegram import *
from funcoes import *
from preco_moeda import *


regressor = LinearRegression()
y_vals = []
intervalo_previsao = timedelta(minutes=10)
ultima_impressao = datetime.now()
token = '6037164173:AAFWH_Ojc434tGzrkHoZtKIz5FJn_szEOe8'
cont = 0
chat_id = last_chat_id(token)
y2 = 0
y1 = 0
preco_atual = 0
acerto = 0
erro = 0
tendencia = 0
validador = True



def adicionar_valor(y):
    global  ultima_impressao, cont, chat_id, token, y2, y1, preco_atual, tendencia, acerto, erro, validador
    y_vals.append(y)
    x = np.arange(1, len(y_vals) + 1).reshape(-1, 1)
    regressor.fit(x, y_vals)
    proximo_x = len(y_vals) + (intervalo_previsao / timedelta(minutes=5))
    tempo = datetime.now() - ultima_impressao
    print(f"Tempo desde a última impressão: {tempo}")
    print(f"valor contador: {cont}")
    print(f"valor y = {y}")
    print(f"valor y2 = {y2}")
    print(f"valor y1 = {y1}")
    print(f"valor regressor.coef_ = {regressor.coef_}")
    print(f"valor preco_atual = {preco_atual}")
    print(f"valor validador = {validador}")
    print(f"valor tendencia = {tendencia}")
    print(f"valor acerto = {acerto}")
    print(f"valor erro = {erro}")

    if cont == 1:
        preco_atual = y
    time.sleep(10)

    if datetime.now() - ultima_impressao >= intervalo_previsao:
        previsao2 = regressor.predict([[proximo_x]])[0]
        print(f"Previsão para daqui a 10 minutos: {previsao2}")
        if tendencia != 0:  
            validador = taxa_acerto(y, preco_atual, tendencia)        
        if  regressor.coef_ > 0:
            print("Tendência de alta, pode ser uma boa hora para comprar")
            preco_atual = y
            tendencia = 1
            send_message(token, chat_id, 'Lembrando (moeda: EUR/USD) Previsões  de 10 minutos Tendência de alta, pode ser uma boa hora para comprar')   
        else:
            print("Tendência de baixa, pode ser melhor vender")
            preco_atual = y
            tendencia = 2
            send_message(token, chat_id, 'Lembrando (moeda: EUR/USD) Previsões  de 10 minutos : Tendência de Baixa, pode ser uma boa hora para vender')

        if validador == True:
            print("Acertou")
            acerto = acerto + 1
            send_message(token, chat_id, 'Lembrando (moeda: EUR/USD) Previsões  de 10 minutos : Acertou')
        else:
            print("Errou")
            erro = erro + 1
            send_message(token, chat_id, 'Lembrando (moeda: EUR/USD) Previsões  de 10 minutos : Errou')        
        ultima_impressao = datetime.now()
        cont = cont + 1        
        porcentagem = (acerto / cont) * 100
        print(f"Porcentagem de acerto: {porcentagem}")
        send_message(token, chat_id, f'Lembrando (moeda: EUR/USD) Previsões  de 10 minutos : Porcentagem de acerto: {porcentagem}')
     


        


def on_message(ws, message):
    data = json.loads(message)
    price = data['tick']['quote']
    adicionar_valor(price)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Conexão fechada")

def on_open(ws):
    print("Conexão aberta")
    subscribe_message = valor_R_50()   
    ws.send(json.dumps(subscribe_message))

if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.binaryws.com/websockets/v3?app_id=1089", on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()
    proxima_atualizacao = datetime.now() + intervalo_previsao
    while True:
        tempo_restante = proxima_atualizacao - datetime.now()
        if tempo_restante.total_seconds() > 0:
            time.sleep(tempo_restante.total_seconds())
        proxima_atualizacao += intervalo_previsao
       
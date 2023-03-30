import numpy as np
import websocket
import json
import time
from datetime import datetime, timedelta
from regressao import LinearRegression
from msgTelegram import *



# Instanciar objeto de regressão linear
regressor = LinearRegression()

# Lista para armazenar valores de y
y_vals = []

# Definir intervalo de tempo entre as previsões
intervalo_previsao = timedelta(minutes=10)
ultima_impressao = datetime.now()

# Variáveis para o cálculo da taxa de acerto
token = '6037164173:AAFWH_Ojc434tGzrkHoZtKIz5FJn_szEOe8'
acertos_compra = 0
erros_compra = 0
acertos_venda = 0
erros_venda = 0
cont = 0
cont2 = 0
chat_id = last_chat_id(token)
y2 = 0
#mensagem = "Tendência de alta, pode ser uma boa hora para comprar"
#mensagem2 = "Tendência de baixa, pode ser uma boa hora para vender"


# Armazenar o preço anterior
preco_anterior = None


def adicionar_valor(y):
    global acertos_compra, erros_compra, acertos_venda, erros_venda, ultima_impressao, cont, chat_id, token, cont2, y2
    y_vals.append(y)

    # Gerar novo valor de x a partir do comprimento da lista de valores de y
    x = np.arange(1, len(y_vals) + 1).reshape(-1, 1)

    # Treinar modelo de regressão linear com os novos valores de x e y
    regressor.fit(x, y_vals)

    # Calcular previsão para daqui a 10 minutos
    proximo_x = len(y_vals) + (intervalo_previsao / timedelta(minutes=5))
    #previsao = regressor.predict([[proximo_x]])[0] 
    #print(f"Última impressão: {ultima_impressao}")
    #print(f"Valor do y: {y}")
    tempo = datetime.now() - ultima_impressao
    print(f"Tempo desde a última impressão: {tempo}")
    #print(f"proximo_x: {proximo_x}")
    cont2 = cont2 + 1
    print(f"valor contador: {cont}")
    print(f"valor contador2: {cont2}")
    print(f"valor y = {y}")
    print(f"valor y2 = {y2}")
    #print(f"valor y = {y}")
    #send_message(token, chat_id, 'teste')
    
    #send_message = (token,-961226810, 'Tendência de alta, pode ser uma boa hora para comprar')
   

    # Definir estratégia simples de compra e venda
    if datetime.now() - ultima_impressao >= intervalo_previsao:
        previsao2 = regressor.predict([[proximo_x]])[0]
        print(f"Previsão para daqui a 10 minutos: {previsao2}")
        y1 = y_vals[cont2]
        #cont = cont + 1     
        #print(f"Valor da previsão: {previsao}")
        if  regressor.coef_ > 0:
            print("Tendência de alta, pode ser uma boa hora para comprar")
            send_message(token, chat_id, 'Lembrando (moeda: EUR/USD) Previsões  de 10 minutos Tendência de alta, pode ser uma boa hora para comprar')
                #send_message = ('6037164173:AAFWH_Ojc434tGzrkHoZtKIz5FJn_szEOe8',-925570433, 'Tendência de alta, pode ser uma boa hora para comprar')
            if y2 < y1:
                acertos_compra += 1
                send_message(token, chat_id, 'Acertou a tendencia de alta')
            else:
                erros_compra += 1
                send_message(token, chat_id, 'Errou a tendencia de alta')
        else:
            print("Tendência de baixa, pode ser melhor vender")
            send_message(token, chat_id, 'Lembrando (moeda: EUR/USD) Previsões  de 10 minutos : Tendência de Baixa, pode ser uma boa hora para vender')
                #send_message = ('6037164173:AAFWH_Ojc434tGzrkHoZtKIz5FJn_szEOe8',-925570433, 'Tendência de Baixa, pode ser uma boa hora para comprar')
            if y2 > y1:
                acertos_venda += 1
                send_message(token, chat_id, 'Acertou a tendencia de baixa')
            else:
                erros_venda += 1
                send_message(token, chat_id, 'Errou a tendencia de baixa')

        y2 = y_vals[-cont2]
        ultima_impressao = datetime.now()
        cont = cont + 1

        # Calcular taxa de acerto
        if cont > 1:
            taxa_acerto_compra = (acertos_compra + acertos_venda)/cont * 100
            print(f"Taxa de acerto para compra: {taxa_acerto_compra}%")
            send_message(token, chat_id, f"Taxa de acerto (Em teste, não verdadeira): {taxa_acerto_compra}%")

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
    subscribe_message = {
        "ticks": "frxEURUSD",
        "subscribe": 1
    }
    ws.send(json.dumps(subscribe_message))

if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.binaryws.com/websockets/v3?app_id=1089", on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

    # Loop para aguardar 10 minutos e gerar nova previsão
    proxima_atualizacao = datetime.now() + intervalo_previsao
    while True:
        # Aguardar até a próxima atualização
        tempo_restante = proxima_atualizacao - datetime.now()
        if tempo_restante.total_seconds() > 0:
            time.sleep(tempo_restante.total_seconds())

        # Atualizar a variável de próxima atualização
        proxima_atualizacao += intervalo_previsao
        #cont2 = cont2 + 1

        # Gerar nova previsão e calcular taxa de acerto
        #adicionar_valor(0)
        #taxa_acerto = acertos / (acertos + erros) * 100
        #print(f"Taxa de acerto: {taxa_acerto}%")
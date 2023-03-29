import numpy as np
import websocket
import json
import time
from datetime import datetime, timedelta
from regressao import LinearRegression

# Instanciar objeto de regressão linear
regressor = LinearRegression()

# Lista para armazenar valores de y
y_vals = []

# Definir intervalo de tempo entre as previsões
intervalo_previsao = timedelta(minutes=10)
ultima_impressao = datetime.now()


# Variáveis para o cálculo da taxa de acerto
acertos = 0
erros = 0

def adicionar_valor(y):
    global acertos, erros, ultima_impressao
    y_vals.append(y)

    # Gerar novo valor de x a partir do comprimento da lista de valores de y
    x = np.arange(1, len(y_vals) + 1).reshape(-1, 1)

    # Treinar modelo de regressão linear com os novos valores de x e y
    regressor.fit(x, y_vals)

    # Calcular previsão para daqui a 10 minutos
    proximo_x = len(y_vals) + (intervalo_previsao / timedelta(minutes=5))
    previsao = regressor.predict([[proximo_x]])[0]
    print(f"Previsão para daqui a 10 minutos: {previsao}")
    print(f"ulima impressao: {ultima_impressao}")
    valor = datetime.now() - ultima_impressao
    print(f"valor: {valor}")

    # Definir estratégia simples de compra e venda
    if datetime.now() - ultima_impressao >= intervalo_previsao:
        if regressor.coef_ > 0:
            print("Tendência de alta, pode ser uma boa hora para comprar")
            if y < previsao:
                #global acertos
                acertos += 1
                print("Acerto!")
            else:
                #global erros
                erros += 1
                print("Erro!")
        else:
            print("Tendência de baixa, pode ser melhor vender")
            if y > previsao:
                #global acertos
                acertos += 1
                print("Acerto!")
            else:
                #global erros
                erros += 1
                print("Erro!")

            ultima_impressao = datetime.now()

        # Calcular taxa de acerto
        taxa_acerto = acertos / (acertos + erros) * 100
        print(f"Taxa de acerto: {taxa_acerto}%")

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

        # Gerar nova previsão e calcular taxa de acerto
        #adicionar_valor(0)
        #taxa_acerto = acertos / (acertos + erros) * 100
        #print(f"Taxa de acerto: {taxa_acerto}%")
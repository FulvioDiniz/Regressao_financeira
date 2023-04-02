import requests
#from main import *


#message = 'Lucro dia/ 36 win / 17 loss == 118'
# mostra o id do último grupo adicionado
def last_chat_id(token):
    try:
        url = "https://api.telegram.org/bot{}/getUpdates".format(token)
        response = requests.get(url)
        if response.status_code == 200:
            json_msg = response.json()
            for json_result in reversed(json_msg['result']):
                message_keys = json_result['message'].keys()
                if ('new_chat_member' in message_keys) or ('group_chat_created' in message_keys):
                    return json_result['message']['chat']['id']
            print('Nenhum grupo encontrado')
        else:
            print('A resposta falhou, código de status: {}'.format(response.status_code))
    except Exception as e:
        print("Erro no getUpdates:", e)

# enviar mensagens utilizando o bot para um chat específico
def send_message(token, chat_id, message):
    try:
        data = {"chat_id": chat_id, "text": message}
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(url, data)
    except Exception as e:
        print("Erro no sendMessage:", e)
# token único utilizado para manipular o bot (não deve ser compartilhado)
# exemplo: '1413778757:AAFxmr611LssAHbZn1uqV_NKFsbwK3TT-wc'
token = '6037164173:AAFWH_Ojc434tGzrkHoZtKIz5FJn_szEOe8'

# id do chat que será enviado as mensagens
chat_id = last_chat_id(token)

#print("Id do chat:", chat_id)
# exemplo de mensagem



# enviar a mensagem
#send_message(token, chat_id, message)
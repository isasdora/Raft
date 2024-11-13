import sys
import requests

#função para redirecionar mensagens para o servidor líder
def redirecionarLider(endereco_servidor, message):
    tipo = message["tipo"]
    #ate alguem falar q é líder
    while True:
        if tipo == "get":
            try:
                res = requests.get(endereco_servidor, json=message, timeout=1)
            except Exception as e:
                return e
        else:
            try:
                res = requests.put(endereco_servidor, json=message, timeout=1)
            except Exception as e:
                return e
        
        #caso a resposta seja válida redireciona para o líder
        if res.status_code == 200 and "payload" in res.json():
            payload = res.json()["payload"]
            if "message" in payload:
                endereco_servidor = payload["message"] + "/request"
            else:
                break
        else:
                break
    return res.json()


#armazenar chave-valor
def put(endereco, key, value):
    endereco_servidor = endereco + "/request"
    payload = {'key': key, 'value': value}
    message = {"tipo": "put", "payload": payload}
    print(redirecionarLider(endereco_servidor, message))

#retorna a chave-valor mas se o servidor não for o líder redireciona até encontrar o líder
def get(endereco, key):
    endereco_servidor = endereco + "/request"
    payload = {'key': key}
    message = {"tipo": "get", "payload": payload}
    print(redirecionarLider(endereco_servidor, message))

if __name__ == "__main__":
    if len(sys.argv) == 3:  #se o número de argumentos for 3 a função get será chamada
        endereco = sys.argv[1]  #endereço do servidor
        key = sys.argv[2]   #chave key
        get(endereco, key)
    elif len(sys.argv) == 4:  #se o número de argumentos for 4, a função put será chamada
        endereco = sys.argv[1]  #endereço do servidor
        key = sys.argv[2]   #chave key
        val = sys.argv[3]   #valor value
        put(endereco, key, val)
    else:
        #se os parâmetros fornecidos forem inválidos exibe o formato correto
        print("Formato incorreto.")
        print("Como usar: python client.py endereco 'key' 'value'  # Para PUT")
        print("Como usar: python client.py endereco 'key'  # Para GET")
        print("Formato de endereço: http://ip:porta")
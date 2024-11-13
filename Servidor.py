from node import Node
from node import SEGUIDOR, LIDER  # Usando os termos SEGUIDOR e LIDER
from flask import Flask, request, jsonify
import sys
import logging

app = Flask(__name__)

@app.route("/request", methods=['GET'])
def pegar_valor():
    payload = request.get_json().get("payload", {})
    resposta = {"codigo": 'falhou', 'payload': payload}
    
    if n.status == LIDER:
        resultado = n.tratar_get(payload)
        if resultado:
            resposta = {"codigo": "sucesso", "payload": resultado}
    elif n.status == SEGUIDOR:
        resposta["payload"]["message"] = n.lider
    return jsonify(resposta)

@app.route("/request", methods=['POST'])
def mandar_valor():
    payload = request.get_json().get("payload", {})
    resposta = {"codigo": "falha"}
    
    if n.status == LIDER:
        resultado = n.tratar_put(payload)
        if resultado:
            resposta = {"codigo": "sucesso"}
    elif n.status == SEGUIDOR:
        payload["message"] = n.lider
        resposta["payload"] = payload
    return jsonify(resposta)

@app.route("/votar", methods=['POST'])
def votar():
    termo = request.json.get("termo")
    indice_compromisso = request.json.get("indice_compromisso")
    staged = request.json.get("staged")
    
    escolha, termo = n.decidir_voto(termo, indice_compromisso, staged)
    mensagem = {"escolha": escolha, "termo": termo}
    return jsonify(mensagem)

@app.route("/batidas", methods=['POST'])
def batidas():
    termo, indice_compromisso = n.seguidor_batida(request.json)
    mensagem = {"termo": termo, "indice_compromisso": indice_compromisso}
    return jsonify(mensagem)

# Desativar log do Flask
log = logging.getLogger('werkzeug')
log.disabled = True

if __name__ == "__main__":
    # python servidor.py index
    if len(sys.argv) == 2:
        index = int(sys.argv[1])  # O índice do IP atual
        Lista_IP_file = "Lista_IP.txt"  # Nome fixo do arquivo de IPs
        Lista_IP = []
        
        # Abre o arquivo de IPs e carrega todos os IPs
        with open(Lista_IP_file) as f:
            for ip in f:
                Lista_IP.append(ip.strip())
        
        # Retira o IP do nó atual da lista usando o índice fornecido
        my_ip = Lista_IP.pop(index)
        http, host, port = my_ip.split(':')

        # Exibe uma mensagem indicando o nó atual
        print(f"Nó {index} ativo:  endereco IP = {my_ip}")
        
        # Inicializa o nó com a lista de IPs restantes e o IP do próprio nó
        n = Node(Lista_IP, my_ip)

        print(f"Iniciando nó em {host}:{port}")
        
        # Inicia o servidor Flask
        app.run(host="0.0.0.0", port=int(port), debug=False)
    else:
        print("Uso: python servidor.py <index>")



from flask import Flask, request, jsonify
import sys
import time
import logging

app = Flask(__name__)

# Desativar o log do Flask (werkzeug)
log = logging.getLogger('werkzeug')
log.disabled = True

# Variáveis de estado do nó
termo_atual = 0
votar_em = None
logs = []  # Armazenamento simples para logs replicados
ultima_batida = time.time()  # Tempo do último heartbeat recebido
lider_atual = None  # Variável para armazenar o líder atual

# Rota para envio de batidas do líder (heartbeat)
@app.route('/batidas', methods=['POST'])
def batidas():
    global termo_atual, ultima_batida
    termo = request.json.get("termo")
    
    print(f"[Recebido /batidas] Termo recebido: {termo}")

    # Atualiza o termo atual e o tempo do último heartbeat recebido
    if termo >= termo_atual:
        termo_atual = termo
        ultima_batida = time.time()  # Atualiza o tempo do último heartbeat
        print(f"[Processado /batidas] Batida de vida recebida. Termo atualizado para {termo_atual}")
        return jsonify({"status": "Batida de vida recebida", "termo": termo_atual}), 200
    else:
        print("[Erro /batidas] Termo inválido")
        return jsonify({"status": "Erro: termo inválido"}), 400

# Rota para votação na eleição de líder
@app.route('/eleicao', methods=['POST'])
def eleicao():
    global termo_atual, votar_em, lider_atual
    termo = request.json.get('termo')
    id_candidato = request.json.get("id_candidato")
    
    print(f"[Recebido /eleicao] Termo: {termo}, ID do candidato: {id_candidato}")

    if termo > termo_atual:
        termo_atual = termo
        votar_em = id_candidato
        lider_atual = id_candidato  # Atualiza o líder atual
        print(f"[Processado /eleicao] Voto atribuído ao candidato {id_candidato} no termo {termo_atual}")
        print(f"Líder atual: {lider_atual}")
        return jsonify({"atribuir_voto": True, "termo": termo_atual, "lider": lider_atual})
    elif termo == termo_atual and (votar_em is None or votar_em == id_candidato):
        votar_em = id_candidato
        lider_atual = id_candidato  # Atualiza o líder atual
        print(f"[Processado /eleicao] Voto atribuído ao candidato {id_candidato} no termo {termo_atual}")
        print(f"Líder atual: {lider_atual}")
        return jsonify({"atribuir_voto": True, "termo": termo_atual, "lider": lider_atual})
    else:
        print(f"[Processado /eleicao] Voto não atribuído. Termo atual: {termo_atual}")
        print(f"Líder atual: {lider_atual}")
        return jsonify({"atribuir_voto": False, "termo": termo_atual, "lider": lider_atual})

# Rota para gerenciamento de termos de eleição
@app.route('/gerenciar_termo', methods=['GET', 'POST'])
def gerenciar_termo():
    global termo_atual

    if request.method == 'GET':
        print("[Recebido /gerenciar_termo] GET - Retornando termo atual")
        return jsonify({"termo_atual": termo_atual})

    elif request.method == 'POST':
        novo_termo = request.json.get("novo_termo")
        print(f"[Recebido /gerenciar_termo] POST - Novo termo: {novo_termo}")

        if novo_termo is not None and novo_termo > termo_atual:
            termo_atual = novo_termo
            print(f"[Processado /gerenciar_termo] Termo atualizado para {termo_atual}")
            return jsonify({"status": "Termo atualizado", "termo_atual": termo_atual})
        else:
            print("[Erro /gerenciar_termo] Nenhuma atualização realizada")
            return jsonify({"status": "Nenhuma atualização realizada", "termo_atual": termo_atual}), 400

# Rota para replicação de logs
@app.route('/replicar_log', methods=['POST'])
def replicar_log():
    log_entry = request.json.get("log_entry")
    termo = request.json.get("termo")
    index = len(logs) + 1  # Índice do novo log, adicionando ao final da lista

    print(f"[Recebido /replicar_log] Log entry: {log_entry}, Termo: {termo}")

    # Armazena o log com o termo e índice
    if log_entry and termo is not None:
        logs.append({"index": index, "termo": termo, "log_entry": log_entry})
        print(f"[Processado /replicar_log] Log replicado com sucesso no índice {index}")
        return jsonify({"status": "Log replicado com sucesso", "index": index, "termo": termo}), 200
    else:
        print("[Erro /replicar_log] Dados incompletos para replicação do log")
        return jsonify({"status": "Erro ao replicar log: dados incompletos"}), 400

# Função para verificar timeout de heartbeat
def verificar_timeout():
    global ultima_batida
    tempo_atual = time.time()
    timeout_limite = 5  # Timeout de 5 segundos para o exemplo

    if tempo_atual - ultima_batida > timeout_limite:
        print("Timeout: Nenhum sinal de vida recebido do líder.")
        # Aqui, o nó poderia iniciar uma nova eleição, por exemplo

if __name__ == "__main__":
    if len(sys.argv) == 2:
        index = int(sys.argv[1])
        nodes = []

        # Lê o arquivo com a lista de nós e IPs
        with open('Lista_IP.txt') as f:
            for line in f:
                name, ip = line.strip().split()
                nodes.append((name, ip))

        # Seleciona o nome e o IP do nó pelo índice
        node_name, uso_ip = nodes[index]
        host, port = uso_ip.replace("http://", "").split(':')

        print(f"Iniciando {node_name} em {host}:{port}")

        # Inicia o servidor Flask com o IP e a porta especificados
        app.run(host=host, port=int(port), debug=False)
    else:
        print("Uso: python servidor.py <index>")

import threading
import time
import utils
from config import cfg

SEGUIDOR = 0
CANDIDATO = 1
LIDER = 2


class Node():
    def __init__(self, colegas, meu_ip):
        self.endereco = meu_ip #ok
        self.colegas = colegas  #ok
        self.bloqueio = threading.Lock() #ok
        self.BD = {} #ok
        self.registro = [] #ok
        self.em_espera = None #ok
        self.termo = 0 #ok
        self.status = SEGUIDOR #ok
        self.maioria = ((len(self.colegas) + 1) // 2) + 1 #ok
        self.contagem_votos = 0 #ok
        self.indice_compromisso = 0 #ok
        self.thread_timeout = None #ok
        self.iniciar_timeout()

    #Simulação de Falhas e Recuperação - Isadora
    def iniciar_timeout(self):
        self.reiniciar_timeout()
        if self.thread_timeout and self.thread_timeout.is_alive():
            return
        self.thread_timeout = threading.Thread(target=self.loop_timeout)
        self.thread_timeout.start()

    def reiniciar_timeout(self):
        self.tempo_eleicao = time.time() + utils.timeout_aleatorio()

    def loop_timeout(self):
        while self.status != LIDER:
            delta = self.tempo_eleicao - time.time()
            if delta < 0:
                self.iniciarEleicao()
            else:
                time.sleep(delta)

    #Eleição de líder - Clesio
    def iniciarEleicao(self):
        self.termo += 1
        self.contagem_votos = 0
        self.status = CANDIDATO
        self.iniciar_timeout()
        self.incrementarVoto()
        self.enviar_solicitacao_voto()

    #Eleição de líder - Clesio
    def incrementarVoto(self):
        self.contagem_votos += 1
        if self.contagem_votos >= self.maioria:
            print(f"{self.endereco} se torna o líder do termo {self.termo}")
            self.status = LIDER
            self.iniciarHeartbeat()

    #Replicação de Logs - Kaio
    def enviar_solicitacao_voto(self):
        for eleitor in self.colegas:
            threading.Thread(target=self.solicitar_voto,
                             args=(eleitor, self.termo)).start()

    #Gerenciamento de Termos de Eleição - Gabriela
    def solicitar_voto(self, eleitor, termo):
        mensagem = {
            "termo": termo,
            "indice_compromisso": self.indice_compromisso,
            "em_espera": self.em_espera
        }
        rota = "votar"
        while self.status == CANDIDATO and self.termo == termo:
            resposta = utils.enviar(eleitor, rota, mensagem)
            if resposta:
                escolha = resposta.json()["escolha"]
                if escolha and self.status == CANDIDATO:
                    self.incrementarVoto()
                elif not escolha:
                    termo = resposta.json()["termo"]
                    if termo > self.termo:
                        self.termo = termo
                        self.status = SEGUIDOR
                break

    #Eleição de líder - Clesio
    def decidir_voto(self, termo, indice_compromisso, em_espera):
        if self.termo < termo and self.indice_compromisso <= indice_compromisso and (
                em_espera or (self.em_espera == em_espera)):
            self.reiniciar_timeout()
            self.termo = termo
            return True, self.termo
        else:
            return False, self.termo

    def iniciarHeartbeat(self):
        print("Iniciando HEARTBEAT")
        if self.em_espera:
            self.tratar_put(self.em_espera)

        for colega in self.colegas:
            t = threading.Thread(target=self.enviar_heartbeat, args=(colega,))
            t.start()

    #Gerenciamento de Termos de Eleição - Gabriela
    def enviar_heartbeat(self, follower):
        if self.registro:
            self.atualizar_indice_compromisso_follower(follower)

        rota = "heartbeat"
        mensagem = {"termo": self.termo, "endereco": self.endereco}
        while self.status == LIDER:
            inicio = time.time()
            resposta = utils.enviar(follower, rota, mensagem)
            if resposta:
                self.tratar_resposta_heartbeat(resposta.json()["termo"],
                                               resposta.json()["indice_compromisso"])
            delta = time.time() - inicio
            time.sleep((cfg.HB_TIME - delta) / 1000)

    #Gerenciamento de Termos de Eleição - Gabriela
    def tratar_resposta_heartbeat(self, termo, indice_compromisso):
        if termo > self.termo:
            self.termo = termo
            self.status = SEGUIDOR
            self.iniciar_timeout()

    #Gerenciamento de Termos de Eleição - Gabriela
    def seguidor_batida(self, msg):
        termo = msg["termo"]
        if self.termo <= termo:
            self.lider = msg["endereco"]
            self.reiniciar_timeout()
            if self.status == CANDIDATO:
                self.status = SEGUIDOR
            elif self.status == LIDER:
                self.status = SEGUIDOR
                self.iniciar_timeout()
            if self.termo < termo:
                self.termo = termo

            if "acao" in msg:
                acao = msg["acao"]
                if acao == "registro":
                    payload = msg["payload"]
                    self.em_espera = payload
                elif self.indice_compromisso <= msg["indice_compromisso"]:
                    if not self.em_espera:
                        self.em_espera = msg["payload"]
                    self.commit()

        return self.termo, self.indice_compromisso

    #Gerenciamento de Termos de Eleição - Gabriela
    def atualizar_indice_compromisso_follower(self, follower):
        rota = "heartbeat"
        primeira_mensagem = {"termo": self.termo, "endereco": self.endereco}
        segunda_mensagem = {
            "termo": self.termo,
            "endereco": self.endereco,
            "acao": "compromisso",
            "payload": self.registro[-1]
        }
        resposta = utils.enviar(follower, rota, primeira_mensagem)
        if resposta and resposta.json()["indice_compromisso"] < self.indice_compromisso:
            resposta = utils.enviar(follower, rota, segunda_mensagem)

    #Kaio servidor
    def tratar_get(self, payload):
        print("obtendo", payload)
        chave = payload["key"]
        if chave in self.BD:
            payload["value"] = self.BD[chave]
            return payload
        else:
            return None

    #Kaio servidor
    def tratar_put(self, payload):
        print("colocando", payload)

        self.bloqueio.acquire()
        self.em_espera = payload
        aguardado = 0
        mensagem_registro = {
            "termo": self.termo,
            "endereco": self.endereco,
            "payload": payload,
            "acao": "registro",
            "indice_compromisso": self.indice_compromisso
        }

        confirmacoes_registro = [False] * len(self.colegas)
        threading.Thread(target=self.espalhar_atualizacao,
                         args=(mensagem_registro, confirmacoes_registro)).start()
        while sum(confirmacoes_registro) + 1 < self.maioria:
            aguardado += 0.0005
            time.sleep(0.0005)
            if aguardado > cfg.MAX_LOG_WAIT / 1000:
                print(f"aguardado {cfg.MAX_LOG_WAIT} ms, atualização rejeitada:")
                self.bloqueio.release()
                return False
        mensagem_commit = {
            "termo": self.termo,
            "endereco": self.endereco,
            "payload": payload,
            "acao": "compromisso",
            "indice_compromisso": self.indice_compromisso
        }
        self.commit()
        threading.Thread(target=self.espalhar_atualizacao,
                         args=(mensagem_commit, None, self.bloqueio)).start()
        print("maioria alcançada, respondendo ao cliente, enviando mensagem de compromisso")
        return True

    #Replicação de Logs - Kaio
    def espalhar_atualizacao(self, mensagem, confirmacoes=None, bloqueio=None):
        for i, colega in enumerate(self.colegas):
            resposta = utils.enviar(colega, "heartbeat", mensagem)
            if resposta and confirmacoes:
                confirmacoes[i] = True
        if bloqueio:
            bloqueio.release()

    #Replicação de Logs - Kaio
    def commit(self):
        self.indice_compromisso += 1
        self.registro.append(self.em_espera)
        chave = self.em_espera["key"]
        valor = self.em_espera["value"]
        self.BD[chave] = valor
        self.em_espera = None
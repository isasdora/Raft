import random
import requests
from config import cfg


def timeout_aleatorio():
    return random.randrange(cfg.MIN_TIMEOUT, cfg.MAX_TIMEOUT) / 1000


def enviar(endereco, rota, message):
    url = endereco + '/' + rota
    try:
        reply = requests.post(
            url=url,
            json=message,
            timeout=cfg.REQUESTS_TIMEOUT / 1000,
        )
    # failed to send request
    except Exception as e:
        # print(e)
        return None

    if reply.status_code == 200:
        return reply
    else:
        return None

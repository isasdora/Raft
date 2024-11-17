# Raft
É um algoritmo de consenso que busca uma maneira simples e eficiente para sistemas distribuídos concordarem quando estão em um estado compartilhado.

### Eleição de Líder
A eleição de líder é como os nós de um sistema distribuído vão eleger um novo líder após uma falha do líder atual ou falta de acessibilidade a ele. Os nós podem assumir 3 estados, sendo eles:
- LÍDER: Coordena e replica dados;
- SEGUIDOR: Recebe e aplica comandos do líder;
- CANDIDATO: Tenta se eleger líder quando detecta que o nó líder não está mais ativo.

### Replicação de Logs
É o processo pelo qual o líder replica as entradas de log aos nós seguidores, garantindo que todos os nós mantenham uma cópia consistente do log, sendo crucial para garantir a tolerância de falhas e a consistência de dados no cluster.

### Gerenciamento de Termos de Eleição 
Envolve a manutenção de um contador de termos que aumenta a cada nova eleição. Um termo é um período de tempo durante o qual pode haver apenas uma eleição de líder, cada nó registra o termo mais recente que observou, e qualquer nó que detectar um termo mais alto reconhece automaticamente um líder mais atualizado, garantindo que os nós concordem em qual líder é válido.

### Simulação de Falhas e Recuperação
A simulação de falhas e recuperação é utilizada para testar quão resistente um sistema distribuído pode ser, observando como se comportam diante de uma falha, como a perda de um líder. O objetivo é garantir a alta disponibilidade e consistência em ambientes distribuídos.

### Execução de Tarefa Coordenada
A execução da tarefa coordenada será feita quando o algoritmo alcançar o consenso, será enviado um comando (`PUT` ou `GET`) que mostrará como o algoritmo reage diante de um comando após alcançar o consenso.

# Como Rodar o Servidor
Os servidores são inicializados com os índices presente no arquivo `Lista_IP.txt` que conta com 5 (0 a 4) endereços. Os endereços dos servidores são necessários para que cada nó em um sistema distribuído saiba como se comunicar com os outros. Esses endereços permitem que os nós enviem mensagens entre si, como solicitações de votos, heartbeat e atualizações de logs, essenciais para coordenar operações e manter a consistência e a disponibilidade do sistema.

```
http://127.0.0.1:5000
http://127.0.0.1:5001
http://127.0.0.1:5002
http://127.0.0.1:5003
http://127.0.0.1:5004
```

Exemplo de como rodar cada um dos 5 servidores:

```
python servidor.py 0
python servidor.py 1
python servidor.py 2
python servidor.py 3
python servidor.py 4
```

# Como Rodar o Cliente
O cliente pode realizar duas das solicitações `HTTP`, sendo elas `PUT` e `GET`. Exemplos do uso dessas solicitações no windows:

```
PUT: py cliente.py 'endereço' 'chave' 'valor'
GET: py cliente.py 'endereço' 'chave'
```

- Se `PUT`:
  -  O primeiro argumento a ser passado sempre será o endereço de um servidor que estará em funcionamento;
  -  O segundo será a chave;
  -  O terceiro um valor para a chave.
  
```
PUT: py cliente.py http://127.0.0.1:5000 cor "Vermelho"
{'codigo': 'successo'}
```
- Se `GET`:
  -  O primeiro argumento a ser passado sempre será o endereço de um servidor que estará em funcionamento;
  -  O segundo será a chave.
  
```
GET: py cliente.py http://127.0.0.1:5000 cor
{'codigo': 'successo', 'payload': {'key': 'cor', 'value': 'Vermelho'}}
```
## Comunicação Cliente/Servidor
A comunicação entre o cliente e o servidor é feita atráves da API REST que foi implementada pela biblioteca Flask, que é usada para expor diferentes endpoints que aceitam e processam requisições `HTTP`, retornando respostas em formato JSON.

## Instalações Adicionais
- flask >= 1.0
- python >= 3.6
  - sys
  - logging
  - time
  - threading
  - random
  - requests

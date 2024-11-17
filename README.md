# Raft
É um algoritmo de consenso que busca uma maneira simples e eficiente para sistemas distribuídos concordarem quando estão em um estado compartilhado.

### Eleição de Líder


### Replicação de Logs


### Gerenciamento de Termos de Eleição 


### Simulação de Falhas e Recuperação
A simulação de falhas e recuperação é utilizada para testar quão resistente um sistema distribuído pode ser, observando como se comportam diante de uma falha, como a perda de um líder. O objetivo é garantir a alta disponibilidade e consistência em ambientes distribuídos.

### Execução de Tarefa Coordenada
A execução da tarefa coordenada será feita quando o algoritmo alcançar o consenso, será enviado um comando (`PUT` ou `GET`) que mostrará como o algoritmo reage diante de um comando após alcançar o consenso.

# Como Rodar o Servidor


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

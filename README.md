# Raft
É um algoritmo de consenso que busca uma maneira simples e eficiente para sistemas distribuídos concordarem quando estão em um estado compartilhado.

## Eleição de Líder


## Replicação de Logs


## Gerenciamento de Termos de Eleição 


## Simulação de Falhas e Recuperação


## Execução de Tarefa Coordenada


# Como Rodar o Servidor


# Como Rodar o Cliente
O cliente pode realizar duas das solicitações HTTP, sendo elas `PUT` e `GET`. 
Exemplos do uso dessas solicitações no windows:

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
  -  O segundo será a chave;
  
```
GET: py cliente.py http://127.0.0.1:5000 cor
{'codigo': 'successo', 'payload': {'key': 'cor', 'value': 'Vermelho'}}
```
## Comunicação Cliente/Servidor


## Instalações Adicionais

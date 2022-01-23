![iClinic logo](https://d1ydp7gtfj5fb9.cloudfront.net/static/img/views/home_v2/header/logo.png?1525283729)

Este repositório hospeda a minha implementação do desafio [iclinic-python-challenge](https://github.com/iclinic/iclinic-python-challenge). 

## Objetivo

O desafio consiste em desenvolver um serviço `API REST` que possibilite a criação de prescrições médicas a serem 
armazenadas em uma base de dados integrando estas informações com o `SERVIÇO DE MÉTRICAS`. 

Para detalhes sobre os requisitos da `API REST` veja o repositório: [https://github.com/iclinic/iclinic-python-challenge](https://github.com/iclinic/iclinic-python-challenge).

## Arquitetura
A aplicação é composta por dois serviços:

- Um `webserver` desenvolvido em `python` utilizando o framework `Flask`. 
- Uma `base de dados` em `postgresql` para armazenar as prescrições médicas.

Foi criado um container para cada serviço de acordo com o arquivo `docker-compose.yml`.

Para o `webserver` o container é representado por `iclinic` e para `base de dados` o container é representado por `db`


`docker-compose.yml`
```yaml
version: "3"

services:
  # data base image
  db:
    image: postgres:14.0
    restart: always
    environment:
      POSTGRES_DB: iclinic
      POSTGRES_USER: iclinic
      POSTGRES_PASSWORD: iclinic

  # iclinic prescription api
  iclinic:
    restart: always
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - "PYTHONUNBUFFERED=1"
    ports:
      - "8008:8008"
    volumes:
      - .:/app
    depends_on:
      - db


```


## Como executar a API

Requisitos:
- Sistema Operational Linux(local ou nuvem).
- Pacotes necessários: `git`, `docker`, `docker-compose` e `curl` devidamente instalados.

### Instalação das dependências
Para `debian` e `ubuntu`:
```shell
sudo apt update -y
sudo apt install -y git docker docker-compose curl
```

### Clonando o repositório
```shell
git clone https://github.com/jomorais/iclinic-prescriptions-api.git
```

### Construindo e executando os containers da aplicação
Entrar no diretório `iclinic-prescriptions-api/`.
```shell
cd iclinic-prescriptions-api/
```
Construir os containers com o docker-compose com base no arquivo `docker-compose.yml`.
```shell
docker-compose up -d
```
Após o comando acima os containers `db` e `iclinic` já estarão em execução.
    
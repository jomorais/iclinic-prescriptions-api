![iClinic logo](https://d1ydp7gtfj5fb9.cloudfront.net/static/img/views/home_v2/header/logo.png?1525283729)

Este repositório hospeda a minha implementação do desafio [iclinic-python-challenge](https://github.com/iclinic/iclinic-python-challenge). 

## Objetivo

O desafio consiste em desenvolver um serviço `API REST` que possibilite a criação de prescrições médicas a serem 
armazenadas em uma base de dados integrando estas informações com o `SERVIÇO DE MÉTRICAS`. 

Para detalhes sobre os requisitos da `API REST` veja o repositório: [https://github.com/iclinic/iclinic-python-challenge](https://github.com/iclinic/iclinic-python-challenge).

A `API REST` foi disponibilizada em uma instância na Digital Ocean, e pode ser acessada por nessa URL: `http://167.71.92.76:8008`

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

## CI/CD com Github Actions

A `API REST` foi desenvolvida considerando um cenário de integração contínua e entrega contínua.

Esse processo de automação é feito pela funcionalidade do github: `github-actions`.

O workflow foi dividido em duas etapas conforme o arquivo `.github/workflows/build_and_deploy.yml`:

- `build`: realiza a validação da aplicação instalando suas dependências e realizando os tests unitários disponibilizados em: `test/`.
- `deploy`: realiza o deploy da aplicação em uma instância virtual no serviço DigitalOcean.

`build_and_deploy.yml`
```yaml
# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions

name: Python application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        
    - name: Test with pytest
      run: |
        python -m pytest test/*.py
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    
    steps:
      - name: Deployment
        uses: appleboy/ssh-action@master
        with:
          host: ${{secrets.SSH_HOST}}
          key: ${{secrets.SSH_KEY}}
          username: ${{secrets.SSH_USERNAME}}
          
          script: |
            apt install docker docker-compose
            rm -rf iclinic-prescriptions-api/
            git clone git@github.com:jomorais/iclinic-prescriptions-api.git
            cd iclinic-prescriptions-api
            docker-compose build --force-rm --no-cache
            docker-compose up -d

    

```

A cada `push` ou `pull request` no branch `main` do github, automaticamente o `github-actions` executa o workflow iniciando processo de `build`, caso tenha sucesso na build e tests, é iniciado o processo de `deploy` da aplicação para o droplet na Didital Ocean.

## Executando a API

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

## Usando a API
O webserver no container `ìclinic` esta rodando na porta `8008`. 

Para realizar uma requisição `POST` de uma nova prescrição médica vamos utilizar pacote `curl`:

Onde `<HOST>` é o IP ou DNS do host da aplicação:
- caso local: usar `localhost`
```shell
curl -X POST http://localhost:8008/prescriptions -H 'Content-Type: application/json' -d '{"clinic": {"id": 1},"physician": {"id": 1},"patient": {"id": 1},"text": "Dipirona 1x ao dia"}'
```
- caso cloud: usar o IP ou DNS do host (minha instância na Digital Ocean: `167.71.92.76`)

```shell
curl -X POST http://167.71.92.76:8008/prescriptions -H 'Content-Type: application/json' -d '{"clinic": {"id": 1},"physician": {"id": 1},"patient": {"id": 1},"text": "Dipirona 1x ao dia"}'
```

Caso a requisição retornar `SUCESSO`, a api deve retornar um json com a nova prescrição médica salva e enviada para o serviço de métricas:
```json
{"data":{"clinic":{"id":1},"id":289,"metric":{"id":"896496fa-eade-462c-8970-88cea894ec7d"},"patient":{"id":1},"physician":{"id":1},"text":"Dipirona 1x ao dia"}}
```

Caso a requisição retornar `ERROR`, a api deve retornar um json com a mensagem do erro `message` e o código do erro `code`:
```json
{"error":{"code":3,"message":"patient not found"}}
```

Foram mapeados os seguintes erros:

| code | message                            |
|------|------------------------------------|
| 01   | malformed request                  |
| 02   | physician not found                |
| 03   | patient not found                  |
| 04   | metrics service not available      |
| 05   | physicians service not available   |
| 06   | patients service not available     |
| 07   | request timeout                    |
| 08   | http error                         | 
| 09   | invalid url                        | 
| 10   | http status                        | 
| 11   | database error                     | 
| 12   | invalid patients service response  |  
| 13   | invalid physicians service response| 
| 14   | invalid metrics service response   |

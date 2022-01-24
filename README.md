![iClinic logo](https://d1ydp7gtfj5fb9.cloudfront.net/static/img/views/home_v2/header/logo.png?1525283729)

Este repositório hospeda a minha implementação do desafio [iclinic-python-challenge](https://github.com/iclinic/iclinic-python-challenge). 

![test status](https://github.com/jomorais/iclinic-prescriptions-api/actions/workflows/build_and_deploy.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/jomorais/iclinic-prescriptions-api/badge.svg?branch=main)](https://coveralls.io/github/jomorais/iclinic-prescriptions-api?branch=main)

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

![arch_iclinic](https://user-images.githubusercontent.com/6545172/150719249-c808c8fc-92e6-4814-bb42-44f30cdf7d38.png)



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

    - name: Coverage Calc (Coveralls.io)
      run: |
        coverage run --source=. -m pytest test/
        coveralls --service=github
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        COVERALLS_REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  
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

![build_deploy_workflow](https://user-images.githubusercontent.com/6545172/150719743-7c5891c1-d4e9-4182-851a-fba0c28296b5.png)


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

## Depurando a aplicação

Para verificar o status de execução dos containers, execute o comando `docker ps`

```shell
sudo docker ps
```

```shell
CONTAINER ID   IMAGE                               COMMAND                  CREATED        STATUS       PORTS                                       NAMES
df8a5e7174f6   iclinic-prescriptions-api_iclinic   "python3 webserver.py"   4 hours ago    Up 4 hours   0.0.0.0:8008->8008/tcp, :::8008->8008/tcp   iclinic-prescriptions-api_iclinic_1
3e9c2510a2ac   postgres:14.0                       "docker-entrypoint.s…"   19 hours ago   Up 4 hours   5432/tcp                                    iclinic-prescriptions-api_db_1
```

Para visualizar os logs da API execute o comando `docker logs`
```shell
sudo docker logs -f iclinic-prescriptions-api_iclinic_1
```

```shell

INFO:Prescriptions.create_prescription(): creating a new prescription: {'clinic': {'id': 51}, 'physician': {'id': 50}, 'patient': {'id': 50}, 'text': 'Dipirona 1x ao diaasdasd'}
INFO:Prescriptions.create_prescription(): accessing Dependent Services...
INFO:Prescriptions.create_prescription(): Physician acquired from Physicians Service API: {'id': 50, 'name': 'Larissa Aragão', 'crm': '84218971'}
INFO:Prescriptions.create_prescription(): Patient acquired from Patient Service API: {'id': 50, 'name': 'Lorenzo da Rosa', 'email': 'lucas-gabrielda-mota@costa.br', 'phone': '+55 61 9332 0585'}
WARNING:Prescriptions.create_prescription(): Clinic not found: {'error': {'message': 'clinic not found', 'code': 7}}
INFO:Prescriptions.create_prescription(): New Prescription: {'data': {'id': 0, 'clinic': {'id': 51}, 'physician': {'id': 50}, 'patient': {'id': 50}, 'text': 'Dipirona 1x ao diaasdasd', 'metric': {'id': ''}}}
INFO:Prescriptions.create_prescription(): saving in database...
INFO:Prescriptions.create_prescription(): SAVED! prescription.id: 295
INFO:Prescriptions.create_prescription(): New Metric: {'id': '', 'physician_id': 50, 'physician_name': 'Larissa Aragão', 'physician_crm': '84218971', 'patient_id': 50, 'patient_name': 'Lorenzo da Rosa', 'patient_email': 'lucas-gabrielda-mota@costa.br', 'patient_phone': '+55 61 9332 0585', 'prescription_id': 295}
INFO:Prescriptions.create_prescription(): integrating it in Metrics Service API...
INFO:Prescriptions.create_prescription(): Metrics are integrated!! Metrics: {'id': '896496fa-eade-462c-8970-88cea894ec7d', 'physician_id': 50, 'physician_name': 'Larissa Aragão', 'physician_crm': '84218971', 'patient_id': 50, 'patient_name': 'Lorenzo da Rosa', 'patient_email': 'lucas-gabrielda-mota@costa.br', 'patient_phone': '+55 61 9332 0585', 'prescription_id': 295}
INFO:Prescriptions.create_prescription(): applying Metrics.id into prescription...
INFO:Prescriptions.create_prescription(): New Prescription are created successfully!!
INFO:Prescriptions.create_prescription(): New Prescription: {'data': {'id': 295, 'clinic': {'id': 51}, 'physician': {'id': 50}, 'patient': {'id': 50}, 'text': 'Dipirona 1x ao diaasdasd', 'metric': {'id': '896496fa-eade-462c-8970-88cea894ec7d'}}}
INFO:192.168.64.1 - - [23/Jan/2022 21:46:02] "POST /prescriptions HTTP/1.1" 201 -

```

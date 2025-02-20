# Projeto de testes de uma aplicação Flask simples. 
* Carrega imagens em um banco de dados sqlite3
* Idealizada para rodar em containers
    * Ex: AWS Fargate

## Orientações gerais
* Criar ambiente virtual (Windows - PowerShell)** <br />
    * python3 -m venv venv   
    * venv\Scripts\activate

* Executar no terminal do VSCode
    * Primeiro acesso
        * source .\venv\Scripts\activate
        * pip install -r requirements.txt
    * Demais acessos
        * .\venv\Scripts\activate 

* Servir a aplicação (Windows - Dev)
    * gunicorn -w 4 -b 0.0.0.0:5000 agriapp:app

* Servir a aplicação (Linux - Prod)
    * gunicorn -w 4 -b 0.0.0.0:5000 agriapp:app
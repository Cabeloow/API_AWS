# API de CRUD de pessoas

## Descrição

Demonstração do uso da AWS para criar uma API que execute o CRUD de pessoas

## Funcionalidades

- Cadastro, Consulta, Atualização e exclusão de pessoas

## Peças Utilizadas

- API Gateway
- Lambda
- DynamoDB

## Instalação

1. Clone o repositório: `git clone https://github.com/Cabeloow/case_jr_backend.git`
2. Navegue para o diretório do projeto: `cd terraform`
3. Execute o comando "terraform init" e logo em seguida "terraform apply" e por fim "yes" para subir todas as peças da AWS

## Documentação técnica

- Para acessar a documentação técnica basta:
1. clonar o repositório
2. abrir o arquivo docs > backend > index.html

OBS: A ideia era colocar no git pages, mas tem que pagar :(

## Uso

Rotas e payloads;

- Cadastro: 
    - Método POST
    - payload exemplo:
        {"cpf": "99988877700", 
        "dados_pessoa":{"nome":  "jp", "sobrenome": "silva", "idade": "20", "pais": "brasil"}}


- Consulta: 
    - Método GET
    - Exemplo consulta:
        para retornar um item específico:
            https://2spw209fvf.execute-api.us-east-1.amazonaws.com/desafio/consulta?cpf=99988877700

        para retornar todos os itens:
            https://2spw209fvf.execute-api.us-east-1.amazonaws.com/desafio/consulta


- Atualiza: 
    - Método PATCH
    - payload exemplo:
        {"cpf":"99988877700", 
        "update_itens":{"nome":  "jp", "idade": "3"}}

- Delete: 
    - Método DELETE
    - payload exemplo:
        {"cpf": "99988877700"}

## Testes

- Para executar os testes
1. import a biblioteca pytest
1. Acesse a pasta "tests"
2. Execute o comando python -m pytest test_backend.py -v

- Para executar o teste de cobertura.
1. import a biblioteca coverage
1. Acesse a pasta "tests"
2. Execute os seguintes comandos:
    - python -m coverage run meu_teste.py
    - python -m coverage report -m
    - python -m coverage html
3. em seguida acesse o arquivo tests\htmlcov\index.html

## Contato

- Nome: João Pedro Guimarães da Silva
- E-mail: jpguimaraes27@hotmail.com
- Celular: 19 99300-7616
- LinkedIn: https://www.linkedin.com/in/jo%C3%A3o-pedro-guimar%C3%A3es-silva-b10ab3186/


<div align="center">
<h1 align="center">Desafio técnico Estante virtual</h1>
</div>

<div>
Este é um projeto desenvolvido com o intuito de realizar um teste técnico para a empresa Estante virtual, utilizando Python e FastApi</b>.
<br>
<br>
O teste consiste em criarmos uma api que permita a criação de competições de natação e dardos e ao final mostrar o ranking de cada modalidade.
<div>
  
<h2> Como configurar o ambiente para execução do projeto </h2>

1. Configure o ambiente virtual (recomendado):
   ```
   python -m venv venv
   ```

2. Ative o ambiente virtual:
    ```
    venv\Scripts\activate
    ```

3. Instale as dependências:
    ```
    pip install -r requirements
    ```

Para iniciar o projeto, basta executar o comando abaixo:
   ```
   uvicorn app.main:app --reload
   ```

Para a utilização dos endpoints, basta informar a url abaixo:
   ```
   http://127.0.0.1:8000/
   ```

<h2>Fluxo de utilização dos endpoints</h2>
/competitors > /competicao > /competicao-evento > /competicao/{competicao_id}/ranking

<h2>Exemplos de POST para cada endpoint responsável pelos cadastros</h2>
<h3>/competitor</h3>

```
   {
    "identifier": "1",
    "name": "COMPETIDOR_1",
    "cpf": "1234567890"
  }
```
<h3>/competicao</h3>

```
  {
      "descricao": "Dardo Final",
      "modalidade": "Dardo",
      "ano_competicao": 2024,
      "status": "EM_ANDAMENTO"
  }
```
<h3>/competicao-evento</h3>

```
  {
      "competicao_id": 1,
      "competitor_id": 1,
      "value": "9.0",
      "unidade": "m"
  }
```
<br>
<br>

Para visualizar o resultado/ranking de cada competição utilizando o endpoint /competicao/{competicao_id}/ranking.<br>
Abaixo um exemplo de retorno:
```
{
    "competicao-id": 1,
    "competicao-descricao": "Dardo Final",
    "competicao-status": "FINALIZADO",
    "competicao-modalidade": "Dardo",
    "competitors-ranking": [
        {
            "id": 4,
            "nome": "COMPETIDOR_4,
            "identificador": "4",
            "valor": "100.0",
            "posicao": 1
        },
        {
            "id": 3,
            "nome": "COMPETIDOR_3",
            "identificador": "3",
            "valor": "90.50",
            "posicao": 2
        },
        {
            "id": 1,
            "nome": "COMPETIDOR_1",
            "identificador": "1",
            "valor": "60.50",
            "posicao": 3
        },
        {
            "id": 2,
            "nome": "COMPETIDOR_2",
            "identificador": "2",
            "valor": "20.50",
            "posicao": 4
        }
    ]
}
```
<br>
<br>

<h2>Algumas regras de negócio aplicadas no projeto</h2>
1° No endpoint <b>/competitors</b> não é permitido cadastrar mais de um competidor com o mesmo numero de identificação e CPF. <br><br>
2° No endpoint <b>competicao-evento</b> é permitido somente o cadastro caso a competição informada no json não esteja finalizada, além de verificar se o candidato tenha no máximo 3 cadastros para a modalidade Dardo.<br><br>
3° No endpoint <b>/competicao/{competicao_id}/ranking</b> o ranking é contabilizado de maneira diferente para cada modalidade:<br>
  - Natação: O ganhador é aquele que possui o menor tempo de cada tentativa.<br>
  - Dardo: O ganhador é aquele que possui a maior distância, dentre 3 tentativas.<br>
<br>
<br>

<h3>Por fim para mais detalhes de GET e schemas de operações PUT e DELETE, basta acessar a url: http://127.0.0.1:8000/docs</h3>
<br>

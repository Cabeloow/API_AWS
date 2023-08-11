import boto3
import logging
import json
from utils import formata_payload_update, validate_payload


class Motor:
    def __init__(self, payload):
        """
        Inicializa a classe Motor.

        Args:
            payload (dict): Dados a serem manipulados pelo motor.
        """
        self.payload = payload
        self.dynamodb = self._create_dynamo_connection()

    def _create_dynamo_connection(self):
        """
        Cria e retorna uma conexão com o DynamoDB.

        Returns:
            boto3.resource: Conexão com a tabela DynamoDB.
        """
        # Define o nome da tabela do DynamoDB
        table_name = "tab_cadastro_user"

        # Cria a conexão com o DynamoDB
        dynamo = boto3.resource("dynamodb").Table(table_name)

        return dynamo

    def create_data(self):
        """
        Cria um novo item na tabela DynamoDB.

        Exemplo de payload:
        {
            "cpf": "99988877700",
            "dados_pessoa":
                {"nome":  "jp",
                "sobrenome": "silva",
                "idade": "20",
                "pais": "brasil"
            }
        }


        Returns:
            dict: Resposta da criação.
        """

        dict_campos_obrigatorios = {"cpf": str, "dados_pessoa": dict}
        validacao = validate_payload(self.payload, dict_campos_obrigatorios)

        if validacao != "ok":
            return validacao

        logging.info("Iniciando a inserção de item")
        response = self.dynamodb.put_item(Item=self.payload)
        logging.info(f"Resposta ---> {response}")

        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": "Item cadastrado com sucesso!", "response": response}
            ),
        }

    def get_data(self):
        """
        Obtém dados da tabela DynamoDB com base no cpf fornecido.
        Quando o cpf é fornecido, traz somente esse item, caso contrário
        traz todos os itens.

        Exemplo de payload:
        url_da_minha_api/consulta?cpf=99988877700

        ou

        url_da_minha_api/consulta

        Returns:
            dict: Dados obtidos.
        """
        if self.payload:
            dict_campos_obrigatorios = {"cpf": str}
            validacao = validate_payload(self.payload, dict_campos_obrigatorios)

            if validacao != "ok":
                return validacao

            item_id = self.payload["cpf"]
            response = self.dynamodb.get_item(Key={"cpf": item_id})
            item = response.get("Item", {})
        else:
            response = self.dynamodb.scan()
            item = response.get("Items", {})

        return {"statusCode": 200, "body": json.dumps(str(item))}

    def update_data(self):
        """
        Atualiza dados na tabela DynamoDB com base no payload fornecido.

        Exemplo de payload:
        {
            "cpf": "99988877700",
            "update_itens": {
                "nome":  "jp",
                "idade": "20"
            }
        }

        Returns:
            dict: Resposta da atualização.
        """

        dict_campos_obrigatorios = {"cpf": str, "update_itens": dict}
        validacao = validate_payload(self.payload, dict_campos_obrigatorios)

        if validacao != "ok":
            return validacao

        update_expression = formata_payload_update(self.payload)
        response = self.dynamodb.update_item(
            Key=update_expression["Key"],
            ConditionExpression=update_expression["ConditionExpression"],
            ReturnValues=update_expression["ReturnValues"],
            UpdateExpression=update_expression["UpdateExpression"],
            ExpressionAttributeValues=update_expression["ExpressionAttributeValues"],
        )
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Item(s) atualizado(s) com sucesso!",
                    "item(s) atualizado(s)": f"{str(response['Attributes'])}",
                }
            ),
        }

    def delete_data(self):
        """
        Exclui um item da tabela DynamoDB com base no cpf fornecido.

        Exemplo de payload:
        {
            "cpf": "99988877700"
        }

        Returns:
            dict: Resposta da exclusão.
        """

        dict_campos_obrigatorios = {"cpf": str}
        validacao = validate_payload(self.payload, dict_campos_obrigatorios)

        if validacao != "ok":
            return validacao

        item_id = self.payload["cpf"]
        response = self.dynamodb.delete_item(
            Key={"cpf": item_id}, ConditionExpression="attribute_exists(cpf)"
        )
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": "Item excluído com sucesso!", "response": response}
            ),
        }

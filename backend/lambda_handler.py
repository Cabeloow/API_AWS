import json

from motor_back import Motor


def lambda_handler(event, context):
    """
    Função principal que atua como um handler para as requisições da API.

    Args:
        event (dict): Dados do evento da AWS Lambda contendo informações da requisição.
        context (object): Objeto de contexto da AWS Lambda.

    Returns:
        dict: Resposta da função, incluindo o statusCode e o body.
    """

    # Verifica qual rota da API foi acessada e executa a operação correspondente
    if event["path"] == "/consulta":
        motor_back = Motor(event["queryStringParameters"])
        response = motor_back.get_data()

    elif event["path"] == "/atualiza":
        mtr = Motor(eval(event["body"]))
        response = mtr.update_data()

    elif event["path"] == "/delete":
        mtr = Motor(eval(event["body"]))
        response = mtr.delete_data()

    elif event["path"] == "/cadastro":
        mtr = Motor(eval(event["body"]))
        response = mtr.create_data()

    else:
        # Caso uma rota inválida seja acessada
        response = {
            "statusCode": 400,
            "body": json.dumps({"message": "Essa rota não existe!"}),
        }

    return response

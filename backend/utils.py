import json


def formata_payload_update(payload):
    update_expression = "SET "
    expression_attribute_values = {}
    for key in payload["update_itens"].keys():
        update_expression += f"dados_pessoa.{key} = :{key}, "
        expression_attribute_values[f":{key}"] = payload["update_itens"][key]

    formated_payload = {
        "Key": {"cpf": payload["cpf"]},
        "ConditionExpression": "attribute_exists(cpf)",
        "ReturnValues": "UPDATED_NEW",
        "UpdateExpression": update_expression[:-2],
        "ExpressionAttributeValues": expression_attribute_values,
    }

    return formated_payload


def validate_payload(payload, lista_campos_obrigatorios):
    # Verifica campos obrigatórios faltantes
    lista_campos_faltantes = list(
        set(lista_campos_obrigatorios.keys()) - set(payload.keys())
    )
    if lista_campos_faltantes:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Ha campos obrigatorios faltando",
                    "campos faltando": str(lista_campos_faltantes),
                }
            ),
        }

    # Valida tipos e campos vazios
    dict_campos_type = {}
    lista_campos_vazios = []
    for value, key, tipo in zip(
        payload.values(), payload.keys(), lista_campos_obrigatorios.values()
    ):
        if not isinstance(value, tipo):
            dict_campos_type[key] = f"tipagem correta: {str(tipo)}"
        if not value:
            lista_campos_vazios.append(key)

    # Verifica campos vazios
    if lista_campos_vazios:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Todos os campos devem estar preenchidos.",
                    "campos em branco": str(lista_campos_vazios),
                }
            ),
        }

    # Verifica tipos divergentes
    if dict_campos_type:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Ha campos com a tipagem errada.",
                    "campos divergentes": dict_campos_type,
                }
            ),
        }

    dict_campos_type_update_itens = {}
    lista_campos_vazios_update_itens = []
    if "dados_pessoa" in payload.keys() or "update_itens" in payload.keys():
        if "dados_pessoa" in payload.keys():
            key_payload = "dados_pessoa"
            lista_campos_obrigatorios = ["nome", "sobrenome", "idade", "pais"]

            lista_campos_faltantes = list(
                set(lista_campos_obrigatorios) - set(payload[key_payload].keys())
            )
            if lista_campos_faltantes:
                return {
                    "statusCode": 400,
                    "body": json.dumps(
                        {
                            "message": "Ha campos obrigatorios faltando",
                            "campos faltando": str(lista_campos_faltantes),
                        }
                    ),
                }

        elif "update_itens" in payload.keys():
            key_payload = "update_itens"

        for value, keys in zip(payload[key_payload].values(), payload[key_payload]):
            if not isinstance(value, str):
                dict_campos_type_update_itens[keys] = "tipagem correta: str"
            if not value:
                lista_campos_vazios_update_itens.append(keys)

    if dict_campos_type_update_itens:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Ha campos com a tipagem errada.",
                    "campos divergentes": dict_campos_type_update_itens,
                }
            ),
        }

    if lista_campos_vazios_update_itens:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Ha campos vazios.",
                    "campos vazios": str(lista_campos_vazios_update_itens),
                }
            ),
        }

    # Se tudo estiver válido, retorna "ok"
    return "ok"

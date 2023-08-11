import unittest
from unittest.mock import MagicMock

import sys
import os

# Adicione o diretório "backend" ao caminho de busca de módulos
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.append(backend_path)

# Agora você pode importar a classe Motor normalmente
from motor_back import Motor


class TestMotorMethods(unittest.TestCase):
    def setUp(self):
        # Configuração inicial para os testes
        self.payload = {
            "cpf": "99988877700",
            "nome": "joao pedro guimaraes",
            "sobrenome": "silva",
            "idade": 20,
            "pais": "brasil",
        }
        self.dynamodb_mock = MagicMock()
        self.motor = Motor(self.payload)
        self.motor.dynamodb = self.dynamodb_mock

    def test_create_data(self):
        self.dynamodb_mock.put_item.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }
        payload = {
            "cpf": "99988877700",
            "dados_pessoa": {
                "nome": "joao pedro guimaraes",
                "sobrenome": "silva",
                "idade": "20",
                "pais": "brasil",
            },
        }
        mtr = Motor(payload)
        response = mtr.create_data()
        self.assertEqual(response["statusCode"], 200)

    def test_get_data(self):
        self.dynamodb_mock.get_item.return_value = {
            "Item": {"cpf": "99988877700", "nome": "joao pedro guimaraes"}
        }
        response = self.motor.get_data()
        self.assertEqual(response["statusCode"], 200)

    def test_get_data_all(self):
        self.dynamodb_mock.get_item.return_value = {
            "Item": {"cpf": "99988877700", "nome": "joao pedro guimaraes"}
        }
        mtr = Motor("")
        mtr.dynamodb = self.dynamodb_mock
        response = mtr.get_data()
        self.assertEqual(response["statusCode"], 200)

    def test_update_data(self):
        self.dynamodb_mock.update_item.return_value = {
            "Attributes": {"cpf": "99988877700", "nome": "novo_nome"}
        }
        payload_update = {
            "cpf": "99988877700",
            "update_itens": {"nome": "jp", "idade": "12"},
        }
        mtr = Motor(payload_update)
        mtr.dynamodb = self.dynamodb_mock
        response = mtr.update_data()
        self.assertEqual(response["statusCode"], 200)

    def test_delete_data(self):
        self.dynamodb_mock.delete_item.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }
        response = self.motor.delete_data()
        self.assertEqual(response["statusCode"], 200)

    def test_campos_obrigatorios_faltantes_create(self):
        payload = {
            "cpf": "99988877700",
            # "dados_pessoa": {
            #     "nome": "joao pedro guimaraes",
            #     "sobrenome": "silva",
            #     "idade": "20",
            #     "pais": "brasil",
            # },
        }
        mtr = Motor(payload)
        response = mtr.create_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_obrigatorios_faltantes_dados_pessoa_create(self):
        payload = {
            "cpf": "99988877700",
            "dados_pessoa": {
                # "nome": "jp",
                "sobrenome": "silva",
                "idade": "20",
                "pais": "brasil",
            },
        }
        mtr = Motor(payload)
        response = mtr.create_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_obrigatorios_em_branco_dados_pessoa_create(self):
        payload = {
            "cpf": "99988877700",
            "dados_pessoa": {
                "nome": "",
                "sobrenome": "silva",
                "idade": "20",
                "pais": "brasil",
            },
        }
        mtr = Motor(payload)
        response = mtr.create_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_obrigatorios_em_branco_create(self):
        payload = {"cpf": "99988877700", "data": {}}
        mtr = Motor(payload)
        response = mtr.create_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_tipagem_errada_create(self):
        payload = {
            "cpf": "99988877700",
            "dados_pessoa": '{"nome": "joao pedro guimaraes", "sobrenome": "silva", "idade": "20", "pais": "brasil"}',
        }
        mtr = Motor(payload)
        response = mtr.create_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_tipagem_errada_dados_pessoa_create(self):
        payload = {
            "cpf": "99988877700",
            "dados_pessoa": {
                "nome": "joao pedro guimaraes",
                "sobrenome": "silva",
                "idade": 20,
                "pais": "brasil",
            },
        }
        mtr = Motor(payload)
        response = mtr.create_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_obrigatorios_faltantes_update(self):
        payload = {"update_itens": {"teste": "valor_teste", "teste2": "valor2"}}
        mtr = Motor(payload)
        response = mtr.update_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_obrigatorios_em_branco_update(self):
        payload = {"cpf": "1", "update_itens": {}}
        mtr = Motor(payload)
        response = mtr.update_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_tipagem_errada_update(self):
        payload = {
            "cpf": "1",
            "update_itens": '{"nome": "valor_teste", "idade": "2"}',
        }
        mtr = Motor(payload)
        response = mtr.update_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_tipagem_errada_update_itens(self):
        payload = {
            "cpf": "1",
            "update_itens": {"nome": "valor_teste", "idade": 22},
        }
        mtr = Motor(payload)
        response = mtr.update_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_obrigatorios_faltantes_delete(self):
        payload = {}
        mtr = Motor(payload)
        response = mtr.delete_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_obrigatorios_em_branco_delete(self):
        payload = {"cpf": ""}
        mtr = Motor(payload)
        response = mtr.delete_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_tipagem_errada_delete(self):
        payload = {"cpf": 1}
        mtr = Motor(payload)
        response = mtr.delete_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_obrigatorios_em_branco_get(self):
        payload = {"cpf": ""}
        mtr = Motor(payload)
        response = mtr.get_data()
        self.assertEqual(response["statusCode"], 400)

    def test_campos_tipagem_errada_get(self):
        payload = {"cpf": 1}
        mtr = Motor(payload)
        response = mtr.get_data()
        self.assertEqual(response["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()

resource "aws_api_gateway_rest_api" "my_api" {
  name = "api_crud_user"
}

# """
# CONSULTA
# """
resource "aws_api_gateway_resource" "consulta" {
  rest_api_id = "${aws_api_gateway_rest_api.my_api.id}"
  parent_id   = "${aws_api_gateway_rest_api.my_api.root_resource_id}"
  path_part   = "consulta"
}

resource "aws_api_gateway_method" "consulta_get" {
  rest_api_id   = "${aws_api_gateway_rest_api.my_api.id}"
  resource_id   = "${aws_api_gateway_resource.consulta.id}"
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method_response" "lambda_consulta_get_response_200" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  resource_id = aws_api_gateway_resource.consulta.id
  http_method = aws_api_gateway_method.consulta_get.http_method
  status_code = "200"
}


resource "aws_api_gateway_integration" "lambda_consulta" {
  rest_api_id = "${aws_api_gateway_rest_api.my_api.id}"
  resource_id = "${aws_api_gateway_method.consulta_get.resource_id}"
  http_method = "${aws_api_gateway_method.consulta_get.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.my_lambda.invoke_arn}"
}

# """
# CADASTRO
# """
resource "aws_api_gateway_resource" "cadastro" {
  rest_api_id = "${aws_api_gateway_rest_api.my_api.id}"
  parent_id   = "${aws_api_gateway_rest_api.my_api.root_resource_id}"
  path_part   = "cadastro"
}

resource "aws_api_gateway_method" "cadastro_post" {
  rest_api_id   = "${aws_api_gateway_rest_api.my_api.id}"
  resource_id   = "${aws_api_gateway_resource.cadastro.id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method_response" "lambda_cadastro_post_response_200" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  resource_id = aws_api_gateway_resource.cadastro.id
  http_method = aws_api_gateway_method.cadastro_post.http_method
  status_code = "200"
}


resource "aws_api_gateway_integration" "lambda_cadastro" {
  rest_api_id = "${aws_api_gateway_rest_api.my_api.id}"
  resource_id = "${aws_api_gateway_method.cadastro_post.resource_id}"
  http_method = "${aws_api_gateway_method.cadastro_post.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.my_lambda.invoke_arn}"
}


# """
# ATUALIZA
# """
resource "aws_api_gateway_resource" "atualiza" {
  rest_api_id = "${aws_api_gateway_rest_api.my_api.id}"
  parent_id   = "${aws_api_gateway_rest_api.my_api.root_resource_id}"
  path_part   = "atualiza"
}

resource "aws_api_gateway_method" "atualiza_post" {
  rest_api_id   = "${aws_api_gateway_rest_api.my_api.id}"
  resource_id   = "${aws_api_gateway_resource.atualiza.id}"
  http_method   = "PATCH"
  authorization = "NONE"
}

resource "aws_api_gateway_method_response" "lambda_atualiza_post_response_200" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  resource_id = aws_api_gateway_resource.atualiza.id
  http_method = aws_api_gateway_method.atualiza_post.http_method
  status_code = "200"
}


resource "aws_api_gateway_integration" "lambda_atualiza" {
  rest_api_id = "${aws_api_gateway_rest_api.my_api.id}"
  resource_id = "${aws_api_gateway_method.atualiza_post.resource_id}"
  http_method = "${aws_api_gateway_method.atualiza_post.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.my_lambda.invoke_arn}"
}



# """
# DELETE
# """
resource "aws_api_gateway_resource" "delete" {
  rest_api_id = "${aws_api_gateway_rest_api.my_api.id}"
  parent_id   = "${aws_api_gateway_rest_api.my_api.root_resource_id}"
  path_part   = "delete"
}

resource "aws_api_gateway_method" "delete_post" {
  rest_api_id   = "${aws_api_gateway_rest_api.my_api.id}"
  resource_id   = "${aws_api_gateway_resource.delete.id}"
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_method_response" "lambda_delete_post_response_200" {
  rest_api_id = aws_api_gateway_rest_api.my_api.id
  resource_id = aws_api_gateway_resource.delete.id
  http_method = aws_api_gateway_method.delete_post.http_method
  status_code = "200"
}


resource "aws_api_gateway_integration" "lambda_delete" {
  rest_api_id = "${aws_api_gateway_rest_api.my_api.id}"
  resource_id = "${aws_api_gateway_method.delete_post.resource_id}"
  http_method = "${aws_api_gateway_method.delete_post.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.my_lambda.invoke_arn}"
}

resource "aws_api_gateway_deployment" "deploy" {
  depends_on = [
    "aws_api_gateway_integration.lambda_consulta",
    "aws_api_gateway_integration.lambda_cadastro",
    "aws_api_gateway_integration.lambda_atualiza",
    "aws_api_gateway_integration.lambda_delete",
  ]

  rest_api_id = "${aws_api_gateway_rest_api.my_api.id}"
  stage_name  = "desafio"
}

resource "aws_lambda_function" "my_lambda" {
  function_name = "lambda_backend_crud_user"
  handler      = "lambda_handler.lambda_handler"
  runtime      = "python3.9"
  filename     = "C:/Users/DELL/Desktop/teste - vaga/case_jr_backend/backend/backend.zip"
  role         = "arn:aws:iam::221231353130:role/lambda-apigateway-role"
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "Allowmy_apiInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.my_lambda.function_name}"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.my_api.execution_arn}/*"
#   source_arn = "arn:aws:execute-api:us-east-1:221231353130:${aws_api_gateway_rest_api.my_api.id}/*/${aws_api_gateway_method.consulta_get.http_method}${aws_api_gateway_resource.consulta.path}"
}
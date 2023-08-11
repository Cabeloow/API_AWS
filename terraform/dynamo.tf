resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "tab_cadastro_user"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "cpf"

  attribute {
    name = "cpf"
    type = "S"
  }

  tags = {
    Name        = "tab_cadastro_user"
  }
}
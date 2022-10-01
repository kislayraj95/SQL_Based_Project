from src.helpers.Check_all_validities import * 
def test_parser_False():
  assert check_validity_of_data(" ", "@")==False 
  assert check_validity_of_data(" ", "^")==False
  assert check_validity_of_data(" ", "*")==False  
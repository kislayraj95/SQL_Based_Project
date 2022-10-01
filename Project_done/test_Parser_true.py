from src.helpers.Check_all_validities import * 
def test_parser_true():
  assert check_validity_of_data("Smith | Steve | D | M | Red | 3-3-1985", "|")==True 
  assert check_validity_of_data("Abercrombie, Neil, Male, Tan, 2/13/1943", ",")==True 
  assert check_validity_of_data("Kournikova Anna F F 6-3-1975 Red", " ")==True
  
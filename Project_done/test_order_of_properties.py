from src.helpers.Check_all_validities import * 
def test_properties_order():
  assert check_validity_of_data("Smith | Steve | D | M | Red | 3-3-1985", "|")==True 
  assert check_validity_of_data("Abercrombie, Neil, Male, Tan, 2/13/1943", ",")==True 
  assert check_validity_of_data("Kournikova Anna F F 6-3-1975 Red", " ")==True
  # chaning the order 
  assert check_validity_of_data("Smith | Steve | M | D | Red | 3-3-1985", "|")==False  
  assert check_validity_of_data("Abercrombie, Neil, Tan, Male, 2/13/1943", ",")==False
  assert check_validity_of_data("Kournikova F F Anna 6-3-1975 Red", " ")==False 
  
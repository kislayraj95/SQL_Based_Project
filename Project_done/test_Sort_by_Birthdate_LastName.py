from src.helpers.sort.sort import sort_by_birth_date_last_name
from src.helpers.parse_file import parse_file
from src.helpers.format_data import format_output

def test_Sort_by_Birthdate_LastName():
  combined_Data= []
  all_data = parse_file("./Project_done/data/pipe.txt", parser="|")

  combined_Data.extend(all_data)

  all_data = parse_file("./Project_done/data/comma.txt", parser=",")
  combined_Data.extend(all_data)

  all_data = parse_file("./Project_done/data/space.txt", parser=" ")
  combined_Data.extend(all_data)
  sorted_data = sort_by_birth_date_last_name(combined_Data)
  output = format_output(sorted_data)
  expected_output = "Abercrombie Neil Male 2/13/1943 Tan\nKelly Sue Female 7/12/1959 Pink\n"
  expected_output +="Bishop Timothy Male 4/23/1967 Yellow\nSeles Monica Female 12/2/1973 Black\n"
  expected_output +="Bonk Radek Male 6/3/1975 Green\nBouillon Francis Male 6/3/1975 Blue\n"
  expected_output +="Kournikova Anna Female 6/3/1975 Red\nHingis Martina Female 4/2/1979 Green\n"
  expected_output +="Smith Steve Male 3/3/1985 Red\n"
  assert expected_output==output
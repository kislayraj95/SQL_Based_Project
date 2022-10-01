import pytest
from datetime import datetime
from src.helpers.format_data import format_output
from src.helpers.parse_file import parse_file
from src.helpers.sort.sort import *
def test_format():
  combined_Data= []
  all_data = parse_file("./Project_done/data/pipe.txt", parser="|")

  combined_Data.extend(all_data)

  all_data = parse_file("./Project_done/data/comma.txt", parser=",")
  combined_Data.extend(all_data)

  all_data = parse_file("./Project_done/data/space.txt", parser=" ")
  combined_Data.extend(all_data)
  sorted_data = sort_by_gender_last_name(combined_Data)
  output = format_output(sorted_data)

  expected_output = "Hingis Martina Female 4/2/1979 Green\nKelly Sue Female 7/12/1959 Pink\n"
  expected_output +="Kournikova Anna Female 6/3/1975 Red\nSeles Monica Female 12/2/1973 Black\n"
  expected_output +="Abercrombie Neil Male 2/13/1943 Tan\nBishop Timothy Male 4/23/1967 Yellow\nBonk Radek Male 6/3/1975 Green\nBouillon Francis Male 6/3/1975 Blue\nSmith Steve Male 3/3/1985 Red\n"

  assert output==expected_output
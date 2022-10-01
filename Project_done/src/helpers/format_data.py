def format_output(sorted_data):
  """
  Getting desired output format 
  """
  required_properites=["LastName", "FirstName",  "Gender",  "DateOfBirth","FavouriteColor"]
  output=""
  for temp_dic in sorted_data:
    for field in required_properites:
      if field=='DateOfBirth':
        output+=temp_dic[field].strftime('%m/%d/%Y').replace('0', '')
      else: 
        output+=temp_dic[field].replace("\n","")
      if field!="FavouriteColor":
        output+=" "
    output+="\n"
  return output 
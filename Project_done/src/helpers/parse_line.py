import datetime 



def str_to_date(date_str):
  "Convert string to date object for sorting purpose "
  date_str = date_str.replace("-", "/")
  format_str = '%m/%d/%Y' # The format
  datetime_obj = datetime.datetime.strptime(date_str, format_str)
  return datetime_obj.date()


def parse_line(line, parser):
    # Every parser has different arrange order, we need dic to hold correct order    
  parser_dic = {"|": ["LastName", "FirstName", "MiddleInitial", "Gender", "FavouriteColor", "DateOfBirth"], 
                ",": ["LastName", "FirstName",  "Gender", "FavouriteColor", "DateOfBirth"],
                " ": ["LastName", "FirstName", "MiddleInitial", "Gender", "DateOfBirth",  "FavouriteColor"]}  
  properties_values = line.split(parser) # parse each line  
  all_keys=parser_dic[parser] # all keys based on parser [list]
  parsed_line = {}
  for i in range(len(properties_values)): # interate through every value 
    parsed_line[all_keys[i]]=""
    if parser in ('|', " "):  # these two parse has different gender and date format so have to deal differently
      # mapping from M-> Male, F-->Female
      
      if all_keys[i]=="Gender" and properties_values[i].replace(" ","")=='M':
        parsed_line[all_keys[i]]= "Male"
        continue 
      elif all_keys[i]=="Gender":
        parsed_line[all_keys[i]]= "Female"
        continue 
      if all_keys[i]=="DateOfBirth":
        parsed_line[all_keys[i]]= str_to_date(properties_values[i].replace(" ","").replace("\n",""))
      else:
        parsed_line[all_keys[i]]= properties_values[i].replace(" ","") # store data in all data 
    else:
      if all_keys[i]=="DateOfBirth":
          parsed_line[all_keys[i]]= str_to_date(properties_values[i].replace(" ","").replace("\n",""))
      else:
        parsed_line[all_keys[i]]= properties_values[i].replace(" ","") # store data in all data 
  
  return parsed_line
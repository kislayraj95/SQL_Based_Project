def check_validity_of_data(line,parser):
    """
    function checks validity of line and parser 
    if invalid, return false 
    other true 
    """
    if parser not in [' ', '|', ',']: # parser itself is wrong 
      return False 
    elif parser=='|':  
      if '|' not in line: # if got wrong parser in line then consider it wrong 
        return False 
      else:
        parsed_line = line.split(parser) # parse line 
        if parsed_line[3].replace(" ","") in ["M", "F"]: # for | check if gender is on correct order
          return True 
        else:
          return False 
    elif parser==',':  
          if ',' not in line: # if got wrong parser in line then consider it wrong 
            return False 
          else:
            parsed_line = line.split(parser) # parse line 
            if parsed_line[2].replace(" ","") in ["Male", "Female"]: # for , check if gender is on correct order
              return True 
            else:
              return False 
    elif parser==' ':  
          if ' ' not in line: # if got wrong parser in line then consider it wrong 
            return False 
          else:
            parsed_line = line.split(parser) # parse line 
            if parsed_line[3].replace(" ","") in ["M", "F"]: # for ' ' check if gender is on correct order
              return True 
            else:
              return False 

from .parse_line import parse_line


def parse_file(filename, parser="|"):
  """
  Function to parse all values in given filename 
  filename (string): name of the file to be read 
  parser (string): on which delimintor we want to parse
  """

  data = open(filename).readlines() # Reading file 
  parsed_file=[]  # all file data will be saved here 
  for line in data: # read line by line 
      parsed_file.append(parse_line(line,parser))
  return parsed_file 

if __name__=="__main__":
    print(parse_file("space.txt", parser=" "))
def sort_by_gender_last_name(data):
  """
  Function to sort data by gender then last_name ascending 
  """
  return sorted(data, key=lambda x: (x['Gender'],x["LastName"]))  # sort dictionary based on specific property
  # sorted(data, key=lambda x: (x['Gender']))
def sort_by_birth_date_last_name(data):
  """
  Function to sort data by last_name and gender ascending 
  """
  
  return sorted(data, key=lambda x: (x['DateOfBirth'], x["LastName"]))  # sort dictionary based on specific property

def sort_by_last_name_descending(data):
  """
  Function to sort data by last_name descending 
  """
  return sorted(data, key=lambda x: x['LastName'], reverse=True)  # sort dictionary based on specific property
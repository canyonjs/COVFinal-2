# Import Modules
import csv

# Array to hold all rows as objects as elements
data_array = []

metric_values = {"deaths": "total_deaths", "cases": "total_cases", "positivity": "positivity_rate", "new": "new_cases"}

# Open dataset csv and store each row as object in array
with open("owid-covid-data.csv", 'r') as dataset:
  reader = csv.DictReader(dataset)
  for row in reader:
    data_array.append(dict(row))

# Format country input for either ISO code or standard country name
def format_input(user_input):
  if len(user_input) == 3:
    return user_input.upper()
  else:
    return user_input.title()

# Check to see if country or ISO code exists in dataset
def validate_input(input_to_check):
  if len(input_to_check) == 3:
    for data_object in data_array:
      for key, val in data_object.items():
        if val == input_to_check:
          print("Found input value in dataset")
          return True
  else:
    print("Sorry, that was not found. Please try again.")
    return False

    # search in location for input_to_check



def get_query_input():
  # Gets user input for country, data and timeframe
  print("Please enter the country, metric and timeframe for your query.")
  
  print(data_array[0])
  

  while True:
    input_country = format_input(input("Country (ex: Honduras or HND, United States or USA): "))
      
    if validate_input(input_country):
      break
    else:
      continue

  while True:
    input_timeframe = input ("Timeframe (ex: week, month, alltime): ").strip().lower()
    
    if input_timeframe == "week" or input_timeframe == "month" or input_timeframe == "alltime":
      break
    else:
      continue
  
  # TODO: FIX THIS, Broken Validation, Never returns TRUE
  while True:
    input_metric = input("Metric (ex: deaths, cases, postivity) or 'more' to see more options: ").strip().lower()
    
    input_metric = metric_values.get(input_metric)
    print(input_metric)
    print("start validate")

    if validate_input(input_metric):
      break
    else:
      continue

  # input_metric = format_input(input_metric)

  print(input_country)
  # print(input_timeframe)
  # print(input_metric)


def main():
  print("COVID-19 Stats")
  print("----------------------------")
  get_query_input()


if __name__ == '__main__':
  main()

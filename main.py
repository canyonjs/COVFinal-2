# Import Modules
import csv
import update_dataset
import aesthetic_output
import input_handler

# Open dataset .csv and store each row as a dict in array
def parse_dataset(datafile):
  with open(datafile, 'r') as dataset:
    # Array to hold all rows as objects as elements
    temp_data_array = []
    reader = csv.DictReader(dataset)
    for line in reader:
      temp_data_array.append(dict(line))
    return temp_data_array

def build_query():
  # Gets user input for country, data and timeframe parameters
  print("Please enter the country, metric and timeframe for your query.")
  search_terms = []

  search_terms.append(input_handler.get_country(main.data_array))
  search_terms.append(input_handler.get_timeframe())
  search_terms.append(input_handler.get_metric(main.data_array))

  print(aesthetic_output.generate_hzrule(45))

  print("You have selected the following parameters:", "\nCountry:", search_terms[0], "\nTimeframe:", search_terms[1], "\nMetric:", search_terms[2])

  return search_terms

def do_query(query_parameters):
  print(query_parameters[0])
  print(query_parameters[1])
  print(query_parameters[2])
  print("Begin query")
  """
  Search dataset for query parameters
  1) a) Convert map input value to key in the case of country, ex: "HND" : ISO_CODE, "Honduras": "Country" and store key
  b) Use dict.get() for all rows matching that country/iso key, collect them into list of dicts
  2) Convert timeframe input into list of dates backward from current day (ex: map week: [12/01/2020, 12/02/2020,...etc]) save for later user
  3) a) convert metric to formal column title (done)
  b) Perform search of list created in #1, ex: where country/iso = USA and dateofrow = [date in timeframe list], capture numerical value for metric and store in array for output or summation
  """


def main():
  # Dataset primary filename
  owid_dataset = "owid-covid-data.csv"
  # Ensure we are working with latest data, attempt to update if necessary
  working_file = update_dataset.data_freshness(owid_dataset)

  # Parse dataset and store in main class attribute for global access
  main.data_array = parse_dataset(working_file)

  # Print header text and line breaks
  aesthetic_output.generate_header()

  # Get inputs, validate and build query 
  search_strings = build_query()

  # Take response and pass it to search/query function
  do_query(search_strings)

if __name__ == '__main__':
  main()

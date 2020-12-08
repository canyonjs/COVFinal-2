# Import Modules
import csv
import update_dataset
import aesthetic_header
import input_handler
import pickle

# Open dataset .csv and store each row as a dict in array
def parse_dataset(datafile):
  with open(datafile, 'r') as dataset:
    # Return data_array, and valid lists of metrics and ISO/Countries
    
    # Temporary list of dictionary elements
    temp_data_array = []

    # List of countries
    dataset_countries = []

    reader = csv.DictReader(dataset)
    for line in reader:
      temp_line = dict(line)
      temp_data_array.append(temp_line)
      # FIXME: Cache out to file, only do this once per dataset update
      if temp_line.get("location") not in dataset_countries:
        dataset_countries.append(temp_line.get("location"))
      if temp_line.get("iso_code") not in dataset_countries:
        dataset_countries.append(temp_line.get("iso_code"))

    dataset_metrics = [*temp_data_array[0]]

    master_array = []
    master_array.append(temp_data_array)
    master_array.append(dataset_countries)
    master_array.append(dataset_metrics)
    
    # Open file to store serialized list
    pickle_serialize = open("light_datadb.cache", "wb")

    # Dump master_array to file
    pickle.dump(master_array, pickle_serialize)

    # Close pickled file
    pickle_serialize.close()

    return master_array

def create_subset(query_parameters):
  print("Gathering relevant collections of data...")
  """
  Search dataset for query parameters
  1) a) Convert map input value to key in the case of country, ex: "HND" : ISO_CODE, "Honduras": "Country" and store key
  b) Use dict.get() for all rows matching that country/iso key, collect them into list of dicts
  2) Convert timeframe input into list of dates backward from current day (ex: map week: [12/01/2020, 12/02/2020,...etc]) save for later user
  3) a) convert metric to formal column title (done)
  b) Perform search of list created in #1, ex: where country/iso = USA and dateofrow = [date in timeframe list], capture numerical value for metric and store in array for output or summation
  """  
  # Build list of dicts as element where country/ISO matches
  country_entries = []

  for data_element in main.data_array:
    if data_element.get(query_parameters[0][0]) == query_parameters[0][1]:
      country_entries.append(data_element)

  # Review country_entries take only those elements which satisfy our timeframe
  selected_items = []

  for z in country_entries:
    for requested_date in query_parameters[1]:
      if z.get("date") == requested_date:
        selected_items.append(z)
  return selected_items
  
def build_query():
  # Gets user input for country, data and timeframe parameters
  print("Please enter the country, metric and timeframe for your query.")
  search_terms = []

  search_terms.append(input_handler.get_country(main.valid_countries))
  search_terms.append(input_handler.get_timeframe())
  search_terms.append(input_handler.get_metric(main.valid_metrics))

  print(aesthetic_header.generate_hzrule(45))

  print("You have selected the following parameters:", "\nCountry:", search_terms[0], "\nTimeframe:", search_terms[1], "\nMetric:", search_terms[2])

  return search_terms

def main():
  # Dataset primary filename and location
  owid_dataset = "data/owid-covid-data.csv"

  # Ensure we are working with latest data, attempt to update if necessary
  working_file = update_dataset.data_freshness(owid_dataset)

  # Parse dataset and store in main class attribute for global access [INCL ALL ROWS]
  triple_list = parse_dataset(working_file)

  main.data_array = triple_list[0]
  # Build sublist to be used for input validation later
  main.valid_countries = triple_list[1]
  main.valid_metrics = triple_list[2]

  # Print header text and line breaks
  aesthetic_header.generate_header()

  # Get inputs, validate and build strings for query 
  search_strings = build_query()

  # create a subset of only those elements which match user criteria
  main.selected_list = create_subset(search_strings)
  print(main.selected_list)

if __name__ == '__main__':
  main()

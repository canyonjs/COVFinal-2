# Import
import csv
import update_dataset
import aesthetic_header
import input_handler
import pickle
import os
from datetime import datetime
import matplotlib.pyplot as plt

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
      
      if temp_line.get("location") not in dataset_countries:
        dataset_countries.append(temp_line.get("location"))
      if temp_line.get("iso_code") not in dataset_countries:
        dataset_countries.append(temp_line.get("iso_code"))
    
    # Get only keys (valid metrics) from dict
    dataset_metrics = [*temp_data_array[0]]

    master_array = []
    master_array.append(temp_data_array)
    master_array.append(dataset_countries)
    master_array.append(dataset_metrics)
    
    # Open file to store serialized list
    pickle_serialize_file = open("light_datadb.cache", "wb")

    # Dump master_array to file
    pickle.dump(master_array, pickle_serialize_file)

    # Close pickled file
    pickle_serialize_file.close()

    return master_array

def build_query():
  # Gets user input for country, data and timeframe parameters
  print("Please enter the country, metric and timeframe for your query.")
  search_terms = []


  search_terms.append(input_handler.get_country(main.valid_countries))
  user_submitted_timeframe = input_handler.get_timeframe()
  search_terms.append(user_submitted_timeframe[0])
  search_terms.append(input_handler.get_metric(main.valid_metrics))

  print(aesthetic_header.generate_hzrule(45))
  print("\nCountry:", search_terms[0], "\nTimeframe:", user_submitted_timeframe[1], "\nMetric:", search_terms[2],"\n")
  print(aesthetic_header.generate_hzrule(45))

  return search_terms

def create_subset(query_parameters):
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

def run_query(search_list, metric_term):
  # Search narrowed list using search_string[metric] to collect dates and values
  output_dict = {}
  # print(search_list)
  for h in search_list:
    if h.get(metric_term) == "":
      output_dict[h.get("date")] = "0"
    else:
      output_dict[h.get("date")] = h.get(metric_term)

  # Ensure value set is not 0s
  for list_val in list(output_dict.values()):
    if list_val != "0":
      return output_dict
  
  return False

def ending_prompt():
  last_input = input("Would you like to run another query? (y/N): ") 
  
  if last_input == "y" or last_input == "yes":
    main()
  else:
    print("Goodbye! Wear a mask, don't be a statistic.")
    quit()

def generate_graph(data_to_graph, chosen_metric):
  print("Generating graph output...")
  x_axis_dates = [*data_to_graph]
  y_axis_metric = list(data_to_graph.values())
  chosen_metric = chosen_metric.replace("_", " ").title()
  graph_title = chosen_metric + " over " + str(len(x_axis_dates)) + " days."
  
  int_y_axis= []
  # Convert y axis data from str to ints
  for p in y_axis_metric:
    int_y_axis.append(int(float(p)))



  # PLT START
  plt.figure(figsize=(12, 8))

  ax = plt.subplot(111)
  ax.spines["top"].set_visible(False)
  ax.spines["right"].set_visible(False)
  ax.get_xaxis().tick_bottom()
  ax.get_yaxis().tick_left()
  
  plt.xticks(rotation=90, fontsize=14)
  plt.yticks(fontsize=14)
  
  plt.xlabel('Dates', fontsize=16)
  plt.ylabel(chosen_metric, fontsize=16)

  plt.title(graph_title, fontsize=22)
  plt.grid(zorder=0)
  plt.bar(x_axis_dates, int_y_axis, color="#a0c5c4", edgecolor="#2e906e", zorder=3)

  date_today = datetime.now()
  date_today_string = date_today.strftime("%m-%d-%Y, %H:%M:%S")
  save_filename = "output_graphs/" + date_today_string + " - " + chosen_metric + ".png" 

  try:
    plt.savefig(save_filename, bbox_inches="tight")
    print("Graph generated successfully. Check folder output_graphs for file.")
  except:
    print("Sorry, something went wrong, please relaunch the program and try again.")
    quit()

  ending_prompt()
  

def main():
  os.system("clear")
  # Dataset primary filename and location
  owid_dataset = "data/owid-covid-data.csv"

  # Ensure we are working with latest data, attempt to update if necessary
  working_file = update_dataset.data_freshness(owid_dataset)

  # Either parse file from scratch or use pickled bytestream
  if os.path.exists("light_datadb.cache"):
    pickle_deserialize_file = open("light_datadb.cache", "rb")
    triple_list = pickle.load(pickle_deserialize_file)
    pickle_deserialize_file.close()
    print("Loaded cached datafile")
  else:
    triple_list = parse_dataset(working_file)

  # Master list including all rows as dicts
  main.data_array = triple_list[0]

  # Lists of valid countries and metrics in dataset to speed up validation
  main.valid_countries = triple_list[1]
  main.valid_metrics = triple_list[2]

  # Print header text and line breaks
  aesthetic_header.generate_header()

  # Get inputs, validate and build strings for query 
  search_strings = build_query()

  # Create a subset of elements which match user input from build_query()
  main.selected_list = create_subset(search_strings)

  # Query selected list generated by create_subset() with user provided metric
  query_result = run_query(main.selected_list, search_strings[2])

  if not query_result:
    print("Sorry, I don't have data for your requested timeframe and metric.")
    input("Press enter to start over...")
    main()

  # Pass query_result dict to graph output along with chosen metric string for label
  generate_graph(query_result, search_strings[2])


if __name__ == '__main__':
  main()

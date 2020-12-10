# This module handles input formatting, validation and translation
from datetime import datetime, timedelta
import pytz

def format_country(country_input):
  # Format and prepare user input country value for validation and query
  if len(country_input) == 3:
    return country_input.upper()
  else:
    return country_input.title()

def country_iso_construct(valid_term):
  # Construct ('iso_code': value tuple for return from validate_input()
  if len(valid_term) == 3:
    return ("iso_code", valid_term)
  else:
    return ("location", valid_term)

def validate_input(input_to_check, input_type, working_dict):
  # Check to see if formatted country or metric input exists in dataset
  if len(input_to_check) >= 3:
    if input_to_check in working_dict:
      if input_type == "country":
        return country_iso_construct(input_to_check)
      elif input_type == "metric":
        return True
  else:
    return False

def get_country(country_verify):
  # Collect country/ISO code input and validate
  while True:
    input_country = format_country(input("Country/ISO CODE (ex: Honduras/HND, United States/USA): ").strip().lower())

    if len(input_country) < 3:
      print("Enter at least three characters")
      continue
    elif not validate_input(input_country, "country", country_verify):
      print("Sorry,", input_country, "was not found. Please try again.")
      continue
    else:
      return validate_input(input_country, "country", country_verify)

def get_timeframe():
  # Collect desired timeframe for graphing purposes
  while True:
    input_timeframe = input("Timeframe (day, week, month or year): ").strip().lower()
    
    # TODO: Allow for custom timeframe (ex: Februrary 2020 - September 2020)
    if input_timeframe == "week":
      return collect_timeframe_values(input_timeframe, 7)
    elif input_timeframe == "month":
      return collect_timeframe_values(input_timeframe, 30)
    elif input_timeframe == "year":
      return collect_timeframe_values(input_timeframe, 365)
    elif input_timeframe == "day":
      return collect_timeframe_values(input_timeframe, 0)
    elif input_timeframe == "alltime":
      # FIXME: Alltime is broken, not currently necessary, as dataset < 1yr.
      print("Alltime graph is currently disabled, choose another option.")
      continue
      # return collect_timeframe_values(input_timeframe, -1)
    else:
      print("You have selected an invalid timeframe, please try again.")
      continue

def collect_timeframe_values(selected_timeframe, num_of_days):
  # Create list of days/date spanning the requested timeframe
  timeframe_values = []

  # Get current date in EST
  eastern = pytz.timezone("US/Eastern")
  date_today = datetime.now(eastern)

  starting_date = date_today

  if num_of_days == -1:
    print("Error")
    # first_date = date(2020, 1, 1)
    # delta_date = starting_date - first_date
  else:
    ending_date = starting_date - timedelta(days = num_of_days)
    delta_date = starting_date - ending_date
  if num_of_days > 1:
    for i in range(delta_date.days):
      day = ending_date + timedelta(days = i)
      timeframe_values.append(day.strftime("%Y-%m-%d"))
  else:
    yesterday_date = starting_date - timedelta(days = 1)
    timeframe_values.append(yesterday_date.strftime("%Y-%m-%d"))
  return timeframe_values

def get_metric(metric_verify):
  # Collect user input for metric, validate or provide list of options
  while True:
    input_metric = input("Metric (type 'list' to see options): ").strip().lower()

    try:
      # Check if user requested to see available metrics
      if input_metric == "list":
        print("--- Available Metrics ---")
        subsect_full_metric_list = metric_verify[4:32]
        print("You can view descriptions and sources for each of these metrics here:")
        print("https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-codebook.csv")

        print("-------")
        for i in subsect_full_metric_list:
          print(i)
        
        # Ensure metric exists in dataset
      elif validate_input(input_metric, "metric", metric_verify):
        return input_metric
      else:
        print("Invalid metric, please try again or type 'list' to see all options.")
        continue
    except:
      print("Your chosen metric does not appear in the dataset, please try again. Alternatively, type 'list' to see a list of available metrics.")
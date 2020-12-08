from datetime import datetime, timedelta

# Format and prepare user input country value for validation and query
def format_country(country_input):
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

# Check to see if formatted country or metric input exists in dataset
def validate_input(input_to_check, input_type, working_dict):
  if len(input_to_check) >= 3:
    if input_to_check in working_dict:
      if input_type == "country":
        return country_iso_construct(input_to_check)
      elif input_type == "metric":
        return True
  else:
    return False

# TODO: Consider consolidation
def get_country(country_verify):
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
  while True:
    input_timeframe = input("Timeframe (day, week, month, year or alltime): ").strip().lower()
    
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
      # FIXME: Alltime is broken, not currently necessary, dataset is < 1yr.
      print("Alltime graph is currently disabled, choose another option.")
      continue
      # return collect_timeframe_values(input_timeframe, -1)
    else:
      print("You have selected an invalid timeframe, please try again.")
      continue

def collect_timeframe_values(selected_timeframe, num_of_days):
  # Create list of days spanning back the requested timeframe
  """
  FIXME: Timezone difficulties, Repl.it is using their server time. 
  Only works before 7pm. EST :)
  """
  timeframe_values = []

  # Get current date
  date_today = datetime.now()

  starting_date = date_today

  # Create lists of days depending on timeframe chosen
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
  # FIXME: Positive is broken
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
        continue
    except:
      print("Your chosen metric does not appear in the dataset, please try again. Alternatively, type 'list' to see a list of available metrics.")
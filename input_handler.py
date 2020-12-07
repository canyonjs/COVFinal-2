from datetime import datetime, timedelta

# Take informal metric command and return formal column name for query
def translate_metric(metric):
    # Defined commands informal:formal values
    metric_commands = {"deaths": "total_deaths", "cases": "total_cases", "positivity": "positivity_rate", "new": "new_cases"}

    return metric_commands.get(metric)

# Format and prepare user input country value for validation and query
def format_country(country_input):
  if len(country_input) == 3:
    return country_input.upper()
  else:
    return country_input.title()

# Check to see if formatted country or metric input exists in dataset
def validate_input(input_to_check, input_type, working_dict):
  if len(input_to_check) >= 3:
    for data_object in working_dict:
      for key, val in data_object.items():
        if val == input_to_check or key == input_to_check:
          if input_type == "Country:":
            # In the case of country, we're going to need the key for later query
            key_cat_input = key, input_to_check
            return key_cat_input
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
    elif not validate_input(input_country, "Country:", country_verify):
      print("Sorry,", input_country, "was not found. Please try again.")
      continue
    else:
      return validate_input(input_country, "Country:", country_verify)

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
      # FIXME: Alltime is broken, not currently necessary, data set tracks sub 1yr.
      print("Alltime graph is currently disabled, choose another option.")
      continue
      # return collect_timeframe_values(input_timeframe, -1)
    else:
      print("You have selected an invalid timeframe, please try again.")
      continue

def collect_timeframe_values(selected_timeframe, num_of_days):
  # Create list of days spanning back the requested timeframe

  timeframe_values = []
  # Get current date and format string
  # form 2020-01-30
  date_today = datetime.now()
  current_date = date_today.strftime("%Y-%m-%d")

  starting_date = date_today
  print(current_date)

  # return selected_timeframe
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
  while True:
    input_metric = input("Metric (deaths, cases, postivity or 'list' to see more options): ").strip().lower()

    try:
      # Check if user requested to see available metrics
      if input_metric == "list":
        print("--- Available Metrics --")
        print("cases - total case count per day")
        print("deaths - total death count per day")
        print("new - new cases per day")
        print("positivity - daily postitivity rate")
      else:
        # Call translate_metric and get formal column title from informal command
        input_metric = translate_metric(input_metric)
        
        # Ensure metric exists in dataset
        if validate_input(input_metric, "Metric:", metric_verify):
          return input_metric
        else:
          continue
    except:
      print("Your chosen metric does not appear in the dataset, please try again. Alternatively, type 'list' to see a list of available metrics.")
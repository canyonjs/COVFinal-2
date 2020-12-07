from datetime import datetime

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
    input_country = format_country(input("Country/ISO CODE (ex: Honduras or HND, United States or USA): ").strip().lower())

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
    input_timeframe = input("Timeframe (today, week, month, alltime): ").strip().lower()
    
    # TODO: Allow for custom timeframe (ex: Februrary 2020 - September 2020)
    if input_timeframe == "week" or input_timeframe == "month" or input_timeframe == "alltime" or input_timeframe == "today":
      # Going to end up returning the list from collect tf function
      return collect_timeframe_values(input_timeframe)
    else:
      print("You have selected an invalid timeframe, please try again.")
      continue

def collect_timeframe_values(selected_timeframe):
  # Get current date and format string
  # form 2020-01-30
  date_today = datetime.now()
  current_date = date_today.strftime("%Y-%m-%d")
  print(current_date)
  return selected_timeframe
  
  week_values = []
  month_values = []
  day_values = []
  alltime_values = []
  
  # Build list of dates counting back from today
  # This is insanity, use timedelta!

  # if selected_timeframe == "week":
  #   week_values.append(current_date)
  #   slice_day = int(week_values[0][8:])
  #   slice_month = int(week_values[0][5:7])
  #   slice_year = int(week_values[0][0:4])

  #   print(slice_day)
  #   print(slice_month)
  #   print(slice_year)

  #   for i in range(6):
  #     slice_day = slice_day -1
  #     print(str(slice_year) + "-" + str(slice_month) + "-" + str(slice_day))

  # elif selected_timeframe == "month":
  #   print("MONTH LIST")
  # elif selected_timeframe == "today":
  #   print("today")
  # else:
  #   print("alltime")

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
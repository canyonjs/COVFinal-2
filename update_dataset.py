import os
from datetime import datetime

# Downloads dataset and clears terminal (Uncaught, can use subprocess to catch)
def fetch_dataset(datafile):
  # Set fallback incase fetch fails
  fallback_dataset = "12-4BackupDataset.csv"

  os.system("echo Fetching latest dataset...")
  os.system("wget https://covid.ourworldindata.org/data/owid-covid-data.csv")
  os.system("clear")

  # Check to see if the file downloaded, otherwise return backup copy (likely unrelable)

  if os.path.exists(datafile):
    print("Success!")
    os.system("clear")
    return datafile
  else:
    print("There was an issue fetching the latest dataset. The application will use an older copy from 12/4/2020. Check your internet connection.")
    return fallback_dataset

def data_freshness(file_to_check):
  # Get current date and format string
  date_today = datetime.now()
  current_date = date_today.strftime("%m/%d/%Y")

  # Check to see if dataset exists and it is current
  try:
    # Get creation date of csv file and format string
    csv_datetime = datetime.fromtimestamp(os.path.getctime(file_to_check))
    csv_date = csv_datetime.strftime("%m/%d/%Y")

    # Check to see if dataset exists and is up to date, attempt fetch
    if csv_date == current_date:
      return file_to_check
    else:
      print("Dataset is outdated.")
      return fetch_dataset(file_to_check)
  except FileNotFoundError:
    print("Dataset not found.")
    return fetch_dataset(file_to_check)
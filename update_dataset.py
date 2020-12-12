import os
from datetime import datetime


# Downloads dataset and clears terminal
def fetch_dataset(datafile, data_ctime):
    # Set fallback incase fetch fails
    fallback_dataset = "data/old_owid-covid-data.csv"
    """ 
  Use os.system, wget to fetch file 
  (unreliable, does not raise exception from wget, subprocess is a better option)
  """

    os.system("echo Fetching latest dataset...")
    os.system(
        "wget --no-use-server-timestamps https://covid.ourworldindata.org/data/owid-covid-data.csv -O data/owid-covid-data.csv"
    )
    os.system("clear")

    # Check to see if the file downloaded, otherwise return backup copy.
    # (Checking for existence doesn't guarantee non-corruption)

    if os.path.exists(datafile):
        print("Success!")
        # Delete dataset cache file, if we hit this branch then we're getting a new dataset
        print("Clearing cache...")
        try:
            os.remove("light_datadb.cache")
        except FileNotFoundError:
            print("Missing cache file")
        os.system("clear")
        # Pass new file back to data_freshness for verification & timestamp output
        data_freshness(datafile)
        return datafile
    elif os.path.exists(fallback_dataset):
        print(
            "There was an issue fetching the latest dataset. Check your internet connection. In the meantime the script will use a fallback dataset."
        )
        print("Dataset last modified:", data_ctime)
        return fallback_dataset
    else:
        print(
            "Sorry, there was an issue downloading the dataset and there does not appear to be a backup dataset to access. Try adding the dataset manually by placing the .csv file in the folder with the script, then relaunch."
        )
        return False


def data_freshness(file_to_check):
    # Get current date and format string
    date_today = datetime.now()
    current_date = date_today.strftime("%m/%d/%Y")
    try:
        # Check to see if dataset exists and is up to date
        if os.path.exists(file_to_check) and data_timestamp(
                file_to_check) == current_date:
            print("Dataset last modified:", current_date)
            return file_to_check
        else:
            """
      If dataset is present and outdated, collect creation date of that file, rename it old_* (incase we need to fallback after fetch attempt)
      """
            original_dataset = data_timestamp(file_to_check)
            print("Dataset is outdated.")
            os.replace(file_to_check, "data/old_owid-covid-data.csv")
            return fetch_dataset(file_to_check, original_dataset)
    except FileNotFoundError:
        # If there is no dataset at all, try and fetch one.
        print("Dataset not found.")
        return fetch_dataset(file_to_check, "01/01/1970")


def data_timestamp(file_to_timestamp):
    # Get creation date of csv file and format string
    csv_datetime = datetime.fromtimestamp(os.path.getmtime(file_to_timestamp))
    csv_date = csv_datetime.strftime("%m/%d/%Y")

    return csv_date

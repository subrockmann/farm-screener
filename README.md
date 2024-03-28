# farm-screener
## Overview
This project collects data from Swiss farms and helps the user to find direct selling farms in their vicinity by displaying the farms on a map. Due to the fact that the collected data is in German, 

## Checking the live app
You can check out this appliaction live at:  
 https://subrockmann-farm-screener-appapp-f8nbec.streamlit.app/

## Used technologies

- Data collection with Mage 
    - Data source: https://www.hofsuche.schweizerbauern.ch/de
- JSON data was uploaded to GCP bucket for raw data
- JSON files were parsed in Mage and combined into parquet files that are uploaded to GCP bucket for clean data
- Parquet farm data is enriched with geolocations using Open Street Map API https://nominatim.openstreetmap.org/ui/search.html
- The data app is build with streamlit https://streamlit.io/
- The add is hosted on the Streamlit Community Cloud https://streamlit.io/cloud


- All infrastructure is IaC and deployed using Terraform 
## Project setup

### Setup authentication with Google Cloud Platform (GCP) using service account credentials
a. Go to the Google Cloud Console: https://console.cloud.google.com/.

b. Create a new project named "farm-screener" and activate it.

c. Navigate to the "IAM & Admin" > "Service accounts" section.

d. Create a new service account named "farm-screener-service-account". Grant this service account the "Editor" role. (Hint: This should be redefined with tighter permissions, once the project is build and deployed.)

e. Generate a new JSON key for the service account and place it inside the "credentials" folder.

f. Create or modify your .env file with 
````
GOOGLE_APPLICATION_CREDENTIALS="/credentials/<keyfile_name>.json"
````
### Create the GCP infrastructure

From inside the terraform folder to create the infrastructure run:

```
terraform apply
```
To remove the infrastructure run:

```
terraform destroy
```


## Running the streamlit application
```
python -m streamlit run app.py
```

To stop the Streamlit server, press Ctrl+C in the terminal.

## Next steps
- Create product category filters
- Display all products that a farm offers
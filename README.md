## How to use

In the 'src' directory, there is a file named .env with the following properties:  

headless  - If 'true' the selenium browser will open in headless mode otherwise it will open in non-headless mode. (recommended value: true)  

inprivate - If 'true' the selenium browser will open in 'inprivate' (Incognito) mode to prevent saving of cookies by the website. If 'false' the browser will open in   normal mode. (recommended value: true)  

output_csv - This is the name of the output data file which will be saved in the 'data' directory. You can change it according to your wish. Make sure to end the name of the file with '.csv'

start_ind - This is the start index from which the scraper will start scraping data from.  

end_ind - This is the end index till which the scraper will scrape the data. 

# Data Ingestion Pipeline Template

This repository consists of boilerplate folder structure to write and organize your scripts for a data ingestion pipeline

## Folder Structure
The tree diagram below represents a general file structure

```
|--- data_source_name                      
     |--- deploy                            # pipeline orchestration and configuration of DAGs
     |    |---dev              
     |    |---prod
     |--- src
          |--- dependencies
          |    |--- cleaning
          |    |    |--- __init__.py
          |    |    |--- cleaner.py         ## Cleaning script here
          |    |--- geocoding
          |    |    |--- __init__.py
          |    |    |--- geocoder.py        ## Geocoding script here
          |    |--- scraping                # This folder contains all data harvesting scipts
          |    |    |--- __init__.py
          |    |    |--- scraper.py         ## Harvesting script here
          |    |--- standardization
          |    |    |--- __init__.py
          |    |    |--- standardizer.py    ## Standardization script here
          |    |--- utils                   # Utility and helper scipts to be placed here
          |         |--- __init__.py
          |--- .dockerignore
          |--- Dockerfile
          |--- client.py                    # Master script that connects all the above blocks
          |--- requirements.txt
```

## Different Blocks of ETL pipeline
1. Scraping/Data Harvesting
    - Contains all the scripts that extracts metadata and raw data to be processed further from database, websites, webservices, APIs, etc.
2. Cleaning
    - Treatment missing fields and values
    - Conversion of amounts to USD
    - Treatment of duplicate entries
    - Convert country codes to `ISO 3166-1 alpha3` i.e. 3 letter format
    - Identify region name and region code using the country code
3. Geocoding
    - Based upon location information available in the data
        - Location label
        - Geo-spatial coordinates
    - Missing field can be found either by using geocoding or reverse geocoding with max precision available
4. Standardization
    - Fields to be strictly in **lower snake casing**
    - Taking care of data types and consistency of fields
    - Standardize fields like `sector` and `subsector`
    - Mapping of `status` and `stage`
    - Renaming of field names as per required standards
    - Manipulation of certain fields and values to meet up the global standards for presentation, analytics and business use of data
    - Refer to the [Global Field Standards](https://docs.google.com/spreadsheets/d/1sbb7GxhpPBE4ohW6YQEakvrEkkFSwvUrXnmG4P_B0OI/edit#gid=0) spreadsheet for the standards to be followed

### Note
> Depending upon what fields are already available in the data `GEOCODING` step may or may not be required.

> It is recommended that the resultant data after each and every step is stored and backed up for recovery purpose.

> Apart from the primary fields listed down in [Global Field Standards](https://docs.google.com/spreadsheets/d/1sbb7GxhpPBE4ohW6YQEakvrEkkFSwvUrXnmG4P_B0OI/edit#gid=0) spreadsheet, there are several other secondary fields that are to be scraped; given by the data provider for every document that holds significant business importance.

## Get started with
- Fork the repository by clicking the `Fork` button on top right-hand side corner of the page.
- After creating fork repo, create a branch in that repo and finally create a `PULL REQUEST` from fork repo branch to the main branch in upstream branch of root repo.


### Submission and Evaluation
- For assignment submission guidelines and evaluation criteria refer to the [WIKI](https://github.com/Taiyo-ai/pt-mesh-pipeline/wiki) documentation

---
Copyright © 2021 Taiyō.ai Inc.

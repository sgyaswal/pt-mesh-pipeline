import dotenv
import logging
from datetime import datetime

from dependencies.scraping.scraper import Scraper
from dependencies.cleaning.cleaning import Cleaning
from dependencies.standardization.standardizer import Standardization

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# In each step, create an object of the class, initialize the class with
# required configuration, and call the run method

def step_1():
    scraper = Scraper()
    scraper.crawler()
    logging.info("Scraped Metadata")


def step_2():
    cleaning = Cleaning()
    cleaning.cleaning()
    cleaning.saving()
    logging.info("Cleaned Main Data")


def step_3():
    logging.info("Geocoded Cleaned Data")


def step_4():
    standardization = Standardization()
    standardization.snake_case()
    standardization.saving()
    logging.info("Standardized Geocoded Data")



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="step to be chosen for execution")

    args = parser.parse_args()

    # Define a list of step functions
    steps = [step_1, step_2, step_3, step_4]

    # If a specific step is provided, execute only that step
    if args.step is not None:
        try:
            step_number = int(args.step)
            if 1 <= step_number <= len(steps):
                steps[step_number - 1]()
                logging.info(
                    {
                        "last_executed": str(datetime.now()),
                        "status": "Step executed successfully",
                    }
                )
            else:
                logging.error("Invalid step number.")
        except ValueError:
            logging.error("Invalid step number format.")
    else:
        # If no specific step is provided, execute all steps one by one
        for step_number, step_func in enumerate(steps, start=1):
            logging.info(f"Executing Step {step_number}...")
            step_func()
            logging.info(f"Step {step_number} completed successfully.")

    logging.info(
        {
            "last_executed": str(datetime.now()),
            "status": "Pipeline executed successfully",
        }
    )

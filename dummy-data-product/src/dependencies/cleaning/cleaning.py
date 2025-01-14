import pandas as pd
import os
from dotenv import load_dotenv

class Cleaning:
    def __init__(self):
        # reading and loading data from .env file
        self.output_name = os.environ.get('output_csv')
        self.df = None
        
        # reading the data csv file
        self.df = pd.read_csv('../../data/' + self.output_name, encoding='utf-16', delimiter='\t')
    
    def __fill_null(self,value='NA'):
        self.df.fillna(value)
    
        
    def __datetime(self,column):
        self.df[column] = pd.to_datetime(self.df[column], errors='coerce')
    
    def cleaning(self):
        # filling null values
        self.__fill_null()
        
        
        
        # converting dates to datetime format
        self.__datetime('Published Date')
        self.__datetime('Bid Opening Date')
        self.__datetime('Document Download / Sale Start Date')
        self.__datetime('Document Download / Sale End Date')
        self.__datetime('Bid Submission Start Date')
        self.__datetime('Bid Submission End Date')
        
    def saving(self):
        self.df.to_csv('../../data/' + self.output_name, encoding='utf-16',sep='\t', index=False)
        
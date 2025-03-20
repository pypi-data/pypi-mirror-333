import requests
import sys
import json
from hermeslib import hutils
from datetime import datetime, timedelta, date
import pandas as pd

base_url = "https://hermes.phinergy.biz/api"

class Units:
    
    def __init__(self, session):
        self.session = session
        self.url = f'{base_url}/units'
        self.units = None
        
    def get_units(self):
        """
        Retrieves units from the API.
        Returns:
            pandas.DataFrame: The units data retrieved from the API.
        """
        
        query = {"query$": "{}", "sort$": '{"zone":1}'}
        response = self.session.request('get', self.url, params=query)
        
        hutils.check_status(response)
        
        json_response = response.json()
        data = json_response['data'] 
        self.units = pd.DataFrame(data)                            
        return self.units
        
    def get_unit_programs(self, unit_name, date):
        """
        Retrieves unit programs for a given unit name and date and returns the data as a pandas DataFrame.        
        Args:
            unit_name (str): The name of the unit
            date (str): The date in the format 'YYYY-MM-DDTHH:MM:SSZ'
        
        Returns:
            pandas.DataFrame: The unit programs data
        """
        
        
        date = hutils.formatting_date(date).strftime('%Y-%m-%dT%H:%M:%SZ')         
        params = {
            'date': date
        }
        
        url = f'{self.url}/{unit_name}/profile-offers-overview'
        response = self.session.request('get', url, params=params)
       
        hutils.check_status(response)
                
        json_response = response.json()
        data = json_response['data']        
        unit_programs = pd.DataFrame(data)
        return unit_programs    
        
        
    def get_unit_margins(self, unit_id, date):
        """
        Retrieve unit margins for a given unit and date.
        Args:
            unit_id (str): The ID of the unit.
            date (str): The date for which margins are to be retrieved.

        Returns:
            pandas.DataFrame: A DataFrame containing the unit margins.
        """
        
        
        date = hutils.formatting_date(date).strftime('%Y-%m-%dT%H:%M:%SZ')         
        params = {
            'flow_date': date
        }
        
        url = f'{self.url}/{unit_id}/margins'
        response = self.session.request('get', url, params=params)
        
        hutils.check_status(response)
        
        json_response = response.json()
        data = json_response['data']        
        unit_margins = pd.DataFrame(data)
        return unit_margins    
        

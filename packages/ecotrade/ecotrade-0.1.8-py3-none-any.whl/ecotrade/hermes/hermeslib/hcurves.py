import requests
import sys
import json
from hermeslib import hutils
from datetime import datetime, timedelta, date
import pandas as pd

base_url = "https://hermes.phinergy.biz/api"

class Curves:

    def __init__(self, session):
        self.session = session
        self.url = f'{base_url}/bidder/curves'
        self.curves = None
        
    
    def get_curves(self):
        """
        Retrieves curves from the API and returns the curve data as a pandas DataFrame. 
        Returns:
            pandas.DataFrame: The curve data.
        """
        
        response = self.session.get(self.url)
        
        hutils.check_status(response)
        
        json_response = response.json()
        data = json_response['data']   
        self.curves = pd.DataFrame(data)
            
        return self.curves
       
        
                  
    def get_curve_values(self, curve_id, startdate, stopdate):
        """
        Retrieves values for a specific curve within a specified time range.
        Parameters:
            curve_id (int): The ID of the curve for which the values are desired.
            startdate (datetime): The start time of the time range.
            stopdate (datetime): The stop time of the time range.
        Returns:
            DataFrame: The values in a pandas DataFrame format if the request is successful, 
            otherwise returns None.
        """
        
        startdate = hutils.formatting_date(startdate)
        stopdate = hutils.formatting_date(stopdate)

        stopdate = hutils.formatting_date(stopdate).strftime('%Y-%m-%dT%H:%M:%SZ')
        startdate = hutils.formatting_date(startdate).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        query = {
            'query$'  : json.dumps({
                'date'  : {
                    '$gte'  : startdate,
                    '$lt'   : stopdate
                }
            })
        }    
       
        response = self.session.request(
            'get',
            f'{self.url}/{curve_id}/values',
            params=query
        )
        
        hutils.check_status(response)
        
        json_response = response.json()
        data = json_response['data']['curve_values']   
        curve_values = pd.DataFrame(data[::-1])
        return curve_values
        
        
                    
    def post_curve_values(self, curve_id, payload):
        """
        Posts values for a specific curve.
        Parameters:
            curve_id (int): The ID of the curve for which the values are to be posted.
            payload (dict): The values to be posted.
        Returns:
            dict: The response from the API.
        """
        
        response = self.session.request(
        'post', f'{self.url}/{curve_id}/values', json=payload)
        
        hutils.check_status(response)
        
        json_response = response.json()            
        return json_response

        

import requests
import sys
import json

from HermesData.hermeslib import hutils
from datetime import datetime, timedelta, date
import pandas as pd

base_url = "https://hermes.phinergy.biz/api"

class Xbid:
    
    def __init__(self, session):
        self.session = session
        self.trades = None
        self.orders = None
        self.nomination = None
        self.book = None
        self.warranty = {}
        
    def get_trades(self, date, mytrades = True):
        """
        Retrieves trades for a given date from the API and returns the trade data as a pandas DataFrame. 
        Args:
            date (str): The date for which to retrieve the trades in the format 'YYYY-MM-DD'.
        Returns:
            pandas.DataFrame: The trade data for the specified date.
        """
        
        date = hutils.formatting_date(date)
               
        delta = timedelta(days=1)
        date = date - delta 

        payload = {
            "flow_date": date.strftime('%Y-%m-%dT%H:%M:%SZ'),    
        }

        if mytrades == True:
            url = f'{base_url}/trades'
        else:
            url = f'{base_url}/trades/all'
        
        response = self.session.request('get', url, payload)
        
        hutils.check_status(response)
        
        json_response = response.json()
        data = json_response['data']   
                  
        self.trades = pd.DataFrame(data)
        #print(self.trades['flow_date'])
        self.trades['flow_date'] = pd.to_datetime(self.trades['flow_date']) 
        if 'buyer_hermes_txt' in self.trades.columns:
            self.trades.drop(['buyer_hermes_txt'], axis=1, inplace=True)
        if 'seller_hermes_txt' in self.trades.columns:
            self.trades.drop(['seller_hermes_txt'], axis=1, inplace=True)    
        self.trades.reset_index(drop=True, inplace=True)      
                        
        return self.trades
        
        
    def get_orders(self, date):
        """
        Retrieves orders for a given date from the API and returns the order data as a pandas DataFrame. 
        Args:
            date (str): The date for which to retrieve the orders in the format 'YYYY-MM-DD'.
        Returns:
            pandas.DataFrame: The order data for the specified date.
        """
        
        date = hutils.formatting_date(date)
               
        delta = timedelta(days=1)
        date = date - delta 

        payload = {
            "flow_date": date.strftime('%Y-%m-%dT%H:%M:%SZ'),    
        }

        url = f'{base_url}/orders'
        response = self.session.request('get', url, payload)
        
        hutils.check_status(response)
        
        json_response = response.json()
        data = json_response['data']   
           
        self.orders = pd.DataFrame(data)         
        self.orders['flow_date'] = pd.to_datetime(self.orders['flow_date']) + pd.Timedelta(days=1)
        self.orders.reset_index(drop=True, inplace=True)      
                        
        return self.orders
          
    
    def get_nominations(self, date):
        """
        Retrieves nominations for a given date from the API and returns the nomination data as a pandas DataFrame. 
        Args:
            date (str): The date for which to retrieve the nominations in the format 'YYYY-MM-DD'.
        Returns:
            pandas.DataFrame: The nomination data for the specified date.
        """
        
        date = hutils.formatting_date(date)
               
        delta = timedelta(days=1)
        date = date - delta 

        payload = {
            "flow_date": date.strftime('%Y-%m-%dT%H:%M:%SZ'),    
        }

        url = f'{base_url}/programs'
        response = self.session.request('get', url, payload)
       
        hutils.check_status(response)
       
        json_response = response.json()
        data = json_response['data']   
           
        self.nominations = pd.DataFrame(data)         
        self.nominations['flow_date'] = pd.to_datetime(self.nominations['flow_date']) + pd.Timedelta(days=1)
        self.nominations.reset_index(drop=True, inplace=True)      
                        
        return self.nominations
        
              
    def get_book(self, unit_id, date, hour):
        """
        Retrieves book for a given unit and date from the API and returns the book data as a pandas DataFrame. 
        Args:
            unit_id (int): The ID of the unit for which to retrieve the book.
            date (str): The date for which to retrieve the book in the format 'YYYY-MM-DD'.
            hour (str): The hour for which to retrieve the book in the format 'HH'.
        Returns:
            pandas.DataFrame: The book data for the specified unit and date.
        """
        
        date = hutils.formatting_date(date)
               
        delta = timedelta(days=1)
        date = date - delta 

        payload = {
            "flow_date": date.strftime('%Y-%m-%dT%H:%M:%SZ'),   
            "hour": hour
        }

        url = f'{base_url}/units/{unit_id}/xbid-book-profile'
        response = self.session.request('get', url, payload)
        
        hutils.check_status(response)
                
        json_response = response.json()
        data = json_response['data']   
           
        self.book = pd.DataFrame(data)                              
        return self.book
        
        
    def get_warranty(self, date):
        """
        Retrieves warranty for a given date from the API and returns the warranty data as a pandas DataFrame. 
        Args:
            date (str): The date for which to retrieve the warranty in the format 'YYYY-MM-DD'.
        Returns:
            pandas.DataFrame: The warranty data for the specified date.
        """
        
        date = hutils.formatting_date(date)
               
        delta = timedelta(days=1)
        date = date - delta 

        payloads = []
        payload_report = {
            "flow_date": date.strftime('%Y-%m-%dT%H:%M:%SZ') 
            }
        payloads.append(payload_report)
        
        payload_collateral = {}        
        payloads.append(payload_collateral)
                
        list_url = ['reports', 'details']
        list_db = ['Reports', 'Collaterals']
        
        for item, url in enumerate(list_url):
            
            current_url = f'{base_url}/warranty/{url}'
            response = self.session.request('get', current_url, params=payloads[item])
            
            hutils.check_status(response)
            
            json_response = response.json()
            data = json_response['data']                   
            self.warranty[f'{list_db[item]}'] = pd.DataFrame(data)                              

        return self.warranty
        
           
#import required libraries
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import numpy as np

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''

    #current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    #Open or create log file and append the log meesage
    with open('code_log.txt', 'a') as file1:
        file1.write(timestamp + ':' + message + "\n")

def extract(BankListURL):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''

    log_progress("Extraction Started")

    try:
        #define a dataframe for storing Bank details table data
        BankListdf = pd.DataFrame(columns=['Name','MC_USD_Billion'])
        #getting response from url
        response = requests.get(BankListURL)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
   
        #heading to identify the table
        heading_text = "By market capitalization"
        table = None

        #find the heading text
        heading_element = soup.find(lambda tag: tag.name in ['h2'] and heading_text in tag.text)

        #find tables under heading text
        if heading_element:
            table = heading_element.find_next('tbody')

        # check if any tables are found 
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td') 
                if len(cols)!=0:
                    data_dict = {"Name": cols[0].text.replace('\n',""),
                            "MC_USD_Billion": cols[2].text.replace('\n',"")}
                    df1 = pd.DataFrame(data_dict, index=[0])
                    print(df1)
                    BankListdf = pd.concat([BankListdf,df1], ignore_index=True)

         
            print(BankListdf.head(5))
            log_progress (" Data extraction complete. Initiating Transformation process")
            
            return BankListdf
        else:
            return pd.DataFrame()

    except Exception as e:
        log_progress(str(e))

        
    

def transform(BankListdf,exchangeRateCSVURL):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''

    try:
        #dataframe for exchange rate
        exchangeRateCSVdf = pd.read_csv(exchangeRateCSVURL)
        log_progress(exchangeRateCSVdf.describe().to_string())
        print(exchangeRateCSVdf)

        #copy relevant data from BankListdf into new df for tranformation
        transformeddf = BankListdf[['Name','MC_USD_Billion']].copy()

        #convert datatype to numeric for MC_USD_Billion
        print("Datatypes of columns \n",transformeddf.dtypes)
        transformeddf['MC_USD_Billion'] =  pd.to_numeric(transformeddf['MC_USD_Billion'],errors = 'coerce')
        print("Updated Datatypes of columns \n ",transformeddf.dtypes)

        #get the conversion rates from exchange rates
        GBPConversionRate = exchangeRateCSVdf.loc[exchangeRateCSVdf['Currency'] == 'GBP', 'Rate'].values
        EURConversionRate = exchangeRateCSVdf.loc[exchangeRateCSVdf['Currency'] == 'GBP', 'Rate'].values
        INRConversionRate = exchangeRateCSVdf.loc[exchangeRateCSVdf['Currency'] == 'GBP', 'Rate'].values

        #Add and calculate values for each row
        transformeddf['MC_GBP_Billion'] = transformeddf['MC_USD_Billion'] / GBPConversionRate
        transformeddf['MC_EUR_Billion'] = transformeddf['MC_USD_Billion'] / EURConversionRate 
        transformeddf['MC_INR_Billion'] = transformeddf['MC_USD_Billion'] / INRConversionRate  
        
        #round to 2 decimal points
        transformeddf['MC_GBP_Billion'] = transformeddf['MC_GBP_Billion'].round(2)
        transformeddf['MC_EUR_Billion'] = transformeddf['MC_EUR_Billion'].round(2)
        transformeddf['MC_INR_Billion'] = transformeddf['MC_INR_Billion'].round(2)

        log_progress("Data transformation complete. Initiating Loading process")
        print("transformed DataFrame : \n",transformeddf.head(2))

        return transformeddf
    
    except Exception as e :
        log_progress(str(e))


def load_to_csv(transformeddf,output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''

    log_progress("Loading Data into CSV file")

    try:
        #loading transformed data into CSV file
        transformeddf.to_csv(output_path,index = False)
        log_progress("Data saved to CSV file")
    
    except Exception as e:
        log_progress (str(e))
    

def load_to_db(transformeddf,sql_connection,table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''

    try:
        # output data to table
        transformeddf.to_sql(table_name, sql_connection, if_exists = 'replace', index = False)
        log_progress("Data loaded to Database as a table, Executing queries")

    except Exception as e:
        log_progress(str(e))
 
def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    try :
        #take cursor to execute queries
        cursor = sql_connection.cursor()

        #execute the query
        print(query_statement)
        cursor.execute(query_statement)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cursor.close()
    except Exception as e:
        log_progress(str(e))



''' define the required entities and call the relevant functions in the correct order to complete the project. Note that this
portion is not inside any function.'''
#URL for extracting bank list
BankListURL = 'https://en.wikipedia.org/wiki/List_of_largest_banks'
#URL to extract Exchange rate CSV
exchangeRateCSVURL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv"
#output CSV path
output_path = "Largest_banks_data.csv"
#table_name for storing output in database
table_name = "Largest_banks"
    
    
log_progress("Preliminaries complete. Initiating ETL process")
    
#call extract function to extract data
df = extract(BankListURL)

# call transform fucntion to calculate different currencies
transformeddf = transform(df,exchangeRateCSVURL)

#call load function to load the output into CSV file
load_to_csv(transformeddf,output_path)

#connect ore create database
sql_connection = sqlite3.connect('Banks.db')
log_progress("SQL Connection initiated")

#call load function to load the output into db
load_to_db(transformeddf,sql_connection,table_name)

log_progress("running queries")

#run query statements
run_query("SELECT * FROM Largest_banks",sql_connection)
run_query("SELECT AVG(MC_GBP_Billion) FROM Largest_banks",sql_connection)
run_query("SELECT Name from Largest_banks LIMIT 5",sql_connection)

log_progress("Process Complete")
sql_connection.close()
log_progress("Server Connection closed")



    
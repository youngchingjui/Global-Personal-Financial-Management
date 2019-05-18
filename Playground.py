# Python Playground    

# From terminal, try this command if all else doesn't work:
#iconv -f [ENCODER FROM] -t UTF-8 [FILENAME]
#file --mime [FILENAME]

import codecs
import os
import chardet
import cchardet
import pandas as pd
from datetime import datetime, timezone
import pytz
import pymysql
import mysql.connector
import os

filename = "Raw/Alipay/20180419_20190419_ACCLOG.csv"

# Method to connect to AWS MySQL database
def connect_aws_db():
  host = "pfm-rdbs-instance.cd5ryppsxnnf.ap-northeast-2.rds.amazonaws.com"
  port = 3306
  dbname = 'pfmdatabase'
  user = 'pfmrdbsuser'
  password = os.environ['PFMDBPW']

  conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
  return conn

# Try to extract the Alipay file with the right codec
def extract_file(filename):

  with open(filename, 'rb') as f: 
    data = f.read()

    # List of possible encodings. Ordered by most comprehensive
    encodings = ['GBK', 'EUC-CN', 'GB18030', 'CP936', 'BIG5-HKSCS', 'CN-GB', 'HZ', 'EUC-TW', 'BIG5', 'CP950', 'BIG5-HKSCS:2004', 'BIG5-HKSCS:2001', 'BIG5-HKSCS:1999', 'ISO-2022-CN', 'ISO-2022-CN-EXT']
    for encoding in encodings:
      try:
        print("Trying to encode with: {}".format(encoding))
        result = data.decode(encoding)
        print("Success with encoding using encoding: {}".format(encoding))

        # If success, then return this file
        return result

      except Exception as e:
        print("Error with encoding: {}".format(encoding))
        print(e)
        continue
    
    return None

def save_to_bucket(data):
  #TODO
  # Connect to cloud bucket to store this file

  pass
  
def get_header_data(data):
  # Extract header data, including the following:
  # - Account name
  # - Datetime of .csv (from - to)
  # - Download time

  # For now, I'll assume all times are in Shanghai time. Keep an eye out if this is not true
  tz = pytz.timezone('Asia/Shanghai')
  time_format = '%Y-%m-%d %H:%M:%S'

  # Get the account_name
  lookup_string3 = '\n#账户名\n：'
  lookup_string4 = '\n#自['
  account_name = data.split(lookup_string3)[1]
  account_name = account_name.split(lookup_string4)[0]

  # Get the date_range of the transactions
  lookup_string6 = ']至['
  lookup_string7 = ']\n#成功总金额：['

  date_range_from = data.split(lookup_string4)[1]
  date_range_from = date_range_from.split(lookup_string6)[0]
  date_range_from = datetime.strptime(date_range_from, time_format)
  date_range_from = tz.localize(date_range_from)

  date_range_to = data.split(lookup_string6)[1]
  date_range_to = date_range_to.split(lookup_string7)[0]
  date_range_to = datetime.strptime(date_range_to, time_format)
  date_range_to = tz.localize(date_range_to)

  # Get the download time
  lookup_string1 = '#下载时间：['
  lookup_string2 = ']\n#----------------------------------------收支明细列表'
  download_time = data.split(lookup_string1)[1]
  download_time = download_time.split(lookup_string2)[0]
  download_time = datetime.strptime(download_time, time_format)
  download_time = tz.localize(download_time)

  # Package up the above 3 variables into the header_data dictionary
  header_data = dict()
  date_range = dict()
  date_range['from'] = date_range_from
  date_range['to'] = date_range_to
  header_data['date_range'] = date_range
  header_data['download_time'] = download_time
  header_data['account_name'] = account_name

  return header_data

def formatData(data):
  # Returns Alipay downloaded statements in a readable format, easy for parsing in a table format

  # Inputs:
  # Data: A .csv formatted file that is already decoded properly

  # Returns: A Pandas datatable
  
  look_for_string = '#----------------------------------------收支明细列表----------------------------------------\n'
  formatted_data = data.split(look_for_string)[1]

  # Remove the random '\t's from the file
  formatted_data = formatted_data.replace('\t','')
  
  # Read each row (split by '\n') into a DataFrame
  data_pd = pd.DataFrame([x.split(',') for x in formatted_data.split('\n')])
  
  # Set column headers as first row of table and drop first row
  data_pd.columns = data_pd.iloc[0]
  data_pd = data_pd.reindex(data_pd.index.drop(0))

  return data_pd

def saveData(data) :
  # Saves data into a specified database
  
  # Inputs:
  # data: a Pandas datatable

  # Returns: None

  # TODO: Build this method
  pass

def save_to_metadata_table(header_data):
  #TODO
  # Adds row of header data to database
  # Checks if this file has already been added before. If so, it does not add the row.
  # If this is not duplicate, then is_new = True. If it is duplicate, method returns false.

  # Returns: is_new, indicating whether this file was previously already uploaded
  
  print("Saving metadata to MySQL db")
  conn = connect_aws_db()
  cur = conn.cursor()
  datetime_format = '%Y-%m-%d %H:%M:%S'
  datetime_format_ms = '%Y-%m-%d %H:%M:%S.%f'
  utc = timezone.utc

  # Pull out all of the variables from header_data
  account_name = header_data.get('account_name')
  date_range_from = header_data.get('date_range').get('from')
  date_range_to = header_data.get('date_range').get('to')
  download_time = header_data.get('download_time')

  # Check if this file has been saved before. If so, set is_new = False
  is_new = True
  query = "SELECT * FROM pfmdatabase.alipay_header WHERE account_name=%s AND date_range_from=%s AND date_range_to=%s AND download_time=%s"

  # Make sure to save all the dates in UTC format
  cur.execute(query, (account_name, date_range_from.astimezone(tz=utc).strftime(datetime_format), date_range_to.astimezone(tz=utc).strftime(datetime_format), download_time.astimezone(tz=utc).strftime(datetime_format)))
  rows = cur.fetchall()
  if len(rows) > 0:
    is_new = False

  # Save metadata to table, even if it might be duplicate
  # Record timestamp of when we're uploading this
  insertStatement = "INSERT INTO pfmdatabase.alipay_header (account_name, date_range_from, date_range_to, download_time, datetime_uploaded) VALUES(%s, %s, %s, %s, %s)"
  cur.execute(insertStatement, (account_name, date_range_from.astimezone(tz=utc).strftime(datetime_format), date_range_to.astimezone(tz=utc).strftime(datetime_format), download_time.astimezone(tz=utc).strftime(datetime_format), datetime.now().astimezone(tz=utc).strftime(datetime_format_ms)))
  conn.commit

  conn.close()
  return is_new

# Get the data from the file
data = extract_file(filename)

# Save the converted file (now in UTF-8 format) to bucket
save_to_bucket(data)

# Get header data from file
header_data = get_header_data(data)
print(header_data)
# Save the header_data to metadata table
is_new = save_to_metadata_table(header_data)

# Extract and structure the data
data = formatData(data)

# Save the data locally for now. 
# TODO: Take this out when no longer needed
data.to_csv('sample_output.csv')

# Save the data into a database (TBD)
saveData(data)


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
  """
  Connects to our database on AWS

  Args:
    None

  Returns:
    conn (Connection): Our connection object to execute SQL statements

  TODO: 
    Refactor so host, port, dbname, user, and password can be interchanged.
    Consider, if re-factored, do we need this method?
  """
  
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
  """
  Saves the decoded raw file to a bucket Google Cloud Platform

  args:
    data (string): Alipay transaction data, including all of the header data. Data should be decoded

  returns:
    None

  TODO: Connect to cloud bucket to store this file
  """
 
  pass
  
def get_header_data(data):
  """
  Extracts Alipay transaction file header data, including the following:
    - Account name
    - Datetime of .csv (from - to)
    - Download time

  Args:
    data (string): Raw, decoded Alipay transaction data

  Returns:
    header_data (dict): Dictionary with the following structure:
      - account_name: String
      - date_range: Struct
          - from: datetime
          - to: datetime
      - download_time: datetime
  """
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

def extract_transactions(data):
  """
  Strips out file header data, and returns Alipay transactions in a Pandas DataFrame format

  Args:
    Data (string): All Alipay transactions and corresponding column headers at top. Transactions must be properly coded, and the file header information is stripped out.

  Returns: 
    data_pd (DataFrame): A Pandas datatable with all transactions
  """
  
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

def restructure_transactions(data):
  """
  Restructures transaction data in a better way to conduct analysis. Following is done:
  - Converts 时间 column to datetime format
  - Creates new column that determines if a transaction is one of the following categories:
    - 转账 (transfer)
    - 支付 (payment)
    - 收款 (deposit)
    - 在线支付 (online payment)
  - Extracts vendor name and/or details from 名称 column
  - Combines 收入 and 支出 columns into a single column. Since Alipay is an asset account (not a liability), debits will be positive and credits will be negative

  """

  return data


def saveData(data):
  """
  Saves Alipay transaction data into a specified database
  
  Args:
    data (DataFrame): 

  Returns
    None

  TODO: 
    Build out this method
  """

  pass

def save_to_metadata_table(header_data):
  """
  Adds the header_data to our pfmdatabase.alipay_header database.
  If this file has already been added before, does not add the header_data and returns is_new=False
  Checks existing rows if ALL of the following match:
    - account_name
    - date_range_from
    - date_range_to
    - download_time

  Datetime values are converted and saved in database in UTC timezone

  Args:
    header_data: Data from the header of alipay transaction downloads. Header_data should have the following dictionary structure:
      - account_name: String
      - date_range: Struct
          - from: datetime
          - to: datetime
      - download_time: datetime

  Returns: 
    is_new (bool): indicates whether header_data is already saved in the database
  """
  
  print("Saving metadata to MySQL db")
  conn = connect_aws_db()
  cur = conn.cursor()
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
  cur.execute(query, (account_name, date_range_from.astimezone(tz=utc), date_range_to.astimezone(tz=utc), download_time.astimezone(tz=utc)))
  rows = cur.fetchall()
  if len(rows) > 0:
    print("Found duplicate entry")
    is_new = False

  # If similar entry was not found, continue to save this new entry
  else :
    # Save metadata to table, even if it might be duplicate
    # Record timestamp of when we're uploading this
    insertStatement = "INSERT INTO pfmdatabase.alipay_header (account_name, date_range_from, date_range_to, download_time, datetime_uploaded) VALUES(%s, %s, %s, %s, %s)"
    cur.execute(insertStatement, (account_name, date_range_from.astimezone(tz=utc), date_range_to.astimezone(tz=utc), download_time.astimezone(tz=utc), datetime.now().astimezone(tz=utc)))
    
    conn.commit()

  conn.close()
  return is_new

def extract_balances(data):
  """
  Extracts point-in-time balance data from Alipay transactions sheet.
  Not all financial institutions provides this. Alipay does, so we'll save it.

  Args:
    data (pandas DataFrame): DataFrame containing Alipay transactions. Must include the 账户余额（元）column

  Returns:
    balances (pandas DataFrame): DataFrame with the following columns:
      - 时间
      - 账户余额（元）
  """

  # TODO: Double check this code works
  balances = data.columns(['时间', '账户余额（元）'])
  return balances

def save_balance_data(balances):
  """
  Saves our Alipay point-in-time balance data to pfmdatabase.balances database

  Args:
    balances (DataFrame): a pandas DataFrame containing the following columns: 
      - 时间
      - 账户余额（元）
  
  Returns:
    None
  """

  # Connect to the database
  conn = connect_aws_db()
  cur = conn.cursor()
  utc = timezone.utc

# Get the data from the file
data = extract_file(filename)

# Save the converted file (now in UTF-8 format) to bucket
save_to_bucket(data)

# Get header data from file
header_data = get_header_data(data)
print("Our header data: {}".format(header_data))

# Save the header_data to metadata table
is_new = save_to_metadata_table(header_data)

# Extract transactions
data = extract_transactions(data)

# Restructures the data so that it's more uniform and we can conduct analysis on the data
data = restructure_transactions(data)

# Extract point-in-time balances from each transaction
balances = extract_balances(data)

# Save balances in database
save_balance_data(balances)

# Save the data locally for now. 
# TODO: Take this out when no longer needed
data.to_csv('sample_output.csv')

# Save the data into a database (TBD)
saveData(data)


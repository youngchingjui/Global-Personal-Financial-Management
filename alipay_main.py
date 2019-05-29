# main.py

import alipay

filename = "Raw/Alipay/20180419_20190419_ACCLOG.csv"

# Get the data from the file
data = alipay.extract_file(filename)

# Save the converted file (now in UTF-8 format) to bucket
alipay.save_to_bucket(data)

# Get header data from file
header_data = alipay.get_header_data(data)
print("Our header data: {}".format(header_data))

# Save the header_data to metadata table
is_new = alipay.save_to_metadata_table(header_data)

# Extract transactions
data = alipay.extract_transactions(data)

# Restructures the data so that it's more uniform and we can conduct analysis on the data
data = alipay.restructure_transactions(data)

# Extract point-in-time balances from each transaction
balances = alipay.extract_balances(data)

# Save balances in database
alipay.save_balance_data(balances)

# Save the data locally for now. 
# TODO: Take this out when no longer needed
data.to_csv('sample_output.csv')

# Save the data into a database (TBD)
alipay.save_to_transactions_table(data)
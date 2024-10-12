import os
import sys
import pandas as pd
import numpy as np

# search path for modules 
sys.path.append(os.path.abspath("../src"))
DATAPATH = "./data"
SRC= "../src"

#File path
input_file_path = os.path.join(DATAPATH, "languages.csv")

# Reading the CSV file into a pandas DataFrame
Original_data = pd.read_csv(input_file_path, delimiter=',')

# Filter the DataFrame to only include rows where the year is 2024 or later
df_2024 = Original_data[Original_data['year'] >= 2024]

#iso2 codes of MEA countries
iso2_codes = [
    'DZ', 'AO', 'BH', 'BJ', 'BW', 'BF', 'BI', 'CV', 'CM', 'CF', 'TD', 'KM', 'CG', 'CI', 'CD',
    'EG', 'GQ', 'ER', 'SZ', 'ET', 'GA', 'GM', 'GH', 'GN', 'GW', 'IL', 'JO', 'KE', 'KW', 'LB', 'LS',
    'LR', 'LY', 'MG', 'MW', 'ML', 'MR', 'MU', 'YT', 'MA', 'MZ', 'NA', 'NE', 'NG', 'RE', 'RW', 'ST',
    'OM', 'QA', 'SA', 'SN', 'SC', 'SL', 'SO', 'ZA', 'SS', 'SH', 'SD', 'TZ', 'TG', 'TN', 'TR', 'UG',
    'AE', 'YE', 'ZM', 'ZW'
]

filtered_df = df_2024[df_2024['iso2_code'].isin(iso2_codes)]

# Filter the DataFrame to only include programming languages
programming_df = filtered_df[filtered_df['language_type'] == "programming"]
programming_df = programming_df.reset_index(drop=True)

# Sort by 'iso2_code' and 'num_pushers' (descending order)
df = programming_df.sort_values(by=['iso2_code', 'num_pushers'], ascending=[True, False])

# Group by 'iso2_code' and assign rank based on 'num_pushers'
df['rank'] = df.groupby('iso2_code')['num_pushers'].rank(method='first', ascending=False).astype(int)

#custom sorting order
iso2_codes = [
    'DZ', 'AO', 'BH', 'BJ', 'BW', 'BF', 'BI', 'CV', 'CM', 'CF', 'TD', 'KM', 'CG', 'CI', 'CD',
    'EG', 'GQ', 'ER', 'SZ', 'ET', 'GA', 'GM', 'GH', 'GN', 'GW', 'IL', 'JO', 'KE', 'KW', 'LB', 'LS',
    'LR', 'LY', 'MG', 'MW', 'ML', 'MR', 'MU', 'YT', 'MA', 'MZ', 'NA', 'NE', 'NG', 'RE', 'RW', 'ST',
    'OM', 'QA', 'SA', 'SN', 'SC', 'SL', 'SO', 'ZA', 'SS', 'SH', 'SD', 'TZ', 'TG', 'TN', 'TR', 'UG',
    'AE', 'YE', 'ZM', 'ZW'
]

# Convert the 'iso2_code' column to a categorical type with the specified order
df['iso2_code'] = pd.Categorical(df['iso2_code'], categories=iso2_codes, ordered=True)

# Sort the DataFrame by the custom iso2_code order
sorted_df = df.sort_values('iso2_code')
sorted_df = sorted_df.reset_index(drop=True)

# Pivot the DataFrame
pivot_df = sorted_df.pivot(index='iso2_code', columns='language', values='rank')

# Fill NaN values with 0
pivot_df = pivot_df.fillna(0).astype(int)

output_file_path = os.path.join(DATAPATH, "language_ranks.csv")
output_file_path_1 = os.path.join(DATAPATH, "language_ranks.xlsx")

#save the DataFrame as a CSV file
pivot_df.to_csv(output_file_path, index=True)  

#save the DataFrame as an Excel file
pivot_df.to_excel(output_file_path_1, index=True)  


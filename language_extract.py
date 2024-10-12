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

programming_df = filtered_df[filtered_df['language_type'] == "programming"]
programming_df = programming_df.reset_index(drop=True)


df = programming_df.sort_values(by=['iso2_code', 'num_pushers'], ascending=[True, False])

df['rank'] = df.groupby('iso2_code')['num_pushers'].rank(method='first', ascending=False).astype(int)


iso2_codes = [
    'DZ', 'AO', 'BH', 'BJ', 'BW', 'BF', 'BI', 'CV', 'CM', 'CF', 'TD', 'KM', 'CG', 'CI', 'CD',
    'EG', 'GQ', 'ER', 'SZ', 'ET', 'GA', 'GM', 'GH', 'GN', 'GW', 'IL', 'JO', 'KE', 'KW', 'LB', 'LS',
    'LR', 'LY', 'MG', 'MW', 'ML', 'MR', 'MU', 'YT', 'MA', 'MZ', 'NA', 'NE', 'NG', 'RE', 'RW', 'ST',
    'OM', 'QA', 'SA', 'SN', 'SC', 'SL', 'SO', 'ZA', 'SS', 'SH', 'SD', 'TZ', 'TG', 'TN', 'TR', 'UG',
    'AE', 'YE', 'ZM', 'ZW'
]

df['iso2_code'] = pd.Categorical(df['iso2_code'], categories=iso2_codes, ordered=True)

sorted_df = df.sort_values('iso2_code')
sorted_df = sorted_df.reset_index(drop=True)

# Pivot the DataFrame
pivot_df = sorted_df.pivot(index='iso2_code', columns='language', values='rank')

pivot_df = pivot_df.fillna(0).astype(int)

output_file_path = os.path.join(DATAPATH, "language_ranks.csv")
output_file_path_1 = os.path.join(DATAPATH, "language_ranks.xlsx")

pivot_df.to_csv(output_file_path, index=True)  

pivot_df.to_excel(output_file_path_1, index=True)  


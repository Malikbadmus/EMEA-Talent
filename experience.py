import os
import sys
import pandas as pd
import numpy as np

# search path for modules 
sys.path.append(os.path.abspath("../src"))
DATAPATH = "./data"
SRC= "../src"

#File path
input_file_path = os.path.join(DATAPATH, "survey_results_public.csv")

# Reading the CSV file into a pandas DataFrame
Original_data = pd.read_csv(input_file_path, delimiter=',')

countries = [
    'Algeria', 'Angola', 'Bahrain', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Carbo Verde', 
    'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Congo', "Côte d'Ivoire", 
    'Democratic Republic of the Congo', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 
    'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Israel', 'Jordan', 'Kenya', 
    'Kuwait', 'Lebanon', 'Lesotho', 'Liberia', 'Libyan Arab Jamahiriya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 
    'Mauritius', 'Mayotte', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Reunion', 
    'Rwanda', 'Sao Tome & Principle', 'Oman', 'Palestine', 'Qatar', 'Saudi Arabia', 'Senegal', 'Seychelles', 
    'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'St Helena', 'Sudan', 'United Republic of Tanzania', 
    'Togo', 'Tunisia', 'Turkey', 'Uganda', 'United Arab Emirates', 'Yemen', 'Zambia', 
    'Zimbabwe'
]

filtered_df = Original_data[Original_data['Country'].isin(countries)]


def convert_to_numeric_or_category(value):
    if value == "Less than 1 year":
        return 0  
    elif value == "More than 50 years":
        return 51  
    else:
       
        return pd.to_numeric(value, errors='coerce')

filtered_df['YearsCodePro'] = filtered_df['YearsCodePro'].apply(convert_to_numeric_or_category)
filtered_df = filtered_df.dropna(subset=['YearsCodePro'])

def categorize_experience(years):
    if years < 1:
        return "Less than 1 year"
    elif 1 <= years <= 2:
        return "1-2 years"
    elif 3 <= years <= 5:
        return "3-5 years"
    elif 6 <= years <= 9:
        return "6-9 years"
    elif 10 <= years <= 14:
        return "10-14 years"
    elif 15 <= years <= 19:
        return "15-19 years"
    elif 20 <= years <= 50:
        return "20 or more years"
    else:
        return "More than 50 years"

filtered_df['experience_range'] = filtered_df['YearsCodePro'].apply(categorize_experience)


experience_ranges = [
    'Less than 1 year',
    '1-2 years',
    '3-5 years',
    '20 or more years',
    '6-9 years',
    '10-14 years',
    '15-19 years',
    'More than 50 years'
]


df = filtered_df[filtered_df['experience_range'].isin(experience_ranges)]
experience_count = df.groupby(['Country', 'experience_range']).size().unstack(fill_value=0)
experience_total = experience_count.sum(axis=1)

experience_percentage_df = (experience_count.T / experience_total).T * 100
pivot_table = experience_percentage_df.reindex(columns=experience_ranges).fillna(0)
pivot_table = pivot_table.reset_index()

output_file_path = os.path.join(DATAPATH, "experience.csv")
output_file_path_1 = os.path.join(DATAPATH, "experience.xlsx")

pivot_table.to_csv(output_file_path, index=True)  
pivot_table.to_excel(output_file_path_1, index=True)  

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


# Specific education values 
education_levels = [
    'Primary/elementary school',
    'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)',
    'Some college/university study without earning a degree',
    'Associate degree (A.A., A.S., etc.)',
    'Bachelor’s degree (B.A., B.S., B.Eng., etc.)',
    'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)',
    'Professional degree (JD, MD, Ph.D, Ed.D, etc.)',
    'Something else'
]


df = filtered_df[filtered_df['EdLevel'].isin(education_levels)]
country_education_counts = df.groupby(['Country', 'EdLevel']).size().unstack(fill_value=0)
country_totals = country_education_counts.sum(axis=1)
education_percentage_df = (country_education_counts.T / country_totals).T * 100
pivot_table = education_percentage_df.reindex(columns=education_levels).fillna(0)
pivot_table = pivot_table.reset_index()


output_file_path = os.path.join(DATAPATH, "education.csv")
output_file_path_1 = os.path.join(DATAPATH, "education.xlsx")


pivot_table.to_csv(output_file_path, index=True)  
pivot_table.to_excel(output_file_path_1, index=True)  
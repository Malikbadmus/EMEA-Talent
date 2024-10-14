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

roles = [
    'Academic researcher',
    'Blockchain',
    'Cloud infrastructure engineer',
    'Data or business analyst',
    'Data engineer',
    'Data scientist or machine learning specialist',
    'Database administrator',
    'Designer',
    'Developer Advocate',
    'Developer, AI',
    'Developer, back-end',
    'Developer, desktop or enterprise applications',
    'Developer, embedded applications or devices',
    'Developer Experience',
    'Developer, front-end',
    'Developer, full-stack',
    'Developer, game or graphics',
    'Developer, mobile',
    'Developer, QA or test',
    'DevOps specialist',
    'Educator',
    'Engineer, site reliability',
    'Engineering manager',
    'Hardware Engineer',
    'Marketing or sales professional',
    'Product manager',
    'Project manager',
    'Research & Development role',
    'Scientist',
    'Senior Executive (C-Suite, VP, etc.)',
    'Student',
    'System administrator',
    'Security professional'
]

age_ranges = [
    "Under 18 years old",
    "18-24 years old",
    "25-34 years old",
    "35-44 years old",
    "45-54 years old",
    "55-64 years old",
    "65 years or older",
    "Prefer not to say"
]



filtered_df = Original_data[Original_data['Country'].isin(countries)]

df = filtered_df[filtered_df['DevType'].isin(roles)]
roles_count = df.groupby(['Country', 'DevType']).size().unstack(fill_value=0)
roles_total = roles_count.sum(axis=1)

roles_percentage_df = (roles_count.T / roles_total).T * 100
pivot_table = roles_percentage_df.reindex(columns=roles).fillna(0)
pivot_table = pivot_table.reset_index()

output_file_path = os.path.join(DATAPATH, "roles.csv")
output_file_path_1 = os.path.join(DATAPATH, "roles.xlsx")


pivot_table.to_csv(output_file_path, index=True)  
pivot_table.to_excel(output_file_path_1, index=True)  



#Get data for age_range
df = filtered_df[filtered_df['Age'].isin(age_ranges)]
age_count = df.groupby(['Country', 'Age']).size().unstack(fill_value=0)
age_total = age_count.sum(axis=1)
age_percentage_df = (age_count.T / age_total).T * 100
pivot_table = age_percentage_df.reindex(columns=age_ranges).fillna(0)
pivot_table = pivot_table.reset_index()


output_file_path = os.path.join(DATAPATH, "age.csv")
output_file_path_1 = os.path.join(DATAPATH, "age.xlsx")
pivot_table.to_csv(output_file_path, index=True)  
pivot_table.to_excel(output_file_path_1, index=True)  
import requests
from bs4 import BeautifulSoup
import pandas as pd

ONET_URL = "https://www.onetonline.org/find/family?f=15"

def fetch_onet_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to retrieve page with status code {response.status_code}")
        return None

def extract_job_roles(soup):
    job_roles = {}

    job_links = soup.find_all('a', href=True)
    
    for link in job_links:
        if '/link/summary/' in link['href']:
            job_title = link.text.strip()
            
            if link['href'].startswith('http'):
                job_link = link['href']
            else:
                job_link = "https://www.onetonline.org" + link['href']
            
            job_roles[job_title] = job_link
    
    return job_roles

def extract_skills_and_technologies(job_url):
    job_soup = fetch_onet_data(job_url)
    if job_soup is None:
        return None, None

    skills = []
    hot_technologies = []

    
    in_demand_skills_link = job_soup.find('a', text="In Demand skills for this job")
    if in_demand_skills_link:
        skills_url = "https://www.onetonline.org" + in_demand_skills_link['href']
        skills_soup = fetch_onet_data(skills_url)
        if skills_soup:
            
            skill_items = skills_soup.find_all('li')
            skills = [skill.text.strip() for skill in skill_items]

    
    hot_tech_link = job_soup.find('a', text="Hot Technologies for this job")
    if hot_tech_link:
        hot_tech_url = "https://www.onetonline.org" + hot_tech_link['href']
        hot_tech_soup = fetch_onet_data(hot_tech_url)
        if hot_tech_soup:
           
            hot_tech_items = hot_tech_soup.find_all('li')
            hot_technologies = [tech.text.strip() for tech in hot_tech_items]
    
    return skills, hot_technologies


def aggregate_data(job_roles):
    job_data = []
    for job_title, job_url in job_roles.items():
        print(f"Processing {job_title}...")
        skills, hot_technologies = extract_skills_and_technologies(job_url)
        job_data.append({
            'Job Title': job_title,
            'In-Demand Skills': skills if skills else 'No data',
            'Hot Technologies': hot_technologies if hot_technologies else 'No data'
        })
    return job_data


def main():
    
    soup = fetch_onet_data(ONET_URL)
    if soup is None:
        return None
    
   
    job_roles = extract_job_roles(soup)
    if not job_roles:
        print("No job roles were extracted.")
        return None
    
    
    job_data = aggregate_data(job_roles)
    
   
    df = pd.DataFrame(job_data)
    
    df.to_csv('tech_roles_onet_data.csv', index=False)
    df.to_excel('tech_roles_onet_data.xlsx', index=True) 
    return df  

if __name__ == "__main__":
    df = main()
    if df is not None:
        print(df.head(50)) 

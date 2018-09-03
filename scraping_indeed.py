#!/usr/bin/python
import requests
import pandas as pd
import time
import bs4
from bs4 import BeautifulSoup



max_results_per_city = 100
city_set = ['Genève', 'Nyon', 'Gland', 'Rolle', 'Lausanne', 'Versoix', 'Acacias', 'Carouge']
columns = ["from_site", "city", "job_link", "job_title", "company_name", "location", "summary", "salary"]
BASE_URL_indeed = 'http://www.indeed.ch'

sample_df = pd.DataFrame(columns = columns)

# scraping code:
for city in city_set:
  for start in range(0, max_results_per_city, 10):
    page = requests.get('http://www.indeed.ch/jobs?q=frontend+developer&l=' + str(city) + '&start=' + str(start))
  time.sleep(1)  # ensuring at least 1 second between page grabs
  soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
  for div in soup.find_all(name="div", attrs={"class":"row"}): 
    # specifying row num for index of job posting in dataframe
    num = (len(sample_df) + 1) 
    # creating an empty list to hold the data for each posting
    job_post = [] 
    from_site = "indeed"
    # append from site
    job_post.append(from_site) 
    # append city name
    job_post.append(city) 
    # job link related to job id
    id = div.get('data-jk', None)
    # grabbing job link
    link = BASE_URL_indeed + '/rc/clk?jk=' + id
    job_post.append(link)
    # grabbing job title
    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
      job_post.append(a["title"])   
    # grabbing company name
    company = div.find_all(name="span", attrs={"class":"company"}) 
    if len(company) > 0: 
      for b in company:
        job_post.append(b.text.strip()) 
    else: 
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
        job_post.append(span.text) 
    # grabbing location name
    c = div.findAll('span', attrs={'class': 'location'}) 
    for span in c: 
      job_post.append(span.text) 
    # grabbing summary text
    d = div.findAll('span', attrs={'class': 'summary'}) 
    for span in d:
        job_post.append(span.text.strip()) 
    # grabbing salary
    try:
      job_post.append(div.find('nobr').text) 
    except:
      try:
        div_two = div.find(name="div", attrs={"class":"sjcl"}) 
        div_three = div_two.find("div") 
        job_post.append(div_three.text.strip())
      except:
        job_post.append("Nothing_found") 
        # appending list of job post info to dataframe at index num
        sample_df.loc[num] = job_post


# saving sample_df as a local csv file — define your own local path to save contents 
sample_df.to_csv("output/indeed.csv", encoding='utf-8')
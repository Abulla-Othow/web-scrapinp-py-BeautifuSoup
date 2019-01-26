from bs4 import BeautifulSoup
import requests
import  pandas as pd
# ================================================
# ========Crawling and scrapping next pages=======
# ================================================

# You need to extract all the detail of job at once.
# You can see that each job has higher level paragraph tag
# whose class name is call 'result-info'
# It is called Wrapper.


# ======URL Extraction=====
# we need 5 variables

# 1. variable for link

url = "https://boston.craigslist.org/search/sof"

# 2. variable that get the website or respond object

response = requests.get(url)
#print(response)     ----200 if that loaded correctly

# 3. Variable to extract the source code of the web page

data = response.text
# print((data))

# 4 variable to make a soup of the web page

soup = BeautifulSoup(data, 'html.parser')

# Get the job variable at once

jobs = soup.find_all('p', {'class': 'result-info'})


npo_jobs = {} # create an empty dictionary
job_no= 0 # count the number of jobs
while True:
  response = requests.get(url)
  data = response.text
  soup = BeautifulSoup(data, 'html.parser')
  jobs = soup.find_all('p', {'class': 'result-info'})

  for job in jobs:
        title = job.find('a', {'class': 'result-title'}).text
        location_tag = job.find('span', {'class': 'result-hood'})
        location = location_tag.text[2:-1] if location_tag else 'N/A'
        date = job.find('time', {'class': 'result-date'}).text
        link = job.find('a', {'class': 'result-title'}).get('href')
        # means to get job description
        job_response = requests.get(link) # get the response from these links
        job_data =job_response.text # get the text from these response
        job_soup = BeautifulSoup(job_data, 'html.parser') # make a soup from job_data and parse it into html
        job_description = job_soup.find('section', 'html.parser') # get the job_description from the soup and parse it into html
        job_attributes_tag = job_soup.find('p', {'class': 'attrgroup'}) # which Job nature-fulltime, contract, salary---
        job_attributes = job_attributes_tag.text if job_attributes_tag else "N/A" # the cleaned code for job_attributes

        job_no+=1
        npo_jobs[job_no] = [title, location, date, link, job_attributes, job_description]
        # print the result


        print('Job Title:', title, '\nLocation:', location, '\nDate:', date, '\nLink:', link, "\nJob Attributes", job_attributes, "\nJob Description:", job_description,  '\n ------')
    #     next page
        url_tag = soup.find('a', {'title': 'next page'})
        if url_tag.get('href'):
            url = 'https://boston.craigslist.org' + url_tag.get('href')
            print(url)
        else:
            break
        print("Total Job:", job_no)

        npo_jobs_df = pd.DataFrame.from_dict(npo_jobs, orient='index', columns=['Job Title','Location', 'Date', 'Link', 'Job Attributes', 'Job Description'])

        npo_jobs_df.head()

        npo_jobs_df.to_csv('npo_jobs.csv')



















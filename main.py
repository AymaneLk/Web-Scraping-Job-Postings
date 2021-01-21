# 1st step install and import modules
    #-- pip/pip3 install lxml
    #-- pip/pip3 install requests
    #-- pip/pip3 install beautifulsoup4
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

# Creating lists to save data
job_title = []
company_name = []
location = []
skills = []
links = []
salary = []
requirement = []
date = []

# Creating a variable to change page's number
page_num = 0

# get inner page infos such as (salary/ requirements)
def get_inner_page_info():
    for link in links:
        result = requests.get(link)
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        salaries = soup.find('div', {'class': 'matching-requirement-icon-container',
                                     'data-toggle': 'tooltip', 'data-placement': 'top'})
        salary.append(salaries.text.strip())
        requirements = soup.find('span', {'itemprop': 'responsibilities'}).ul
        respon_text = ''
        for li in requirements.find_all('li'):
            respon_text += li.text + '| '
        respon_text = respon_text[:-2]
        requirement.append(respon_text)

# create csv file and fill it with values
def create_csv():
    file_list = [job_title, company_name, date, location, skills, links, salary, requirement]

    exported = zip_longest(*file_list)
    with open('jobs_scrapping.csv', mode='w', encoding='utf-8') as file_object:
        wr = csv.writer(file_object)
        wr.writerow(['Job title', 'Company name', 'Date', 'Location', 'Skills',
                     'Links', 'Salary', 'Requirements'])
        wr.writerows(exported)
    print("==> DONE!")


while True:
    # 2nd step use requests to fetch the url
    try:
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")

        # 3rd step save page content/markup
        src = result.content
        #print(src) ===> to print the HTML code of the page

        # 4th step create soup object to parse content
        soup = BeautifulSoup(src, "lxml")
        #print(soup)

        page_limit = int(soup.find('strong').text)

        if page_num > (page_limit // 15):
            print('DONE: Pages ended, terminate...')
            break

        # 5th step find the elements containing infos we need
        #-- job titles, job skills, company names, location names
        job_titles = soup.find_all('h2', {'class': 'css-m604qf'})
        company_names = soup.find_all('a', {'class': 'css-17s97q8'})
        locations = soup.find_all('span', {'class': 'css-5wys0k'})
        job_skills = soup.find_all('div', {'class': 'css-y4udm8'})
        posted_new = soup.find_all('div', {'class': 'css-4c4ojb'})
        posted_old = soup.find_all('div', {'class': 'css-do6t5g'})
        posted = [*posted_new, *posted_old]

        # 6th step loop over returned lists to extract needed info into othe lists
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].a.attrs['href'])
            company_name.append(company_names[i].text)
            location.append(locations[i].text)
            skills.append(job_skills[i].text)
            date.append(posted[i].text)

        page_num += 1
        print('SUCCESS: Page switched...')
    except:
        print("FAILEID: Error occured...")
        break

# Calling the 2 functions
get_inner_page_info()
create_csv()

# The meaning of unpacking:
# x = [1, 2, 3]
# y = ['a', 'b', 'c']
# z = [x, y]
# *z = [1, 2, 3, 'a', 'b', 'c']
# zip_longest(*z) = [[1, a], [2, b], [3, c]]

from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import time


def extract_job_title_from_result(soup):
    jobs = []
    for div in soup.find_all(name= "div", attrs={"class":"row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return(jobs)


def extract_company_from_result(soup):
    companies = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
            for span in sec_try:
                companies.append(span.text.strip())
    return(companies)

 
def extract_location_from_result(soup):
    locations = []
    spans = soup.findAll("span", attrs={"class": "location"})
    for span in spans:
        locations.append(span.text)
    return(locations)


def extract_salary_from_result(soup):
    salaries = []
    for div in soup.find_all(name = "div", attrs = {"class":"row"}):
        salaryDiv = div.find("div", attrs={"class":"salarySnippet"})
        try:
            salaries.append(salaryDiv.find("span", attrs={"class":"salary no-wrap"}).text.replace('\n','').strip())
        except:
            try:
                div_two = salaryDiv.find(name="span", attrs={"class":"salary-est-similar no-wrap"})
                salaries.append(div_two.text.replace('\n','').strip())
            except:
                salaries.append("Nothing found")
    return(salaries)


def extract_summary_from_result(soup):
    summaries = []
    for div in soup.find_all(name = "div", attrs = {"class":"row"}):
        try:
            summaries.append(div.find("div", attrs={"class":"summary"}).text.replace('\n','').strip())
        except:
            summaries.append("Nothing found")
    return(summaries)


def prepareSalary(salary):
    if len(str(salary)) <= 3:
        strSalary = "%240%2C" + "0"*(3 - len(str(salary))) + str(salary)
    else:
        strSalary = "%24" + str(salary)[:-3] + "%2C" + str(salary)[-3:]
    return strSalary


city_set = ['New+York','Chicago','San+Francisco', 'Austin', 'Seattle',
            'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh',
            'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC', 'Boulder']

columns = ["city", "job_title", "company_name", "location", "summary", "salary"]


def scrappingFunction(job, salary, cities, columnsNames, maxResults):
    url = 'http://www.indeed.com/jobs?q=' + job.replace(' ', '+') + '+' + prepareSalary(salary) + '&l='
    sample_df = pd.DataFrame(columns = columnsNames)


    for city in cities:
        for start in range(0, maxResults, 10):
            num = (len(sample_df) + 1) 
            page = requests.get(url + str(city) + '&start=' + str(start))
            #time.sleep(1)  #ensuring at least 1 second between page grabs
            soup = BeautifulSoup(page.text, 'lxml')

            jobs = extract_job_title_from_result(soup)
            companies = extract_company_from_result(soup)
            locations = extract_location_from_result(soup)
            salaries = extract_salary_from_result(soup)
            summaries = extract_summary_from_result(soup)

            for i in range(len(jobs)):
                sample_df.loc[num + i] = [city, jobs[i], companies[i], locations[i], salaries[i], summaries[i]]
                                 
    #saving sample_df as a local csv file — define your own local path to save contents 
    sample_df.to_csv('scrappy.csv', encoding='utf-8')
     

scrappingFunction('data scientist', 20000 , city_set, columns, 100)

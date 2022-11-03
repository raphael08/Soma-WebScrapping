
import requests
from bs4 import BeautifulSoup as bs
import creds
import pandas as pd

login_url = 'https://soma.dit.ac.tz/login'
secure_url = 'https://soma.dit.ac.tz/'

session = requests.Session()
request = session.get(login_url).content

soup = bs(request,'html.parser')

csrf = soup.find('input',{'name':'csrf'}).get('value')

payload = {
           'email': creds.email,
           'password': creds.password,
           'csrf': csrf,  

           }


p = session.post(login_url,data=payload)

t = session.get(secure_url)

soup = bs(t.text, "html.parser")

image =soup.select('a.nav-link')
links = [ links.get("href") for links in image] 
result_url = [l for l in links if '/student-semester-results' in l]

result_url = (f'https://soma.dit.ac.tz{result_url[0]}')
result_page = session.get(result_url).text

result = pd.read_html(result_page)
r = pd.DataFrame(result)
r.to_csv('matokeo.csv',index=False)




import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

#Download Google Chrome Drive : https://sites.google.com/a/chromium.org/chromedriver/
browser = webdriver.Chrome('chromedriver.exe')
browser.get("https://www.linkedin.com/login/")
#config.txt contains your LinkedIn username and password in different lines
file = open("config.txt")
line = file.readlines()
username = line[0]
password = line[1]
elementID = browser.find_element_by_id('username')
elementID.send_keys(username)
elementID = browser.find_element_by_id('password')
elementID.send_keys(password)
elementID.submit()

#paste your organization/university people/alumni link
browser.get('https://www.linkedin.com/company/usfsic/people/')


rep = 6 #determine the rep enough to scroll all the page
last_height = browser.execute_script("return document.body.scrollHeight")

for i in range(rep):
  browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
  time.sleep(5)
  new_height = browser.execute_script("return document.body.scrollHeight")
  if new_height == last_height:
    break
  new_height = last_height

#gets the page source
src = browser.page_source
soup = BeautifulSoup(src, 'lxml')


pav = soup.find('div', {'class' : 'artdeco-card pv5 pl5 pr1 mt4'})
all_links = pav.find_all('a', {'class' : 'ember-view link-without-visited-state'})

profilesID = []
for link in all_links:
  profilesID.append(link.get('href'))

print(profilesID)
print(len(profilesID))


names = []
linkedInLink = []
subtitles = []
bios = []
majors = []
SICRoles = []

#for each profile accessible, the following attributes will be scrapped
for profileID in profilesID:
  fulllink = 'https://www.linkedin.com' + profileID
  linkedInLink.append(fulllink)
  browser.get(fulllink)
  time.sleep(8)
  src = browser.page_source
  soup = BeautifulSoup(src, 'lxml')
  print(soup.prettify())

  #scraping name
  try:
    name = soup.find('div', {'class': 'artdeco-entity-lockup__title ember-view'}).get_text().strip()
    names.append(name)
    print(name)
  except AttributeError:
    names.append("N/A")
    print("N/A")

  #scrapping subtitle
  try:
    subtitle = soup.find('div', {'class': 'artdeco-entity-lockup__subtitle ember-view truncate'}).get_text().strip()
    subtitles.append(subtitle)
    print(subtitle)
  except AttributeError:
    subtitles.append("N/A")
    print("N/A")

  #scraping bios
  try:
    bio = soup.find('div', {'class': 'display-flex ph5 pv3'}).get_text().strip()
    bios.append(bio)
    print(bio)
  except AttributeError:
    bios.append("N/A")
    print("N/A")

#sections
  sections = soup.find_all('section', {'class': 'artdeco-card ember-view break-words pb3 mt2'})
  major = 0
  for section in sections:
    sectionEducation = section.find('h2', {'class': 'pvs-header__title text-heading-large'})
    # scraping major
    if sectionEducation.find(string="Education"):
      subSections = section.find_all('span', {'class': 't-14 t-normal'})
      for a in subSections:
        try:
          major = a.get_text().strip()
          break
        except AttributeError:
          major = 'N/A'
          break
      break
    else:
      major = 'N/A'
  print(major)
  majors.append(major)

    #scrapping role within SIC (can be used for other specific orgs)
  for section in sections:
    if section.find(string = "Experience"):
      subSections2 = section.find_all('li', {'class': 'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})
      for i in subSections2:
        if i.find('img', {'alt': 'Student Investment Club at USF logo'}):
          try:
            SICRole = i.find('span', {'class': 't-bold mr1'}).get_text().strip()
            break
          except AttributeError:
            SICRole = i.find('span', {'class': 't-bold mr1 hoverable-link-text'}).get_text().strip()
            break
        else:
          SICRole = 'N/A'
      break
    else:
      SICRole = 'N/A'
  print(SICRole)
  SICRoles.append(SICRole)

#create dataframe of results
df = pd.DataFrame(list(zip(names, linkedInLink, subtitles, bios, majors, SICRoles)),
               columns =['Name','LinkedIn link', 'Sub-titles', 'Bio', 'Major', 'SIC Roles'])

print(df)
#export to csv file
df.to_csv('data.csv', index=False)

#done!!

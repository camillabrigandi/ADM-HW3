### QUESTION 1 ####
import os
import requests
from bs4 import BeautifulSoup

def download_html(url, dest_folder):
    #path is the local path we're working in 
    if not os.path.exists(dest_folder):  # create folder if it does not exist
        os.makedirs(dest_folder) 
    
    filename = url.replace('https://www.findamasters.com//masters-degrees/course/', '').replace('/', '_')
    file_path = os.path.join(dest_folder, filename)
    url_req = requests.get(url)

    if url_req.ok:
        soup = BeautifulSoup(url_req.text, 'html.parser')
        with open(file_path, 'w') as file: 
            file.write(soup.prettify())
        
        file.close()


### 1.3 ####
def get_attributes(doc):
    #initialize all the values as empty string
    courseName, universityName, facultyName, isItFullTime, description, startDate, fees, modality, duration, city, country, administration, url = ['']*13
    
    page_soup = BeautifulSoup(doc, 'html.parser')
    
    #Course Name
    courseNamelinks = page_soup.find_all('h1', {'class': 'course-header__course-title'})
    if courseNamelinks !=[]:
        courseName = courseNamelinks[0].contents[-1].strip('\n ')
    
    
    #University Name 
    page_universityNamelinks = page_soup.find_all('a', {'class': 'course-header__institution'})
    if page_universityNamelinks != []:
        universityName = page_universityNamelinks[0].contents[0].strip('\n ')


    #Faculty Name 
    facultyName_links= page_soup.find_all('a', {'class':'course-header__department' })
    if facultyName_links != []:
        facultyName = facultyName_links[0].contents[0].strip('\n ')


    #Full Time
    isItFullTime_modality__links= page_soup.find_all('a', {'class':'concealLink' })
    if isItFullTime_modality__links != []:
        for item in isItFullTime_modality__links:
            if item['href']== "/masters-degrees/full-time/":
                isItFullTime = item.contents[0].strip('\n ')
                break
            elif item['href']== "/masters-degrees/part-time/" :
                isItFullTime = item.contents[0].strip('\n ')
                break
        

    #Short Description (description)
    descritpion_ref = page_soup.find_all('div', {'id': 'Snippet'})
    if descritpion_ref!=[]:
        description = descritpion_ref[0].text
        description = description.split('\n')
        for i in range(len(description)):
            description[i] = description[i].strip()

        description = ' '.join(description).strip()


    # Start Date (startDate)
    startDaterefs = page_soup.find_all('span', {'class':'key-info__start-date'})
    if startDaterefs != []:
        startDate=startDaterefs[0].contents[-1].strip('\n ')
    

    #Fees (to save as fees): string;
    fees_ref = page_soup.find_all('div', {'class': 'course-sections__fees'})
    if fees_ref != []:
        fees_ref_ref = fees_ref[0].find_all('div', {'class': 'course-sections__content'} )

        fees_link = fees_ref_ref[0].find_all('a')
        if fees_link != []:
            fees = fees_link[0].contents[0].strip('\n ')
        else:
            fees = fees_ref_ref[0].text
            fees = fees.split('\n')
            for i in range(len(fees)):
                fees[i] = fees[i].strip()
            fees = ' '.join(fees).strip()
            


    #modality (MSC, modality)
    if isItFullTime_modality__links != []:
        for item in isItFullTime_modality__links:
            if item['href']== "/masters-degrees/msc-degrees/":
                modality = item.contents[0].strip('\n ')
                break
 

    #Duration (to save as duration):string;
    durationref = page_soup.find_all('span', {'class':'key-info__duration'})
    if durationref != []:
        duration = durationref[0].contents[-1].strip('\n ')

    #City (to save as city): string;
    city_links= page_soup.find_all('a', {'class':'course-data__city' })
    if city_links != []:
        city  = city_links[0].contents[0].strip('\n ')


    #Country (to save as country): string;
    country_links= page_soup.find_all('a', {'class':'course-data__country' })
    if country_links !=[]:
        country = country_links[0].contents[0].strip('\n ')


    #Presence or online modality (to save as administration): string;
    online_links= page_soup.find_all('a', {'class':'course-data__online' })
    oncampus_links =  page_soup.find_all('a', {'class':'course-data__on-campus' })
    if online_links + oncampus_links != []:
        if online_links != []:
            administration = online_links[0].contents[0].strip('\n ')
        elif oncampus_links != []:
            administration = oncampus_links[0].contents[0].strip('\n ')


    #Link to the page (to save as url): string.
    url_ref = page_soup.find_all('link', {'rel': 'canonical'})
    if url_ref != []:
        url = url_ref[0]['href']

    return [courseName, universityName, facultyName, isItFullTime, description, startDate, fees, modality, duration, city, country, administration, url]
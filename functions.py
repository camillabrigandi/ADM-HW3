import os
import bs4
import requests
from bs4 import BeautifulSoup
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import heapq

import numpy as np 
### QUESTION 1 ####

## 1.1 ##
def extract_masters(this_url):
  result_url = requests.get(this_url)
  result_soup = BeautifulSoup(result_url.text)
  result_links = result_soup.find_all('a', {'class':'courseLink'})
  result_list=[]
  for item in result_links:
    result_list.append((item['href'], item.text))

  return result_list



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
    modality_ref = page_soup.find_all('span', {'class': 'key-info__qualification' })
    if modality_ref != []:
        modality_ref_ref = modality_ref[0].find_all('a')
        modality = []
        for item in modality_ref_ref: 
            modality.append(item.contents[0].strip('\n '))
                    
        modality = ' '.join(modality).strip('\n ')

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



####### 2.1.2 ########

def preprocess_query(query):
    tokenized_query = nltk.word_tokenize(query)
    stopw = nltk.corpus.stopwords.words('english')
    return [nltk.PorterStemmer().stem(word) for word in tokenized_query if (word.isalnum() and (not word in stopw))]


def get_documents_conjunctive_query(query: list, vocabulary_dict: dict, inverted_index : dict):
    #checking if all the query's words are in the vocabulary
    query_not_voc = [word for word in query if word not in vocabulary_dict]

    #there are words of the query that aren't in the voc => no documents for this query 
    if query_not_voc != []:
        return []
    
    #if all the words of the query are in the vocabulary: 
    query = set(query) #deleting repetitions in the query 
    query_idx = [vocabulary_dict[word] for word in query]

    #if there are possible documents: determine their indexes and store them as a list of sets
    probable_documents = list(map(set, [inverted_index.get(word_idx) for word_idx in query_idx]))

    #getting probable documents that contain all the words by comparing the ones that contain each word subsequently
    for i in range(1, len(probable_documents)): 
        probable_documents[i] =  probable_documents[i-1].intersection(probable_documents[i])

        #if there are no documents that contain the all the words in th query up to this point => no doc at all
        if probable_documents[i] == set():
            return []
    
    #output: list of document indeces for the doc satysfing the query
    return list(probable_documents[-1])



#### 2.2
def search_engine_tfidf(query: list, tfidf_invidx_dict: dict, vocabulary: dict, k = 10 ):
    # check if there are any words in the query that aren't in the vocabulary
    i=0
    while query[i] in vocabulary and i < len(query) -1 :
        i+=1
    
    if i != len(query) - 1:
        return []

    #if all the words in the query are in the vocabulary: 
    #1. retrieving all the documents containing all the words in the query, using the function of the old search engine
    sat_query_docs = get_documents_conjunctive_query(query, vocabulary, tfidf_invidx_dict) # non funziona

    #2. check if there are any documents at all that satisfy the query
    if sat_query_docs == []:
        return []

    # if such documents exist:
    query_word_idx = [vocabulary[word] for word in query]

    #docs representation using tfidf, as list of lists 
    docs_tfidf = np.array([[tfidf_invidx_dict[word_idx].get(doc) for word_idx in query_word_idx] for doc in sat_query_docs])
    np.reshape(docs_tfidf, (len(sat_query_docs), len(query)))

    #tfidf of the query va sistemato questo
    tfidf = TfidfVectorizer()  
    query_tfidf = np.array(tfidf.fit_transform([' '.join(query)]).todense())

    cossim_vec = cosine_similarity(docs_tfidf, query_tfidf)
    #heap_topk = heapq.nlargest(k, list(zip(sat_query_docs, cossim_vec)), key=lambda el: el[1])

    return heapq.nlargest(k, list(zip(sat_query_docs, cossim_vec)), key=lambda el: el[1])
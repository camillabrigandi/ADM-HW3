import os
import requests
from bs4 import BeautifulSoup
from functions import get_attributes

for page_number in range(1, 401):
    folder_name = 'page_'+str(page_number)
    folder = os.listdir(folder_name)
    
    i = 1
    for file in folder:
        doc = open(os.path.join(folder_name, file), 'r')
        doc_attributes = get_attributes(doc)
        doc.close()

        course_number = i + 15*(page_number-1)
        tsv_name = 'course_' + str(course_number) + '.tsv'
        line = '\t '.join(doc_attributes)
        with open(os.path.join('courses_tsv', tsv_name), 'w') as tsv_file:
            tsv_file.write(line)
        tsv_file.close()
        
        i+=1
        

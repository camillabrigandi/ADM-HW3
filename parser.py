import os
import requests
from bs4 import BeautifulSoup
from functions import get_attributes

for page_number in range(1, 401):
    #define folder name
    folder_name = 'page_'+str(page_number)
    #list of all the files inside the folder
    folder = os.listdir(folder_name)
    
    i = 1 #number of the course inside the folder (from 1 to 15)
    for file in folder:
        #access file to read it
        doc = open(os.path.join(folder_name, file), 'r')
        doc_attributes = get_attributes(doc)
        doc.close()

        #course number among all courses 
        course_number = i + 15*(page_number-1)
        # create and write course_"course_number".tsv file:
        tsv_name = 'course_' + str(course_number) + '.tsv'  # define file's name
        line = '\t '.join(doc_attributes)                   # line of the file as a string
        
        #write tsv file & saving all the files in the folder "courses_tsv" to have it all together (os.path.join)
        with open(os.path.join('courses_tsv', tsv_name), 'w') as tsv_file: 
            tsv_file.write(line)
        tsv_file.close()
        
        i+=1 #update number of the course inside the folder 
        

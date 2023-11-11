### SAVING HTML & ORGANIZING THEM IN FOLDERS ###
import itertools
from functions import download_html

prova = int(input())
with open('msc_links.txt', 'r') as file:
    for i in range(1, prova):
        folder_i = 'page_' + str(i)
        
        #selecting the lines corresponding to the i-th page
        needed_lines = itertools.islice(file, 0, 15)

        #saving the corresponding html in "page_i" folder
        for url in needed_lines:
            download_html(str(url), folder_i)
        


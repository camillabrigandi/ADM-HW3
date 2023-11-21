### SAVING HTML & ORGANIZING THEM IN FOLDERS ###

from functions import download_html
import time

# saving each link in the .txt file as an element of alist
file = open('msc_links.txt', 'r')
lines_list = file.readlines()
file.close()


for i in range(1, 401):
    # maning the folder corresponding to the i-th page of the website
    folder_i = 'page_' + str(i)
        
    #selecting the lines corresponding to the i-th page
    start = (i-1)*15
    stop =  i*15
    needed_lines = lines_list[start : stop]

    #saving the corresponding htmls in "page_i" folder
    for line in needed_lines:
        url  = 'https://www.findamasters.com/' + str(line)[:-1]
        download_html(str(url), folder_i)
        time.sleep(2) #delay next request to download correctly the html
    

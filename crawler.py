from functions import extract_masters
from functions import download_html
import time


# GETTING MASTERS' DEGREE LINKS AND SAVING THEM IN A .TXT FILE 
# saving urls in a list
links = []
for page in range(1, 401):
    url = 'https://www.findamasters.com/masters-degrees/msc-degrees/?PG='+str(page)
    links += extract_masters(url)


if len(links) == 6000:  #make sure we retrieved all the links 

    # write the file with all the links
    file = open('msc_links.txt','w')
    for link in links:
        file.write(link[0]+'\n')

    file.close()

    ### SAVING HTML & ORGANIZING THEM IN FOLDERS ##

    '''# saving each link in the .txt file as an element of a list
    file = open('msc_links.txt', 'r')
    lines_list = file.readlines()
    file.close()'''


    for i in range(1, 401):
        # initializing the folder name for the i-th page of the website
        folder_i = 'page_' + str(i)
            
        #selecting the lines corresponding to the i-th page
        start = (i-1)*15
        stop =  i*15
        needed_lines = links[start : stop]

        #saving the corresponding htmls in "page_i" folder
        for line in needed_lines:
            url  = 'https://www.findamasters.com/' + str(line)[:-1] #[:-1] to eliminate the "\n" character placed at the end of every line
            download_html(str(url), folder_i)
            time.sleep(2) #delay next request to download correctly the html
    
else: 
    print('Some links are missing')
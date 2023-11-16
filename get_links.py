# GETTING MASTERS' DEGRRES LINKS

'''# se to true to install bs4 & selenium
if False: 
    pip install bs4;
    pip install selenium'''

from functions import extract_masters

links = []
for page in range(1, 401):
    url = 'https://www.findamasters.com/masters-degrees/msc-degrees/?PG='+str(page)
    links += extract_masters(url)


#writing the msc_links.txt file 
if len(links) == 6000: 
    file = open('msc_links.txt','w')
    for link in links:
        file.write(link[0]+'\n')

    file.close()
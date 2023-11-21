# GETTING MASTERS' DEGREE LINKS AND SAVING THEM IN A .TXT FILE 
# import function needed
from functions import extract_masters

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
else: 
    print('Some links are missing')
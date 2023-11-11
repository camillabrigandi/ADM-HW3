### QUESTION 1 ####
import os


def download_html(url: str, dest_folder):
    #path is the local path we're working in 
    if not os.path.exists(dest_folder):  # create folder if it does not exist
        os.makedirs(dest_folder) 
    
    filename = str(url).replace('/masters-degrees/course/', '').replace('/', '_')
    file_path = os.path.join(dest_folder, filename)
    url_req = requests.get(url)

    soup = BeautifulSoup(url_req.text, 'html.parser')
    with open(file_path, 'w') as file: 
        file.write(soup.prettify())
    
    file.close()
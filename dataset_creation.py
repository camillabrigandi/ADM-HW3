# CREATION OF A .CSV FILE CONTAINING PANDAS DATAFRAME WITH MASTER DEGREES 
import pandas as pd
import csv
import os

columns_names = ['courseName', 'universityName', 'facultyName', 'isItFullTime', 'description', 'startDate', 'fees', 'modality', 'duration', 'city', 'country', 'administration', 'url']
msc_degrees = pd.DataFrame(columns= columns_names )
for i in range(1, 6001): 
    course_file = csv.reader(open(os.path.join('courses_tsv', 'course_'+str(i))+'.tsv', 'r'), delimiter='\t')
    line = pd.DataFrame(course_file, columns= columns_names, index = [i])
    msc_degrees = pd.concat([msc_degrees, line])

msc_degrees.to_csv('msc_degrees.csv', index=False)
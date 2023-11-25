#! /bin/bash
#####################
#merge the tsv files#
#####################
sed -i '1i\courseName universityName facultyName     isItFullTime    description     startDate       fees    modality        duration        city    country administration url' course_1.tsv
#add the column names manually to just the 1st tsv file (course_1.tsv), since we need them only once
#sed stands for "stream editor", it's a powerful tool used for text manipulation.
#-i tells sed to edit files in-place, and 1i tells sed to insert the following text at the first line of the file (the column names).
cat course_*.tsv > merged_courses.tsv   
#The > operator is used to redirect the output of the cat command to merged_courses.tsv.
################################################################
#1) Which country offers the most Master's Degrees? Which city?#
################################################################
#From the explored dataset we can see that the country is the 11th column, and the city is the 10th column. So we can write:
max_msc=$(awk -F'\t' '{print $10, $11}' merged_courses.tsv | sort | uniq -c | sort -nr | head -n 1) 
echo "Country and city that offer the most Master's Degrees : $max_msc"
#"awk -F'\t' '{print $10, $11}' merged_courses.tsv" uses awk to print the 10th and 11th fields (columns) of each line in the merged_courses.tsv file. The -F'\t' option tells awk to use a tab as the field separator.
#sort sorts the output of the awk command.
#uniq -c counts the number of occurrences of each line. The -c option tells uniq to prefix lines by the number of occurrences.
#sort -nr sorts the output of uniq -c in reverse numerical order. The -n option tells sort to compare according to string numerical value, and the -r option tells it to sort in reverse order.
#head -n 1 prints the first line of the output, which is the line with the most occurrences.
#max_msc=$(...) assigns the output of the entire command to the variable max_msc.
#################################################
#2) How many colleges offer Part-Time education?#
#################################################
#Counting the college that offer part-time (the 4th column in our merged file contains the Full time/Part time information)
course=$(awk -F '\t' '$4 ~ /Part time/ {print $2}' merged_courses.tsv | sort -u | wc -l)
echo "Number of college that offer Part-Time education: $course"
#awk -F '\t' '$4 ~ /Part time/ {print $2}' merged_courses.tsv it checks each line to see if the fourth field contains the string "Part time". If it does, it prints the second field.
#sort -u: This part sorts the output and removes duplicate lines in one step. The -u option stands for "unique", which means it only prints the first occurrence of each line.
#wc -l: It counts the number of lines in the output.
#then with "echo" I print the number of college that offer Part-Time education.
##########################################################################################################
#3)Print the percentage of courses in Engineering (the word "Engineer" is contained in the course's name)#
##########################################################################################################
total_courses=$(($(wc -l < merged_courses.tsv) - 1))
engineering_courses=$(awk -F '\t' '$1 ~ /Engineer/ {print $1}' merged_courses.tsv | wc -l)
percentage=$(awk "BEGIN {printf \"%.2f\", ($engineering_courses / $total_courses) * 100}")
echo "Percentage of Engineering courses: $percentage%"
#"total_courses=$(($(wc -l < merged_courses.tsv) - 1))" counts the total number of lines in the merged_courses.tsv file and subtracts 1. 
#The - 1 is used to exclude the header line from the count. The result is stored in the variable total_courses.
#engineering_courses=$(awk -F '\t' '$1 ~ /Engineer/ {print $1}' merged_courses.tsv | wc -l) uses awk to print the first field (column) of each line that contains the word "Engineer", and then counts the number of such lines. 
#The result is stored in the variable engineering_courses.
#percentage=$(awk "BEGIN {printf \"%.2f\", ($engineering_courses / $total_courses) * 100}") calculates the percentage of engineering courses by dividing the number of engineering courses by the total number of courses and multiplying by 100. 
#The result is formatted as a floating-point number with two decimal places and stored in the variable percentage.
#then with "echo" I print the percentage of engineering courses.
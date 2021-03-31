#Import all the needed data
import csv
from csv import reader
import datetime
import operator
from collections import deque
import itertools
from datetime import date, datetime, timedelta
from collections import Counter


#The original file has a problem. It has a blank space. I dont want to change the code generating the original file so Ill just fix it here
with open('C:/Users/Maksym/Desktop/andre/names.csv') as input, open('C:/Users/Maksym/Desktop/andre/names_clean.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    for row in csv.reader(input):
        if any(field.strip() for field in row): #This considers all rows except those that are blank
            writer.writerow(row) #Write it in the output file

#The following block of code creates anothe csv file but joins the first column (user_id) with the last (session)
with open('C:/Users/Maksym/Desktop/andre/names_clean.csv') as f:
    reader = csv.reader(f)
    with open('C:/Users/Maksym/Desktop/andre/output_fff.csv', 'w') as g:
        writer = csv.writer(g)
        for row in reader:
            new_row = [' '.join([row[0], row[2]])] + row[1:]
            writer.writerow(new_row)

#For some reason it generated blank rows again. So I fix it again in the same way as before.
with open('C:/Users/Maksym/Desktop/andre/output_fff.csv') as input, open('C:/Users/Maksym/Desktop/andre/names_clean_2.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    for row in csv.reader(input):
        if any(field.strip() for field in row):
            writer.writerow(row)



#Eu copiei este codigo do stackoverflow. O que isto faz e dar-te a primeira e a ultima vez que aparece um elemento da coluna 1, que no nosso caso é uma juncao de "user_id" e e session. Dessa maneira, da-nos o row correspondente a primeira e a ultima ocurrencia de cada sessao de cada user
#Tudo isto é copiado ao array de "result"
#https://stackoverflow.com/questions/48116067/how-to-find-out-first-and-last-occurrence-from-csv-python
with open('C:/Users/Maksym/Desktop/andre/names_clean_2.csv', newline='') as f:
    reader = csv.reader(f)
    result = []
    for k, g in itertools.groupby(reader, operator.itemgetter(0)):
        group = list(g)
        result.append(group[0])
        if len(group) > 1:
            result.append(group[-1])
    print(len(result))

#THis function defines a loop that begins on a certain date and finishes on another data. Each iteration, a certain amount of time (delta) is added to the. Basically it iterates over time for a given interval of times, adding X minutes/hours/days each iteration
def datespan(startDate, endDate, delta=timedelta(days=1)): #Delta can be specified later and will overwrite this delta
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta



#Create an empty array called #Timestamping. This will be important ahead.
timestamping=[]

#We call the function defined earlier to iterate over time, starting on 1/1/2020 at 00 hours 00 minutes, 00 seconds and each iteration we will be adding 20 minutes more. Each of these "timestamp" will be processed in the nested loop
for timestamp in datespan(datetime(2020, 1, 1, 0, 0, 0), datetime(2020, 2, 1, 0, 0, 0), delta=timedelta(minutes=20)):

    #This is the nested loop. Remember the "result" array that stores the first and the last activity of EACH session of EACH user. This loop will read the "result" array iteratively twice. The first time starting from the first row and second time starting from the second row. (So the second iteration for example will read the second row and the third)
    for line,line2 in zip(result[:-1], result[1:-1]): #Why the "-1"? Because I want the loop to read the "result" line by line EXCEPT the last line, because the last line is the header. It is an artifact of the previous code and happened after sorting. The header went to the bottom 
        
        #Compare the previous line with the current one. line[0] == line2[0] will only be true if both "user_id" and "session" coincide.
        if line[0] == line2[0]:
            #If this is true, the following two lines of code will extract the timestamp in datetime format of the current and the previous line, which will correspond to the first and the last activity for one of the sessions of one of the individuals (not to be confused with the variable called just "timestamp")
            last_timestamp_formatted = datetime.strptime(line2[1], '%Y-%m-%d %H:%M:%S.%f')
            first_timestamp_formatted =  datetime.strptime(line[1], '%Y-%m-%d %H:%M:%S.%f')

            #Now, besides having the variable "timestamp", we also need another one defined as 20 minutes after the timestamp. Because we want to define an INTERVAL of time, not just a point in time
            timestamp_limit=timestamp+timedelta(minutes=19, seconds=59)

            #This code checks if both the first and the last activity of a certain session of a certain user is WITHIN the interval of time comprised between "timestamp" and "timestamp_limit" (20 minutes) 
            if last_timestamp_formatted<timestamp_limit and first_timestamp_formatted>timestamp:
                #If this is true, we append the current timestamp to the "timestamping" array. Since we are in a loop, the more activity we have in this timestamp, the more copies of this timestamp will appear in the array
                timestamping.append(timestamp)
                print(timestamp, first_timestamp_formatted, last_timestamp_formatted, timestamp_limit)

#Basically just applying a counter command to array "timestamping", we get a count in dictionary format of how many times a certain timestamp appears in the array. Its already sorted. So the first element of this output is the solution of this problem
print(Counter(timestamping))

#The first lines of output are:
#Counter({datetime.datetime(2020, 1, 30, 15, 0): 19, datetime.datetime(2020, 1, 31, 14, 20): 15, datetime.datetime(2020, 1, 1, 12, 20): 14
#There were 19 sessions happening on 2020-1-30 between 15:00:00 and 15:19:19, the highest in any block of 20 minutes.

#This explains why I don't need to worry about sessions with only one instance in this problem. The code is made in such a way that it ignores these sessions when comparing if line[0] == line2[0]:. Notice how session_2 of user_1 has only one instance and how it will be ignored in the processing in this code
#user1, 00:01, session_1
#user1, 00:03, session_1
#user1, 00:25, session_2
#user1, 00:50, session_3
#user1, 00:55, session_3
#user2, 00:15, session_1
#user2, 00:16, session_1


#Iteration1:
#user1, 00:01, session_1 VS user1, 00:03, session_1
#user match and session too;
#OUTPUT:
#user1, 00:01, 00:03, session1


#2:
#user1, 00:03, session_1 VS user1, 00:25, session_2
#user match but session not
#OUTPUT:*skip*

#3
#user1, 00:25, session_2 VS user1, 00:50, session_3
#user match but session not
#OUTPUT:*skip*

#4
#user1, 00:50, session_3 VS user1, 00:55, session_3
#user match and session too
#OUTPUT: user1, 00:50, 00:55, session_3

#5
#user1, 00:55, session_3 VS user2, 00:15, session_1
#user not matching and session not matching:
#OUTPUT:SKIP

#6
#user2, 00:15, session_1 VSuser2, 00:16, session_1
#user matching and session too
#OUTPUT:user2, 00:15,0:16, session_1

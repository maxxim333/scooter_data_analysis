#Import all the needed data
import csv
from csv import reader
import datetime
import operator
from collections import deque
import itertools

#Open the file
reader = csv.reader(open('C:/Users/Maksym/Desktop/andre/Python_Test_Data.csv'), delimiter=";", quotechar='"')

#Sort the file by first column (user_id)
reader = sorted(reader,  key=lambda row:(row[0]), reverse=False)

#Skip the first line (header)
reader=reader[1:]

#I will process the whole file entirely with loops, but I will do it user-by-user. For that, I need to create an epty list of users that I already processed and I'll be adding users that I processed to this list.
processed=[]

#This is the first timestamp of the user (the first activity ever of that user)
first_timestamp=0

#Counter of a session. The "i" will define the current number of the session for each user. I will add +1 every iteration where the session is not the same as the previous one
i=1

#Create a new writable csv file 
f = open('names.csv', 'w')

#Begin the loop
with f:
    fnames = ['user_id', 'event_timestamp', 'session'] #The next three lines add a header to the new file I just created
    writer = csv.DictWriter(f, fieldnames=fnames)
    writer.writeheader()
    j=0 #This is just a counter of lines processed
    
    #I will create a loop in which each iteration reads the Nth and N+1nth line. For example the first iteration, the first iteration will read the first line of the input CSV file (called "previous") and the second line (called "current"). The second iteration will read the second line (previous) and the third line (current).
    for previous, current in zip(reader, reader[1:]):
        if previous and current:

            j=j+1 #add one to counter of processed lines
            x=current[0].split(",") #I want to split the rows by coma, so I can individually extract the userID and the time stamp of each row
            x2=previous[0].split(",") #Same as above but for "previous" row

            current_user=x[0] #This extracts the user_id of the "current" row
            previous_user=x2[0]#This extracts the user_id of the "previous" row

            current_timestamp=x[1] #This extracts the timestamp of the "current" row
            previous_timestamp=x2[1] #This extracts the timestamp of the "previous" row

            #The following 5 lines exist because the first row is a special case, where there is no sense comparing the previous line with the current. The previous line in the first iteration will correspond to the first row of the file (excluding header) and will be by default the session_1 of the first user that appears in the database
            if j==1:
                print (previous_user, previous_timestamp, "session_1")
                f.write(str(previous_user) + "," + str(previous_timestamp) + "," + "session_1" + " \n") #In the file, we write the user ID, the timestamp of activity and the number of session (this is the special case, where I hardcode session_1 into the file)
                processed.append(str(previous_user)) #append the user_id to the list of the processed users
                first_timestamp=previous_timestamp #This overwrites the "first_timestamp" variable which will be now the timestamp of the "previous" row

            #Now this is the general code, which applies to all the rows starting from the second
            else:
                
                #The following 6 lines check if the user_id is new (meaning not even one row of this user was processed). This effectively means that this is a new user appearing in the loop. We reset the "i" to one, because by definition, if it appears for the first time in the loop, it will be his first session. Also we reset the "first_timestamp" variable, because if this user appears for the first time, previously, the "first_timestamp" corresponded to another user
                if str(current_user) not in processed: 
                    print (current_user, current_timestamp, "session_1")
                    f.write(str(current_user) + "," + str(current_timestamp) + "," + "session_1" + " \n")
                    processed.append(str(current_user))
                    first_timestamp=current_timestamp
                    i=1

                #If the the user_id of the row being processed already appeared before at least once, this block of code runs
                else:
                    #First we we are still talking about the same user as in the row processed before. If yes, we calculate the difference between the current timestamp and the previous one. This "if" has no "else", meaning if the previously processed user is not the same as the current one, there is no point in calculating the difference of timestamps between their activity and the iteration is finished.
                    if current_user == previous_user: #compares the ID of users
                        current_timestamp_formatted = datetime.datetime.strptime(current_timestamp, '%Y-%m-%d %H:%M:%S.%f') #This is just to convert the timestamp of the current line into the "datetime" library-supported format. It's a library that works with timestamps that I chose because it's easy to calculate time differences with it.
                        previous_timestamp_formatted = datetime.datetime.strptime(previous_timestamp, '%Y-%m-%d %H:%M:%S.%f') #Same but for the "previous timestamp"
                        first_timestamp_formatted = datetime.datetime.strptime(first_timestamp, '%Y-%m-%d %H:%M:%S.%f') #Same but for the "first" timestamp of the user being processed now


                        time_diff=current_timestamp_formatted-first_timestamp_formatted #This calculates the time difference between the current and the first timestamp.

    ############################# DISCLAIMER #######################
    # When I read the exercise, the phrase "set of consecutive demands events done by one user, which are less than 20 min apart" was ambiguous. For me, it can have 2 interpretations:
    # 
    # Scenario1: Time has to be broken down into 20-minute blocks and consider every 20-minutes as a separate session. Eg:
    # user_1, 00:00:00, session_1
    # user_1, 00:15:00, session_1
    # user_1, 00:21:00, session_2 (because it doesnt fit the first block of 20-minutes)
    # user_1, 00:42:00, session_3 (because it doesnt fit the first nor second block of 20-minutes)                    
    # 
    # Scenario2: The session is only over when there is more than 20 minutes between any two consevutive activities. Eg:
    #user_1, 00:00:00, session_1
    #user_1, 00:15:00, session_1
    #user_1, 00:21:00, session_1 (because only 6 minutes passed since the last activity of the session)
    # user_1, 00:42:00, session_2 (because more than 20 minutes passed since the last activity)       
    #
    #This code, by default runs assuming scenario1, but I also made it functional for scenario2. For scenario2, the last executable line must be deleted and the following line must be made executable by removing the "#":
    #time_diff=current_timestamp_formatted-previous_timestamp_formatted


                        #The following 3 lines of code are executed if time difference is less that 20 (meaning that the current timestamp belongs to the same session of the same user as the previous one)
                        if time_diff < datetime.timedelta(minutes=20):
                            print(current_user, current_timestamp, "session_{}".format(i))
                            f.write(str(current_user) + "," + str(current_timestamp) + "," + "session_{}".format(i) + " \n") #we write the current row's user ID, timestamp and session numbered with "i", which is as explained earlier the iterator of the session number

                        #In this block of code, we do the same as in the previous block of code except we add "1" to our "i", since if the difference between time stamps is superior to 20 minutes, we are talking about another session.
                        else:
                            i=i+1
                            print(current_user, current_timestamp, "session_{}".format(i))
                            f.write(str(current_user) + "," + str(current_timestamp) + "," + "session_{}".format(i) + " \n")
                            first_timestamp=current_timestamp



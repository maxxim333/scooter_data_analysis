# scooter_data_analysis
This is an exercise I helped a friend to do for his interview. Since all this code is mine, I feel I'm entitled to post it here. 

It was for a data analyst job in a scooter-renting company. The input file they provided was a csv with logs of users and timestamps of their activities. The goal was to create "Sessions" of each users in which each session is defined by certain characteristics. Then I needed to find out the "peak of demand" for scooters defined by the time period where there is the biggest overlap of sessions. 

The images I provide are divided in two and there are two .py files. One takes as an input the csv table provided by the interviewers and generates a file with session ids and the other takes this file as input and outputs a sorted array of timestamps and their corresponding amount of overlapping sessions. The first element is the answer to the problem: the time of the year with the most demand of scooters.

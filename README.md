# McqDb_project

Project Context :
                 Live services generate logs at a very high rate; e.g., it creates over 100,000 log lines a second.
                 Usually, these logs are loaded inside databases to enable fast querying, but the cost of keeping all the logs becomes too high. 
                 For this reason, only the recent logs are kept in databases, and logs for longer periods are kept in file archives.
                 For this problem, we should assume we store our data in multiple files.
                 We close a file and start a new file when the file size reaches 16GB. Our file names are of the format LogFile-######.log (e.g., LogFile-000008.log, or LogFile-000139.log). 
                 Currently, we have over 10,000 log files with the last log file name LogFile-0018203.log and a total data size of 285TB.
                 
Problem Statement :
                 We usually use our log database to query our logs. But now and then, we may have to query older logs for customer support or debugging. In most of these cases, we know the time range for which we need to analyze the logs.
We need a tool that could extract the log lines from a given time range and print it to console in time effective manner.
The command line (CLI) for the desired program is as below
LogExtractor.exe -f "From Time" -t "To Time" -i "Log file directory location"
All the time formats will be "ISO 8601" format.
The extraction process should complete in a few seconds, minimizing the engineer's wait time.

Log file format:
               1. The log file has one log per line.
               2. Every log line will start with TimeStamp in "ISO 8601" format followed by a comma (',').
               3. All the log lines will be separated by a single newline character '\n'.
               4. Example logline: 2020-01-31T20:12:38.1234Z, Some Field, Other Field, And so on, Till new line,...\n
               
               
                                             Log Extraction Project

Problem statement :-
                                    We need a tool that could extract the log lines from a given time range and print it to console in time effective manner.
                                     
Problem Statement Solution :--
Naive Solution :-
                                        We need to check every file and in every file we check every log and If timestamp of log is between the given time range, we will print the log on console.
Optimized Solution :-
                              As we have large no. of files (around 10000) and every file-size is 16GB and total data size of 285TB. So, we can’t search every file and every log in every file. To overcome with this problem, I will use binary search to find the file starting with timestamp just smaller than or equal to given from_time. I will use first time stamp in the every file as a base to use binary search as timestamp will be in sorted order.
     Now, I will open that file and I will check the log in the file and if timestamp is between given time range I will print to console. This process will repeat if either we get time in log greater than given to-time, or we checked all log inside the file. If we get time greater than given to-time , I will stop the process. In second case I will open the next file and I will repeat the process until I get time greater than given to-time.
Function used in the code :- 
SortFiles(dir_path):-- function used to sort the file name in ascending order for eg after sorting filename will be in order 000001.log,000002.log ...
Parser(dir_path) :-- function used to find first timestamp encountered in every file and stored in a dictionary  with file_no as key and timestamp as value in the same order in which we inserted in the dictionary.
Binary_Search(timestamp_dict,from_time):-- function used to find the file with nearest timestamp less than or equal to given from_time.
GetNextKey(an,d):- function  used to get next key in dictionary given a key an in dictionary d
GetTimeStamp(x):- function used to get the first valid timestamp in the file x
PrintLog(x,from_time,to_time):- function used to print log print if timestamp of line in file is less than the given to_time
OUTPUT :-
                  Log between the given time range will be printed on console as well as I stored all log in a text file output_log , that will be generated in the location where LogExtracter.exe is located after the execution of the code.
                 



                                                                     
                                                                   
                                                                    
               

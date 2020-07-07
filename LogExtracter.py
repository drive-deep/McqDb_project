import os
import re
import sys
import datetime
import dateutil.parser
import pytz
from collections import OrderedDict
import time
from itertools import islice


timestamp_dict=OrderedDict()
d={}
'''
from_time="2020-07-07T01:01:02.9990Z"
to_time="2020-07-07T01:01:06.0184Z"
dir_path="c:\Users\Null_ptr\Desktop\project_mcqdb"'''
from_time=sys.argv[2]
to_time=sys.argv[4]
dir_path=sys.argv[6]

line_len=10


##timestamp_dict-- dictionary used to store file_no as key and first time stamp encountered as pair in the file
## d -- dictionary used to store file_no as key and file_name as value 
##sortfiles :-- function used to sort the file name in ascending order for eg after sorting filename will be in order 000001.log,000002.log ...
def SortFiles(dir_path):
    dirFiles = [x for x in os.listdir(dir_path) if x[-4:]=='.log' or x[-4:]=='.txt']
    dirFiles.sort()
    
##comparetimestamp :--- function used to compare two timestamp in iso 8601 format . it return 0 if both are same ,else return 1 if first timestamp is greater than second ,else return -1
def CompareTimeStamp(timestamp1,timestamp2):
    timestamp1= dateutil.parser.parse(timestamp1)
    timestamp2= dateutil.parser.parse(timestamp2)
    if timestamp1==timestamp2:
        return 0
    elif timestamp1>timestamp2:
        return 1
    else:
        return -1
        
##binary search -- function used to find the file with nearest timestamp less than or equal to given from_time
def Binary_Search(timestamp_dict,from_time):
    key=list(timestamp_dict.keys())
    start=key[0]
    end=key[-1]
    ans=start;
    #print(start,end)
    while(start<=end):
        mid=(start+end)//2
        if(CompareTimeStamp(timestamp_dict[mid],from_time)==1):
            end=mid-1
        else:
            ans=mid
            start=mid+1
        #print(start,end)    
                
    #print("ans=",ans)
    PrintLog(ans,from_time,to_time)
 
##getnextkey  --function  used to get next key in dictionary given a key an in dictionary d  
def GetNextKey(an,d):
    try:
        temp=list(d)
        res=temp[temp.index(an)+1]
    except(ValueError,IndexError):
        res=None    
    return res

##gettimestamp(x)--function used to get the first valid timestamp in the file x
def GetTimeStamp(x):
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{4}Z)'
    with open(os.path.join(dir_path,x),"r") as file:
        line=file.readline()
        while(not re.findall(regex,line)):
            line=file.readline()
        timestamp_check=re.findall(regex,line)
        if timestamp_check:
            timestamp=timestamp_check[0]
            global line_len
            line_len=len(line)
        
        return timestamp    

##printlog ---function used to print log print if timestamp of line in file is less than the given to_time
def PrintLog(x,from_time,to_time):
    file_name=d[x]
    flag=0
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{4}Z)'
    with open(os.path.join(dir_path,file_name),"r") as file:
        
        First_TimeStamp=GetTimeStamp(file_name)
        total_microsec=0
        from_time1=dateutil.parser.parse(from_time)
        to_time1=dateutil.parser.parse(to_time)
        First_TimeStamp1=dateutil.parser.parse(First_TimeStamp)
        #print('Firsttimestamp=',First_TimeStamp)
        if from_time1>First_TimeStamp1:
            diff=from_time1-First_TimeStamp1
            microsec=diff.microseconds
            sec=diff.seconds
            days=diff.days
            total_microsec=(days*24*60*60*100000)+(sec*100000)+microsec
            total_microsec=total_microsec//100
            
            
            file.seek(max((line_len+1)*(total_microsec-1),0))
            line=file.readline()
            
        
        
        for line in file:
            
            timestamp_check=re.findall(regex,line)
            if timestamp_check:
                
                timestamp=timestamp_check[0]
                    #print(timestamp,from_time,to_time)
                    #print(CompareTimeStamp(timestamp,from_time),CompareTimeStamp(timestamp,to_time))
                if(CompareTimeStamp(timestamp,from_time)>=0 and CompareTimeStamp(timestamp,to_time)<=0):
                    print(line.strip())
                   # output_file.write(str(line))
                elif(CompareTimeStamp(timestamp,to_time)>0) or not line:
                    flag=1
                    break
        
                 
                #print(flag)
            if flag==1:
                break
        
        
                   
        if flag==0:
     
            res=GetNextKey(x,d)
            if res:
                PrintLog(res,from_time,to_time)

            
            
        
        
##parser :--function used to find first timestamp encountered in every file and stored in a dictionary  with file_no as key and timestamp as value in the same order in which we inserted in the dictionary  
def Parser(dir_path):
    
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{4}Z)'
    for x in os.listdir(dir_path):
        if(x[-4:]=='.log' or x[-4:]=='.txt'):
            
            file_no=re.findall(r'\d+',x)
            if file_no:
                
                y=int(file_no[0])
                d[y]=x
                
                timestamp_dict[y]=GetTimeStamp(x)
            
                
                  
            
            
           
SortFiles(dir_path)    
Parser(dir_path)
Binary_Search(timestamp_dict,from_time)



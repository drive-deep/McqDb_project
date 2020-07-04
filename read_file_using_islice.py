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
from_time="2020-06-30T16:01:01.007879"
to_time="2020-06-30T16:01:01.007880"
dir_path="c:\Users\Null_ptr\Desktop\project_mcqdb"
NoOfLineInCache=2000
line_len=80

#output_file=open("c:\Users\Null_ptr\Desktop\project\output_log","w+")
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
    print(start,end)
    while(start<=end):
        mid=(start+end)//2
        if(CompareTimeStamp(timestamp_dict[mid],from_time)==1):
            end=mid-1
        else:
            ans=mid
            start=mid+1
        print(start,end)    
                
    print("ans=",ans)
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
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6})'
    with open(os.path.join(dir_path,x),"r") as file:
        line=file.readline()
        while(not re.findall(regex,line)):
            line=file.readline()
        timestamp_check=re.findall(regex,line)
        if timestamp_check:
            timestamp=timestamp_check[0]
            line_len=len(line)
        
        return timestamp    

##printlog ---function used to print log print if timestamp of line in file is less than the given to_time
def PrintLog(x,from_time,to_time):
    file_name=d[x]
    
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6})'
    with open(os.path.join(dir_path,file_name),"r") as file:
        flag=0
        First_TimeStamp=GetTimeStamp(file_name)
        total_microsec=0
        from_time1=dateutil.parser.parse(from_time)
        to_time1=dateutil.parser.parse(to_time)
        First_TimeStamp1=dateutil.parser.parse(First_TimeStamp)
        
        if from_time1>First_TimeStamp1:
            diff=from_time1-First_TimeStamp1
            microsec=diff.microseconds
            sec=diff.seconds
            days=diff.days
            total_microsec=(days*24*60*60*1000000)+(sec*1000000)+microsec-100
            total_microsec=max(total_microsec,0)
            print(line_len)
            #file.seek(line_len*total_microsec)
        
        lines_cache=islice(file,NoOfLineInCache)
        
        for line in lines_cache:
            
        
            timestamp_check=re.findall(regex,line)
            if timestamp_check:
                
                timestamp=timestamp_check[0]
                print(timestamp,from_time,to_time)
                print(CompareTimeStamp(timestamp,from_time),CompareTimeStamp(timestamp,to_time))
                if(CompareTimeStamp(timestamp,from_time)>=0 and CompareTimeStamp(timestamp,to_time)<=0):
                    print(line.strip())
                #output_file.write(str(line))
                elif(CompareTimeStamp(timestamp,to_time)>0):
                    flag=1
                    break
        
                   
            
            if flag==1:
                
                break        
        if(flag==0):
            res=GetNextKey(x,d)
            if res:
                timestamp_nextfile=GetTimeStamp(d[res])
                if(CompareTimeStamp(to_time,timestamp_nextfile)>=0 ):
                    PrintLog(res,from_time,to_time)
                
            
            
            
        
        
##parser :--function used to find first timestamp encountered in every file and stored in a dictionary  with file_no as key and timestamp as value in the same order in which we inserted in the dictionary  
def Parser(dir_path):
    #os.chdir(dir_path)
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6})'
    for x in os.listdir(dir_path):
        if(x[-4:]=='.log' or x[-4:]=='.txt'):
            
            file_no=re.findall(r'\d+',x)
            if file_no:
                
                y=int(file_no[0])
                d[y]=x
                print(y,x)
                timestamp_dict[y]=GetTimeStamp(x)
            
                
                  
            
            
           
SortFiles(dir_path)    
Parser(dir_path)
Binary_Search(timestamp_dict,from_time)


#output_file.close() 

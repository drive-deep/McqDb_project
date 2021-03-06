
import os
import re
import sys
import datetime
import dateutil.parser
import pytz
from collections import OrderedDict


timestamp_dict=OrderedDict()
d={}
from_time=sys.argv[2]
to_time=sys.argv[4]
dir_path=sys.argv[6]


##timestamp_dict-- dictionary used to store file_no as key and first time stamp encountered as pair in the file
## d -- dictionary used to store file_no as key and file_name as value 
##sortfiles :-- function used to sort the file name in ascending order for eg after sorting filename will be in order 000001.log,000002.log ...
def sortfiles(dir_path):
    dirFiles = [x for x in os.listdir(dir_path) if x[-4:]=='.log' or x[-4:]=='.txt']
    dirFiles.sort()
    
##comparetimestamp :--- function used to compare two timestamp in iso 8601 format . it return 0 if both are same ,else return 1 if first timestamp is greater than second ,else return -1
def comparetimestamp(timestamp1,timestamp2):
    timestamp1= dateutil.parser.parse(timestamp1)
    timestamp2= dateutil.parser.parse(timestamp2)
    if timestamp1==timestamp2:
        return 0
    elif timestamp1>timestamp2:
        return 1
    else:
        return -1
        
##binary search -- function used to find the file with nearest timestamp less than or equal to given from_time
def binary_search(timestamp_dict,from_time):
    key=list(timestamp_dict.keys())
    start=key[0]
    end=key[-1]
    ans=start;
    
    while(start<=end):
        mid=(start+end)//2
        if(comparetimestamp(timestamp_dict[mid],from_time)==1):
            end=mid-1
        else:
            ans=mid
            start=mid+1
                
    #print("ans=",ans)
    printlog(ans,from_time,to_time)
 
##getnextkey  --function  used to get next key in dictionary given a key an in dictionary d  
def getnextkey(an,d):
    try:
        temp=list(d)
        res=temp[temp.index(an)+1]
    except(ValueError,IndexError):
        res=None    
    return res

##gettimestamp(x)--function used to get the first valid timestamp in the file x
def gettimestamp(x):
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{4}Z)'
    with open(os.path.join(dir_path,x),"r") as file:
        line=file.readline()
        while(not re.findall(regex,line)):
            line=file.readline()
        timestamp_check=re.findall(regex,line)
        if timestamp_check:
            timestamp=timestamp_check[0]
        
        return timestamp    

##printlog ---function used to print log print if timestamp of line in file is less than the given to_time
def printlog(x,from_time,to_time):
    file_name=d[x]
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{4}Z)'
    with open(os.path.join(dir_path,file_name),"r") as file:
        line=file.readline()
        
        timestamp_check=re.findall(regex,line)
        if timestamp_check:
            timestamp=timestamp_check[0]
            if(comparetimestamp(timestamp,from_time)>=0 and comparetimestamp(timestamp,to_time)<=0):
                print(line.strip())
                
        
        tmp=0            
        while line:
            line=file.readline()
            timestamp_check=re.findall(regex,line)
            if timestamp_check:
                timestamp=(timestamp_check[0])
                #print(timestamp,from_time,to_time)
                #print(timestamp,comparetimestamp(timestamp,from_time),comparetimestamp(timestamp,to_time))
                
                if(comparetimestamp(timestamp,from_time)>=0 and comparetimestamp(timestamp,to_time)<=0):
                    print(line.strip())
                elif(comparetimestamp(timestamp,to_time)>0):
                    tmp=1
                    break    
            if tmp==1:
                break        
        if(tmp==0):
            res=getnextkey(x,d)
            if res:
                timestamp_nextfile=gettimestamp(d[res])
                if(comparetimestamp(to_time,timestamp_nextfile)>=0 ):
                    printlog(res,from_time,to_time)
                
            
            
            
        
        
##parser :--function used to find first timestamp encountered in every file and stored in a dictionary  with file_no as key and timestamp as value in the same order in which we inserted in the dictionary  
def parser(dir_path):
    #os.chdir(dir_path)
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{4}Z)'
    for x in os.listdir(dir_path):
        if(x[-4:]=='.log' or x[-4:]=='.txt'):
            
            file_no=re.findall(r'\d+',x)
            y=int(file_no[0])
            d[y]=x
            with open(os.path.join(dir_path,x),"r") as file:
                line=file.readline()
                
                while(not re.findall(regex,line)):
                    line=file.readline()
                
                timestamp_check=re.findall(regex,line)  
                if timestamp_check:
                    timestamp=re.findall(regex,line)[0]
                    timestamp_dict[y]=timestamp
                
                  
            
            
           
sortfiles(dir_path)    
parser(dir_path)
binary_search(timestamp_dict,from_time)


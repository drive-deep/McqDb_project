
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




def sortfiles(dir_path):
    dirFiles = [x for x in os.listdir(dir_path) if x[-4:]=='.log' or x[-4:]=='.txt']
    dirFiles.sort()
    

def comparetimestamp(timestamp1,timestamp2):
    timestamp1= dateutil.parser.parse(timestamp1)
    timestamp2= dateutil.parser.parse(timestamp2)
    if timestamp1==timestamp2:
        return 0
    elif timestamp1>timestamp2:
        return 1
    else:
        return -1
        
    
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
                
    
    printlog(ans,to_time)
    
def getnextkey(an,d):
    try:
        temp=list(d)
        res=temp[temp.index(an)+1]
    except(ValueError,IndexError):
        res=None    
    return res

def gettimestamp(x):
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{4}Z)'
    with open(x,"r") as file:
        line=file.readline()
        while(not re.findall(regex,line)):
            line=file.readline()
        timestamp_check=re.findall(regex,line)
        if timestamp_check:
            timestamp=timestamp_check[0]
        
        return timestamp    

def printlog(x,to_time):
    file_name=d[x]
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{4}Z)'
    with open(file_name,"r") as file:
        k=file.readline()
        timestamp_check=re.findall(regex,k)
        while(not re.findall(regex,k)):
            k=file.readline()
        if k:
            print k  
        timestamp_line=re.findall(regex,k)[0]
        while(comparetimestamp(timestamp_line,to_time)<=0):
            while(not re.findall(regex,k)):
                k=file.readline()
            timestamp_line=re.findall(regex,k)[0]
            if k:
                print k
        
        file.close()    
        res=getnextkey(x,d)
        if res:
            timestamp_nextfile=gettimestamp(d[res])
            if(comparetimestamp(to_time,timestamp_nextfile)>=0 ):
                    
                printlog(res,to_time)
                
            
            
            
        
        
    
def parser(dir_path):
    os.chdir(dir_path)
    regex=r'^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{4}Z)'
    for x in os.listdir(dir_path):
        if(x[-4:]=='.log' or x[-4:]=='.txt'):
            
            file_no=re.findall(r'\d+',x)
            y=int(file_no[0])
            d[y]=x
            with open(x,"r") as file:
                line=file.readline()
                
                while(not re.findall(regex,line)):
                    line=file.readline()
                   
                timestamp=re.findall(regex,line)[0]
                
                timestamp_dict[y]=timestamp  
            
            
           
sortfiles(dir_path)    
parser(dir_path)
binary_search(timestamp_dict,from_time)


import os
import re
import sys
import datetime
import dateutil.parser

#time=datetime.datetime.now().isoformat()
#print(time)


with open("00001.txt","w+") as file:
    for m in range(0,24):
        for k in range(0,60):
        
            for i in range(0,60):
                for j in range(0,10000):
                    s=datetime.datetime.now().replace(microsecond=j).replace(second=i).replace(minute=k).replace(hour=m).isoformat()
             
                    tmp=s[:20]+s[22:]+'Z'+", Some Field, Other Field, And so on, Till new line,...\n"
                    #print(tmp)
            
                    file.write(tmp)
    


import sys
import random
import time

def updateCurrentThreshold(list):
  sum =0
  for numbers in list:
    sum += numbers
  ave = sum/(len(list))
  print (ave)
  print (len(list))
  return (ave)
  
  
  
init_Threshold =input('Enter Your init Threshold')
Threshold = init_Threshold
Threshold = float(Threshold)
interval = input('Enter you Interval size')
interval = int(interval)
x = random.uniform(1, 100)
hit=0
hi2=0
list =[];
list2 =[];
high=0
low=0
while(True):
  x = random.uniform(1, 100)
  time.sleep(4)
  print ("New Data: ",x)
  print ("Current Threshold: " ,Threshold )
  if(x>Threshold):
    
    if(high ==1 or hit==0):
      list.append(x)
      hit+=1
    elif(high == 0 and hit >= 1):
      list =[]
      hit=1
      list.append(x)
    else:
      hit = 0
      list=[]
    high=1
    low=0
  elif(x<Threshold):
    if(low  == 1 or hit == 0):
      list.append(x)
      hit+=1
    elif(low == 0 and hit >= 1):
      list =[]
      hit=1
      list.append(x)
    else:
      hit = 0
      list=[]
    high=0
    low=1
  if(hit==interval):
    Threshold=updateCurrentThreshold(list)
    print ("new Threshold ",Threshold)
    hit=0

    
  
  








  
  
  
  
  
  
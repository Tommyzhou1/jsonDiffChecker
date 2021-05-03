import json
import shutil
import math
import jsondiff as jd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import csv

src = 'C:/DSCIoT/IQControl/IQControl/assets/translations/en.json'
dest = 'C:/Users/jzhouga/Desktop/jsonComparator'

try:
    shutil.copy(src, dest)
    print("successfully update the file")
except IOError:
    print ("Unable to copy file. %s")

with open('tl.json') as f1:
  originalData = json.load(f1)

with open('en.json') as f2:
  targetData = json.load(f2)

results = jd.diff(originalData, targetData,syntax='explicit')
delete_results = results[jd.delete]
insert_results = list(results[jd.insert].keys())
update_results = results[jd.update]

dataset = {"deleted phrase": delete_results, "inserted phrase" : insert_results}
print ("{:<20} {:<20}".format("deleted phrase", "inserted phrase"))
for i in range(max(len(delete_results),len(insert_results))):
    try:
        inserts = dataset["inserted phrase"][i]
    except IndexError:
        inserts = ""

    try:
        deletes = dataset["deleted phrase"][i]
    except IndexError:
        deletes = ""
    print ("{:<20} {:<20}".format(deletes, inserts))

date_time = datetime.now()
dates = date_time.strftime("%m/%d/%Y, %H:%M:%S")

fields = ["numOfPhrases"]
List = [dates,max(len(originalData),len(targetData))]

with open('data.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(List)

x = []
y = []
with open('data.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(row[0])
        y.append(row[1])  

plt.plot(x,y, label='Application Phrases')
plt.xlabel('Date Time')
plt.ylabel('Number of Phrases')
plt.title('Phrases Change Diagram')
plt.legend()
plt.show()
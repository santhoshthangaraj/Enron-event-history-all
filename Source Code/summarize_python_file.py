# Add your python script here
#summarize_python_file
import sys
import operator
import datetime
import time
import collections
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

#Variable declaration
sendingCount ={}
receivingCount = {}
sortedSendingCount = {}
sortedReceivingCount = {}
topNSender = {}

#First Requirements
#Opening the file, couting the number of email sent and received by each person
with open(sys.argv[1],"r") as inputfile:
    for line in inputfile:
        items = line.split(",")
        if len(items) == 6:
            timeD,ID,sender,receiver,topic,mode = items
            listOfreceiver = receiver.split("|")
            if not sendingCount.has_key(sender):
                sendingCount[sender] = len(listOfreceiver)
            else:
                sendingCount[sender] = sendingCount[sender] + len(listOfreceiver)
            for listOfrec in listOfreceiver:
                if not receivingCount.has_key(listOfrec):
                    receivingCount[listOfrec] = 1
                else:
                    receivingCount[listOfrec] = receivingCount[listOfrec] + 1
                    
#Sorting the date based on email sent
sortedSendingCount = sorted(sendingCount.items(), key = lambda t: t[1], reverse=True)
sortedReceivingCount = sorted(receivingCount.items(), key = lambda t: t[1], reverse=True)

#Writing into the file named A.csv
outputFile = open("A.txt", "a")
outputFile.write("person");
outputFile.write(",");
outputFile.write("sent");
outputFile.write(",");
outputFile.write("received");
outputFile.write("\n");
for key,value in sortedSendingCount:    
    outputFile.write(key);
    outputFile.write(",");
    outputFile.write(str(value));
    outputFile.write(",");
    if receivingCount.has_key(key):
        outputFile.write(str(receivingCount.get(key)));
    else:
        outputFile.write("0");
    outputFile.write("\n");
for key, value in sortedReceivingCount:
    if not sendingCount.has_key(key):
        outputFile.write(key);
        outputFile.write(",");
        outputFile.write("0");
        outputFile.write(",");
        outputFile.write(str(value));
        outputFile.write(",");
        outputFile.write("\n");


#Second Requirements
#Get the top N person based on email sent
topN = 5
counter = 0
while (counter < topN and counter < len(sortedSendingCount)):
    key = sortedSendingCount[counter][0]
    topNSender[key] = 1
    counter += 1
    
#Analyzing the email count over time for the top 5 person in terms of message sent
SenderCountOverTime = {}
yearHafly = collections.OrderedDict()
yearHafly = {'f1998':0,'s1998':1,'f1999':2,'s1999':3,'f2000':4,'s2000':5,'f2001':6,'s2001':7,'f2002':8,'s2002':9}
with open(sys.argv[1],"r") as inputfile:
    for line in inputfile:
        items = line.split(",")
        if len(items) == 6:
            timeSend,ID,sender,receiver,topic,mode = items
            if topNSender.has_key(sender):
                listOfreceiver = receiver.split("|")
                countOverTime = {}
                formatTime = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(float(timeSend)/1000.))
                month,day,yearandtime = formatTime.split("/")
                year, exactTime = yearandtime.split(" ")
                if int(month) < 6:
                    haflyCount =  str("f") + str(year)
                else:
                    haflyCount =  str("s") + str(year)
                index = yearHafly.get(haflyCount)
                if not SenderCountOverTime.has_key(sender):
                    templist = [0,0,0,0,0,0,0,0,0,0]
                    templist[index] = len(listOfreceiver)
                    SenderCountOverTime[sender] = templist[:]
                else:   
                    templist[index] = SenderCountOverTime[sender][index] + len(listOfreceiver)                    
                    SenderCountOverTime[sender] = templist[:]


#Third requirements
#Analyzing the received unique email/person name count over time for the 5 person
trackingunique = {}
uniqueReceivedCountOverTime = {}
with open(sys.argv[1],"r") as inputfile:
    for line in inputfile:
        items = line.split(",")
        if len(items) == 6:
            timeSend,ID,sender,receiver,topic,mode = items            
            formatTime = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(float(timeSend)/1000.))
            month,day,yearandtime = formatTime.split("/")
            year, exactTime = yearandtime.split(" ")
            countreceiver = 0
            listOfreceiver = receiver.split("|")
            if int(month) < 6:
                haflyCount =  str("f") + str(year)
            else:
                haflyCount =  str("s") + str(year)
            index = yearHafly.get(haflyCount)
            while countreceiver < len(listOfreceiver):
                preceiver = listOfreceiver[countreceiver]
                if topNSender.has_key(preceiver):
                    timeAndSender = str(preceiver) + str(sender) + str(haflyCount)
                    if not trackingunique.has_key(timeAndSender):
                        trackingunique[timeAndSender] = 1                     
                        if not uniqueReceivedCountOverTime.has_key(preceiver):
                            tempor = [0,0,0,0,0,0,0,0,0,0]
                            tempor[index] = 1
                            uniqueReceivedCountOverTime[preceiver] = tempor
                        else:
                            uniqueReceivedCountOverTime[preceiver][index] += 1
                    else:
                        trackingunique[timeAndSender] = 1
                countreceiver += 1


#Visualization the second and third requirements which shows the email sent and received over the time in separate chart for the top N -5 person
#Xaxis - shows the duration hafly(six months)
xAxisName = ['1998-1st','1998-2nd','1999-1st','1999-2nd','2000-1st','2000-2nd','2001-1st','2001-2nd','2002-1st','2002-2nd']

#Get the person name, duration and email count
topNPersonSend = SenderCountOverTime.keys()
topNPersonSendCount = SenderCountOverTime.values()
topNPersonReceived = uniqueReceivedCountOverTime.keys()
topNPersonReceivedCount = uniqueReceivedCountOverTime.values()

#Plotting the figures
receivingFigure = plt.figure("Unique Email Receiving Count For Each Six Months")
plt.figure(1, figsize = (8.5,11))
axes = plt.gca()
axes.set_xlim([-2,11])
axes.set_ylim([-2,300])
yticks = np.arange(-2, 300, 10)
plt.xticks(range(10), xAxisName)
plt.yticks(yticks)
plt.plot(range(10), topNPersonReceivedCount[0], 'b-', label = topNPersonReceived[0])
plt.plot(range(10), topNPersonReceivedCount[1], 'r-', label = topNPersonReceived[1])
plt.plot(range(10), topNPersonReceivedCount[2], 'g-', label = topNPersonReceived[2])
plt.plot(range(10), topNPersonReceivedCount[3], 'y-', label = topNPersonReceived[3])
plt.plot(range(10), topNPersonReceivedCount[4], 'm-', label = topNPersonReceived[4])
plt.legend()
plt.xlabel('Duration(Six Months)')
plt.ylabel('Receiving Count')

sendingFigure = plt.figure("Sending Email Count For Each Six Months")
axes = plt.gca()
axes.set_xlim([-2,11])
axes.set_ylim([-2,7500])
yticks = np.arange(-2, 7500, 1000)
plt.xticks(range(10), xAxisName)
plt.yticks(yticks)
plt.plot(range(10), topNPersonSendCount[0], 'b-', label = topNPersonSend[0])
plt.plot(range(10), topNPersonSendCount[1], 'r-', label = topNPersonSend[1])
plt.plot(range(10), topNPersonSendCount[2], 'g-', label = topNPersonSend[2])
plt.plot(range(10), topNPersonSendCount[3], 'y-', label = topNPersonSend[3])
plt.plot(range(10), topNPersonSendCount[4], 'm-', label = topNPersonSend[4])
plt.legend()
plt.xlabel('Duration(Six Months)')
plt.ylabel('Sending Count')

#Saving the file
receivingFigure.savefig("Unique Email Receiving Count For Each Six Months", dpi=100)
sendingFigure.savefig("Sending Email Count For Each Six Months", dpi=100)
receivingFigure.show()
sendingFigure.show()
raw_input()


# coding: utf-8


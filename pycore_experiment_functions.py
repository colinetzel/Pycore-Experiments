#!/usr/bin/python
#Python version 2.7.12
import pandas
import numpy as np
import re
import time
import math
from scipy import stats
from core import pycore

def runExperiment_clientLog(logPath, csv, xType, initBandwidth, initDelay, initJitter, initLoss, initDuplicate, xVals, numRuns):
    curPath = logPath + csv
    workfile = open(curPath,"w")
    workfile.write("timestamp,sourceIP,sourcePort,destinationIP,destinationPort,ID,interval,dataTransferred,bandwidth\n")
    workfile.close()

    session = pycore.Session(persistent=True)
    node1 = session.addobj(cls=pycore.nodes.CoreNode, name="n1")
    node2 = session.addobj(cls=pycore.nodes.CoreNode, name="n2")
    hub1 = session.addobj(cls=pycore.nodes.HubNode, name="hub1")

    node1.newnetif(hub1, ["10.0.0.1/24"], ifname = "net1")
    node2.newnetif(hub1, ["10.0.0.2/24"], ifname = "net2")


    hub1.linkconfig(netif = node1.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
        loss = initLoss, duplicate = initDuplicate, devname=None)
    hub1.linkconfig(netif = node2.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
        loss = initLoss, duplicate = initDuplicate, devname=None)

    node2.cmd(["iperf", "-s"], wait = False)

    if xType == "bandwidth":
        
        for bandwidth in xVals:

            hub1.linkconfig(netif = node1.netif(0), bw = bandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)
            hub1.linkconfig(netif = node2.netif(0), bw = bandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)
            
            time.sleep(2) #give time for linkconfigs to be processed by CORE
            for i in range(numRuns):
                node1.shcmd("iperf -f b -y c -c 10.0.0.2 >> %s" %(curPath))
            

    elif xType == "delay":
        for delay in xVals:

            hub1.linkconfig(netif = node1.netif(0), bw = initBandwidth*1000000, delay = delay/2.0, jitter = initJitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)
            hub1.linkconfig(netif = node2.netif(0), bw = initBandwidth*1000000, delay = delay/2.0, jitter = initJitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)

            time.sleep(2) #give time for linkconfigs to be processed by CORE
            for i in range(numRuns):
                node1.shcmd("iperf -f b -y c -c 10.0.0.2 >> %s" %(curPath))

    elif xType == "jitter":
        for jitter in xVals:

            hub1.linkconfig(netif = node1.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = jitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)
            hub1.linkconfig(netif = node2.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = jitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)

            time.sleep(2) #give time for linkconfigs to be processed by CORE
            for i in range(numRuns):
                node1.shcmd("iperf -f b -y c -c 10.0.0.2 >> %s" %(curPath))

    elif xType == "loss":
        for loss in xVals:

            hub1.linkconfig(netif = node1.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = loss, duplicate = initDuplicate, devname=None)
            hub1.linkconfig(netif = node2.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = loss, duplicate = initDuplicate, devname=None)

            time.sleep(2) #give time for linkconfigs to be processed by CORE

            for i in range(numRuns):
                node1.shcmd("iperf -f b -y c -c 10.0.0.2 >> %s" %(curPath)) #try icmd as well?

    elif xType == "duplicate":
        for duplicate in xVals:

            hub1.linkconfig(netif = node1.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = initLoss, duplicate = duplicate, devname=None)
            hub1.linkconfig(netif = node2.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = initLoss, duplicate = duplicate, devname=None)

            time.sleep(2) #give time for linkconfigs to be processed by CORE

            for i in range(numRuns):
                node1.shcmd("iperf -f b -y c -c 10.0.0.2 >> %s" %(curPath))

    else:
        print("Error: invalid x-value type")
        session.shutdown()
        exit(-1)

    session.shutdown()
    return


def runExperiment_serverLog(logPath, csv, xType, initBandwidth, initDelay, initJitter, initLoss, initDuplicate, xVals, numRuns):
    curPath = logPath + csv
    workfile = open(curPath,"w")
    workfile.write("timestamp,sourceIP,sourcePort,destinationIP,destinationPort,ID,interval,dataTransferred,bandwidth\n")
    workfile.close()

    session = pycore.Session(persistent=True)
    node1 = session.addobj(cls=pycore.nodes.CoreNode, name="n1")
    node2 = session.addobj(cls=pycore.nodes.CoreNode, name="n2")
    hub1 = session.addobj(cls=pycore.nodes.HubNode, name="hub1")

    node1.newnetif(hub1, ["10.0.0.1/24"], ifname = "net1")
    node2.newnetif(hub1, ["10.0.0.2/24"], ifname = "net2")


    hub1.linkconfig(netif = node1.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
        loss = initLoss, duplicate = initDuplicate, devname=None)
    hub1.linkconfig(netif = node2.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
        loss = initLoss, duplicate = initDuplicate, devname=None)

    node2.shcmd("nohup iperf -s -f m >> %s &" %(curPath))

    if xType == "bandwidth":
        
        for bandwidth in xVals: 

            hub1.linkconfig(netif = node1.netif(0), bw = bandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)
            hub1.linkconfig(netif = node2.netif(0), bw = bandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)
            
            time.sleep(2) #give time for linkconfigs to be processed by CORE
            for i in range(numRuns):
                node1.cmd(["iperf","-c","10.0.0.2"], wait=True)
                time.sleep(30)
            

    elif xType == "delay":
        for delay in xVals: 

            hub1.linkconfig(netif = node1.netif(0), bw = initBandwidth*1000000, delay = delay/2.0, jitter = initJitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)
            hub1.linkconfig(netif = node2.netif(0), bw = initBandwidth*1000000, delay = delay/2.0, jitter = initJitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)

            time.sleep(2) #give time for linkconfigs to be processed by CORE
            for i in range(numRuns):
                node1.cmd(["iperf","-c","10.0.0.2"], wait=True)
                time.sleep(30)

    elif xType == "jitter":
        for jitter in xVals:

            hub1.linkconfig(netif = node1.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = jitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)
            hub1.linkconfig(netif = node2.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = jitter, 
                loss = initLoss, duplicate = initDuplicate, devname=None)

            time.sleep(2) #give time for linkconfigs to be processed by CORE
            for i in range(numRuns):
                node1.cmd(["iperf","-c","10.0.0.2"], wait=True)
                time.sleep(30)

    elif xType == "loss":
        for loss in xVals:

            hub1.linkconfig(netif = node1.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = loss, duplicate = initDuplicate, devname=None)
            hub1.linkconfig(netif = node2.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = loss, duplicate = initDuplicate, devname=None)

            time.sleep(2) #give time for linkconfigs to be processed by CORE

            for i in range(numRuns):
                node1.cmd(["iperf","-c","10.0.0.2"], wait=True)
                time.sleep(30)

    elif xType == "duplicate":
        for duplicate in xVals:

            hub1.linkconfig(netif = node1.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = initLoss, duplicate = duplicate, devname=None)
            hub1.linkconfig(netif = node2.netif(0), bw = initBandwidth*1000000, delay = initDelay, jitter = initJitter, 
                loss = initLoss, duplicate = duplicate, devname=None)

            time.sleep(2) #give time for linkconfigs to be processed by CORE

            for i in range(numRuns):
                node1.cmd(["iperf","-c","10.0.0.2"], wait=True)
                time.sleep(30)

    else:
        print("Error: invalid x-value type")
        session.shutdown()
        exit(-1)

    session.shutdown()
    return


def plotExperiment(xType, logPath, csvs, xVals, numRuns, experimentLength, outfile = None, logScale = False, lossSpecial = False, isServer = False):
    "Plot a single experiment from one or several csvs"

    if outfile:
        import matplotlib
        matplotlib.use('cairo')
    import matplotlib.pyplot as plt

    #use title from 1st csv
    if csvs[0] != "data.csv":
        title, isLegend = parseFilename(csvs[0])
        plt.title(title)
    else:
        isLegend = False

    #add axis labels
    if logScale:
        plt.ylabel('Log-Throughput (Mb/s)')
        plt.xlabel('Log-Bandwidth (Mb/s)')
    elif xType == "bandwidth":
        plt.ylabel('Throughput (Mb/s)')
        plt.xlabel('Bandwidth (Mb/s)')
    elif xType == "delay":
        plt.ylabel('Throughput (Mb/s)')
        plt.xlabel('Delay (us)')
    elif xType == "jitter":
        plt.ylabel('Throughput (Mb/s)')
        plt.xlabel('Jitter (us)')
    elif xType == "loss":
        plt.ylabel('Throughput (Mb/s)')
        plt.xlabel('Loss (%)')
    elif xType == "duplicate":
        plt.ylabel('Throughput (Mb/s)')
        plt.xlabel('Duplicate (%)')

    #parse and plot each csv
    for i in range(len(csvs)):

        if isServer: #server logging
            if(numRuns == 1):
                throughput = serverLogParse(logPath, csvs[i])
            else:
                throughput = []
                errors = []
                bandwidth = serverLogParse(logPath, csvs[i])

                for j in range(experimentLength):
                    throughput.append(np.average(bandwidth[j*numRuns:(j+1)*numRuns]))
                    errors.append(stats.sem(bandwidth[j*numRuns:(j+1)*numRuns]))

        else: #client logging
            iperfOut = pandas.read_csv(logPath + csvs[i])
            if(numRuns == 1):
                throughput = [float(throughput)/1000000 for throughput in iperfOut.bandwidth] # convert to megabits
            else:
                throughput = []
                errors = []
                for j in range(experimentLength):
                    throughput.append(np.average(iperfOut.bandwidth[j*numRuns:(j+1)*numRuns]/1000000))
                    errors.append(stats.sem(iperfOut.bandwidth[j*numRuns:(j+1)*numRuns]/1000000))
                
        if csvs[i] != "data.csv":
            legend = parseFilename(csvs[i])[1]
        else:
            legend = None

        if logScale:
            if numRuns > 1:
                plt.yscale('log')
                plt.xscale('log')
                plt.errorbar(xVals, throughput, yerr = errors, label = legend)
                plt.plot(xVals,xVals, 'r-')
            else:
                plt.loglog(xVals,throughput, label = legend)
                plt.loglog(xVals, xVals, 'r-')
        elif xType == "bandwidth":
            if numRuns > 1: #plot errors
                plt.errorbar(xVals, throughput, yerr = errors, label = legend)
            else:
                plt.plot(xVals, throughput, label = legend)
            plt.plot(xVals, xVals, 'r-')
        elif xType == "delay":
            if numRuns > 1: #plot errors
                plt.errorbar([val*2.0 for val in xVals], throughput, yerr = errors, label = legend)
            else:
                plt.plot([val*2.0 for val in xVals], throughput, label = legend)
        elif xType == "jitter":
            if numRuns > 1: #plot errors
                plt.errorbar(xVals, throughput, yerr = errors, label = legend)
            else:
                plt.plot(xVals, throughput, label = legend)
        elif xType == "loss":
            if numRuns > 1: #plot errors
                plt.errorbar([val*2.0 for val in xVals], throughput, yerr = errors, label = legend)
            else:
                plt.plot([val*2.0 for val in xVals], throughput, label = legend)
        elif xType == "duplicate":
            if numRuns > 1: #plot errors
                plt.errorbar([val*2.0 for val in xVals], throughput, yerr = errors, label = legend)
            else:
                plt.plot([val*2.0 for val in xVals], throughput, label = legend)
        else:
            print("Error: invalid x-value type.")
            exit(-1)

    if isLegend:
        plt.legend()
    if outfile:
        plt.savefig(outfile)
    plt.show()
    return

def serverLogParse(logPath, csv):
    "Produces a list of floats of throughput values (in Mbits) from the output of the server side of iperf version 2"
    bandwidthPattern = re.compile("[\d\.]+ Mbits") #grab the bandwidth + the units afterwards

    logFile = open(logPath + csv)

    throughputs = [bandwidthPattern.search(line) for line in logFile.readlines()]
    throughputs = filter(None, throughputs)
    throughputs = [float(x.group()[:-6]) for x in throughputs]

    return throughputs

def serverLogDebug(logPath, csv, newCsv):
    "Reads a server side experiment log and writes a list of the throughputs to a new csv file for manual examination."
    throughputs = serverLogParse(logPath, csv)
    writeOut = open(logPath + newCsv, "w")
    for entry in throughputs:
        writeOut.write(str(entry) + "\n")
    return

def parseFilename(filename):
    "Parse a csv output from experiment for the title and legend values"

    trimmed = filename[:-4] #trim .csv suffix
    values = trimmed.split("-")
    title = values[0]
    title = title.replace("_"," (",1)
    title = title + ")"
    title = title.replace("_"," ")


    legend = None
    for value in values[1:]:
        if "_" in value:
            continue #ignore constant values
        legend = value #1st nontitle value with no _ is legend
        break
        
    return (title, legend) #legend could be None
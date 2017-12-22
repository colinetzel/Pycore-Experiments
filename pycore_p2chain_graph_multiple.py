#!/usr/bin/python
#Python version 2.7.12
import argparse
import pycore_experiment_functions as functions


parser = argparse.ArgumentParser()
parser.add_argument("-o", type=str, default=None, help="Output filename.")
parser.add_argument("-x", type=str, default="bandwidth", choices=["bandwidth","delay", "jitter","loss","duplicate"]\
, help="Value to plot on x-axis") #add arg for ALL linkconfig values
parser.add_argument("-i", type=float, default=1, help="Interval between x-values (-1 is special log scale and selected by default)")
parser.add_argument("--length", type=int, default=10, help="Experiment length (number of points)")
parser.add_argument("--bandwidth", type=float, default=1, help="Constant/Initial bandwidth value for run (Default 1 Mb/s).")
parser.add_argument("--delay", type=float, default=0, help="Constant/Initial round-trip delay value for run.")
parser.add_argument("--jitter", type=float, default=0, help="Constant/Initial jitter value for run.")
parser.add_argument("--loss", type=float, default=0, help="Constant/Initial round-trip loss value for run.")
parser.add_argument("--duplicate", type=float, default=0, help="Constant/Initial round-trip duplicate value for run.")
parser.add_argument("--numRuns", type=int, default=1, help ="Number of runs to average together for each data point.")
parser.add_argument("--server", action='store_true', help="Use server logging instead of client logging.")
parser.add_argument("csvs", nargs= argparse.REMAINDER, default=["data.csv"], help="Remaining arguments (csv filenames of raw outputs)")

logPath = "" #Set this to a folder of your choice

args = parser.parse_args()

outfile = args.o
csvs = args.csvs
xType = args.x
interval = args.i
initBandwidth = args.bandwidth
initJitter = args.jitter
numRuns = args.numRuns
useServer = args.server

#convert to round-trip, half across each link
initDelay = args.delay/2.0
initLoss = args.loss/2.0
initDuplicate = args.duplicate/2.0



lossSpecial = False
logScale = False

if interval == -1:
    logScale = True
    experimentLength = 10
elif interval == -2:
    lossSpecial = True
    experimentLength = 8
else:
    experimentLength = args.length

#temppath = /home/colin/UNH_Masters_Program/Capstone_Project/logs/midnightstruggle.csv
if logScale: #logscale of bandwidth currently
    xVals = [0.1,0.2,0.5,1,2,5,10,20,50,100] #test
elif lossSpecial:
    xVals = [0.0,0.05,0.10,0.25,0.5,1.0,2.5,5.0] #rt loss is twice link loss
elif xType == "bandwidth":
    xVals = [interval*i for i in range(1,experimentLength+1)]
elif xType == "delay" or xType == "loss" or xType == "duplicate":
    xVals = [interval*i/2.0 for i in range(experimentLength)]
else:
    xVals = [interval*i for i in range(experimentLength)]


def main():
    functions.plotExperiment(xType, logPath, csvs, xVals, numRuns, experimentLength, outfile, logScale, lossSpecial, useServer)

main()
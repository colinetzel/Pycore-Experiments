#!/bin/sh
# Author: Colin Etzel
# requires superuser (sudo) privileges

# Example of using multiple graphs


# Client version of experiment

python pycore_P2chain_graph.py -o discard.pdf -x duplicate -i 1 --length 11 --delay 0 --bandwidth 10 --numRuns 25 -csv Client_10mbBandwidth_25runs-delay0ms.csv
python pycore_P2chain_graph.py -o discard.pdf -x duplicate -i 1 --length 11 --delay 10000 --bandwidth 10 --numRuns 25 -csv Client_10mbBandwidth_25runs-delay10ms.csv
python pycore_P2chain_graph.py -o discard.pdf -x duplicate -i 1 --length 11 --delay 100000 --bandwidth 10 --numRuns 25 -csv Client_10mbBandwidth_25runs-delay100ms.csv

python pycore_p2chain_graph_multiple.py -o clientDuplicateDelayRanges.pdf -x duplicate -i 1 --length 11 --numRuns 25 Client_10mbBandwidth_25runs-delay0ms.csv Client_10mbBandwidth_25runs-delay10ms.csv Client_10mbBandwidth_25runs-delay100ms.csv

# Server version of experiment

python pycore_P2chain_graph.py -o discard.pdf -x duplicate -i 1 --length 11 --server True --delay 0 --bandwidth 10 -csv Server_10mbBandwidth_25runs-delay0ms.csv --numRuns 25 --server True
python pycore_P2chain_graph.py -o discard.pdf -x duplicate -i 1 --length 11 --server True --delay 10000 --bandwidth 10 -csv Server_10mbBandwidth_25runs-delay10ms.csv --numRuns 25 --server True
python pycore_P2chain_graph.py -o discard.pdf -x duplicate -i 1 --length 11 --server True --delay 100000 --bandwidth 10 -csv Server_10mbBandwidth_25runs-delay100ms.csv --numRuns 25 --server True

python pycore_p2chain_graph_multiple.py -o serverDuplicateDelayRanges.pdf -x duplicate -i 1 --length 11 --server True --numRuns 25 Server_10mbBandwidth_25runs-delay0ms.csv Server_10mbBandwidth_25runs-delay10ms.csv Server_10mbBandwidth_25runs-delay100ms.csv
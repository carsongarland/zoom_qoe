#!/bin/bash

#RESULT DIRECTORY NAME
DIRNAME='/root/zoom-analysis/data/'

#PCAP FILE NAME
FILENAME='zoom'

#CAPTURE TIME
TIME=60

#INTERFACE
IFACE='enp3s0f0'

#SNAPSHOT LENGTH
SNAPLEN=3000

#RING BUFFER SIZE
RING_BUFFER_SIZE=1024

#CURRENT TIME
current_time=$(date "+%Y-%m-%d-%H%M")

#CAPTURING PACKETS
echo 'Capturing ZOOM Packets'
timeout -s SIGINT $TIME /root/gulp-v2/cmake-build-release/bin/gulp -f "udp port 8801" -i $IFACE -s $SNAPLEN -o $DIRNAME -n $FILENAME -r $RING_BUFFER_SIZE 

#USING PRINCETON TOOL
cd $DIRNAME
make all

#ANONYMIZATION 
python3 /root/zoom_pipeline/make_anon.py $DIRNAME'stats.csv' $DIRNAME'meetings.csv' $DIRNAME'streams.csv'
mkdir ./results
mv ./stats_anon.csv ./results/stats_anon.csv
mv ./meetings_anon.csv ./results/meetings_anon.csv
mv ./types.csv ./results/types_anon.csv 
mv ./streams_anon.csv ./results/streams_anon.csv

#UPLOADING TO GOOGLE DRIVE
/root/zoom_pipeline/upload.sh ./results "zoom-"$current_time

#CLEAN UP
make spotless
rm *.pcap
rm -r ./results

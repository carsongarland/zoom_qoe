# Zoom Quality of Experience

## Zoom Traffic Capture

This repository contains tools to collect, anonymize, and analyze packet traces of Columbia University Zoom traffic. 

### Scripts

#### zoom_pipeline.sh

Captures packets associated with Zoom for the collection pipeline and facilitates the subsequent anonyization/analyzation.
* uses gulp to filter out Zoom packets from the pipeline
* uses Princeton tool to create CSV from PCAP
* uses make_anon.py to anonymize CSV
* uses upload.sh to upload results to Google Drive

#### make_anon.py

Anonymizes Columbia IPs.
* uses Cryptopan to anonymize Columbia IPs while retaining Zoom IPs

#### upload.sh

Uploads resulting CSV to Google Drive.

## Zoom Analysis

This repository contains tools analyze csv packet traces of Columbia University Zoom traffic. 

### Scripts

#### crashes.py

Identifies potential crashes within Zoom Meetings.
* utilizes UDP connection analysis.
* uses loss as potential indicator.

#### zoom_analysis.py

Produces relevant metrics for further analysis into Zoom Meeting performance.

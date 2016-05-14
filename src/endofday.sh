#!/bin/bash

set -e

DATE=`date +"%Y%m%d"`
LOG=log.$DATE.jsonl
REPORT=report.$DATE.html

echo "backup $DATE log"
cat $LOG | gzip > $HOME/recoil/logs/$LOG.gz

echo "extracting data"
grep DATA $LOG | pytho src/extract_data.py

echo "Back up market data to AWS S3"
aws s3 sync $HOME/recoil/logs s3://ltcm/logs --size-only

echo "Creating report ($REPORT)"
python src/daily_report.py < $LOG > $REPORT

echo "Cleaning session logs"
rm $LOG

echo "Done."


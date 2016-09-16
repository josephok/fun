#!/bin/bash

# Add this script to crontab:
# eg.
# 0 * * * * /home/joe/code/fun/cron/spider.sh

cd /home/joe/code/fun && python3 main.py &> logs/spider/stdout.log

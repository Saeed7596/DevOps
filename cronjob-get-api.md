> sudo apt-get install curl

> crontab -l # View current cronjobs

> crontab -e # Edit cronjobs

# Get api every minute
* * * * * curl -X GET https://example.com >> /path/to/logfile.log 2>&1

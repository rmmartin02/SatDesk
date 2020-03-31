Generates full images from himwari-8 and goes-16 satellites

### Windows:
Use this to article to setup scheduler to run this about every 10 minutes:

https://www.esri.com/arcgis-blog/products/product/analytics/scheduling-a-python-script-or-model-to-run-at-a-prescribed-time/?rmedium=redirect&rsource=blogs.esri.com/esri/arcgis/2013/07/30/scheduling-a-scrip

### Mac:
Use crontab to setup script to run every 10 minutes
* Find path to SatDesk
* Then setup crontab
```
crontab */10 * * * *  cd {path to SatDesk folder} && $(which python3) desktop.py >> cron.log

```

Then setup your desktop to point towards the 'finalImages' folder and slideshow every <10 minutes
## Itunes Analytics App Data Downloading Script
## Author: D.Kisler <admin@dkisler.de>

import json
import os
from itunes_app_analytics import (Params, 
                                  Login, 
                                  DataFetcher, 
                                  browser)

def dates_list(dates, interval = 'm'):
    from datetime import (datetime, timedelta)
    # dates borders
    start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    
    if interval == 'd':
        dates_list = [(start + timedelta(days=x)).strftime('%Y%m%d') for x in range(0, (end-start).days)]
    else:
        total_months = lambda dt: dt.month + 12 * dt.year
        dates_list = []    
        for tot_m in range(total_months(start)-1, total_months(end)):
            y, m = divmod(tot_m, 12)
            dates_list.append(datetime(y, m+1, 1).strftime("%Y%m")) 
    return dates_list

## credentials
PATH = os.path.dirname(__file__)
credentials = json.load(open(os.path.join(PATH, 'credentials.json')))
## folder to save data
PATHo = 'path/to/save/data'
## application itunes ID
appID = itunesAppID
## dates
date_start, date_end = '2017-06-01', '2018-08-01'
dates = dates_list([date_start, date_end])

## login into the appconenct
_ = Login(credentials['user'], credentials['pass'])
## data fetcher instance
fetcher = DataFetcher
# list of metrics
param = Params()
#
#viewBy = {'overall':None}
viewBy = {}
for k,v in param.viewby.items():
    viewBy[k] = v
#
def dirmk(dir_out):
    fetcher.output_dir(download_dir = dir_out)
    if not os.path.isdir(dir_out):
        os.mkdir(dir_out)
# 
downloader = fetcher.download
for iM in param.measure.keys(): 
    # set the output dir
    dir_out = os.path.join(PATHo, iM)
    dirmk(dir_out)
    for iD in dates:
        for iV, iVval in viewBy.items():
            dirmk(os.path.join(dir_out, iV))
            downloader(appID, param.measure[iM], param.interval['month'], param.zoom['day'], iD, iVval)

browser.close()